"""
Data Mapper Agent for SQL to NoSQL Migration

This agent maps SQL table structures to optimal NoSQL document structures,
considering relationships, access patterns, and performance requirements.
"""

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config

class DataMapperAgent:
    """Agent responsible for mapping SQL structures to NoSQL document structures"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.TEMPERATURE
        )
        
        self.agent = Agent(
            role="Data Structure Mapping Specialist",
            goal="Map SQL table structures to optimal NoSQL document structures for efficient data access and storage",
            backstory="""You are a senior data architect with extensive experience in both relational and NoSQL databases. 
            You excel at understanding data access patterns and designing document structures that optimize for 
            read performance while maintaining data integrity. Your expertise includes identifying embedding vs 
            referencing strategies, designing appropriate indexes, and balancing normalization with denormalization 
            for NoSQL systems.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def map_sql_to_nosql(self, schema_analysis: dict) -> dict:
        """
        Map SQL schema to NoSQL document structure
        
        Args:
            schema_analysis: Output from SchemaAnalyzerAgent
            
        Returns:
            Dictionary with NoSQL document mappings
        """
        mapping_result = {
            "collections": [],
            "relationships": [],
            "indexes": [],
            "embedding_strategies": []
        }
        
        # Process each table and create collection mappings
        for table in schema_analysis.get("tables", []):
            collection_mapping = self._create_collection_mapping(table, schema_analysis)
            mapping_result["collections"].append(collection_mapping)
        
        # Define relationship strategies
        mapping_result["relationships"] = self._define_relationship_strategies(schema_analysis)
        
        # Suggest indexes
        mapping_result["indexes"] = self._suggest_indexes(mapping_result["collections"])
        
        # Define embedding strategies
        mapping_result["embedding_strategies"] = self._define_embedding_strategies(schema_analysis)
        
        return mapping_result
    
    def _create_collection_mapping(self, table: dict, schema_analysis: dict) -> dict:
        """Create NoSQL collection mapping for a SQL table"""
        relationships = schema_analysis.get("relationships", [])
        table_relationships = [r for r in relationships if r["from_table"] == table["name"]]
        
        # Determine if this should be embedded or referenced
        embedding_strategy = self._determine_embedding_strategy(table, table_relationships)
        
        collection_mapping = {
            "sql_table": table["name"],
            "nosql_collection": self._convert_to_collection_name(table["name"]),
            "document_structure": self._design_document_structure(table),
            "embedding_strategy": embedding_strategy,
            "primary_key_mapping": self._map_primary_key(table),
            "field_mappings": self._map_fields(table),
            "relationships": table_relationships
        }
        
        return collection_mapping
    
    def _convert_to_collection_name(self, table_name: str) -> str:
        """Convert SQL table name to NoSQL collection name"""
        # Convert snake_case to camelCase or keep as is
        return table_name.lower()
    
    def _design_document_structure(self, table: dict) -> dict:
        """Design the document structure for a table"""
        document_structure = {
            "_id": "ObjectId (auto-generated)",
            "metadata": {
                "created_at": "timestamp",
                "updated_at": "timestamp",
                "version": "number"
            }
        }
        
        # Add fields from SQL table
        for column in table.get("columns", []):
            field_name = column["name"]
            field_type = self._map_sql_to_nosql_type(column.get("type", "VARCHAR"))
            
            document_structure[field_name] = {
                "type": field_type,
                "required": not column.get("nullable", True),
                "unique": column.get("is_unique", False),
                "indexed": column.get("is_primary_key", False) or column.get("is_unique", False)
            }
        
        return document_structure
    
    def _map_sql_to_nosql_type(self, sql_type: str) -> str:
        """Map SQL data types to NoSQL equivalent types"""
        type_mapping = {
            "VARCHAR": "string",
            "TEXT": "string",
            "INT": "int32",
            "BIGINT": "int64",
            "DECIMAL": "decimal128",
            "FLOAT": "double",
            "DOUBLE": "double",
            "BOOLEAN": "bool",
            "DATE": "date",
            "DATETIME": "date",
            "TIMESTAMP": "timestamp",
            "JSON": "object",
            "BLOB": "binData"
        }
        
        sql_type_upper = sql_type.upper()
        for sql_key, nosql_type in type_mapping.items():
            if sql_key in sql_type_upper:
                return nosql_type
        
        return "string"  # Default fallback
    
    def _determine_embedding_strategy(self, table: dict, relationships: list) -> str:
        """Determine whether to embed or reference related data"""
        # Simple heuristic: if table has many relationships or is a lookup table, use reference
        if len(relationships) > 3:
            return "reference"
        
        # If table name suggests it's a detail/lookup table, embed
        if any(keyword in table["name"].lower() for keyword in ["detail", "lookup", "config"]):
            return "embed"
        
        return "reference"  # Default to reference for safety
    
    def _map_primary_key(self, table: dict) -> dict:
        """Map SQL primary key to NoSQL _id field"""
        for column in table.get("columns", []):
            if column.get("is_primary_key"):
                return {
                    "sql_column": column["name"],
                    "nosql_field": "_id",
                    "type": self._map_sql_to_nosql_type(column.get("type", "VARCHAR"))
                }
        
        return {"sql_column": "id", "nosql_field": "_id", "type": "ObjectId"}
    
    def _map_fields(self, table: dict) -> list:
        """Map SQL fields to NoSQL document fields"""
        field_mappings = []
        
        for column in table.get("columns", []):
            if not column.get("is_primary_key"):  # Skip primary key as it's handled separately
                field_mapping = {
                    "sql_column": column["name"],
                    "nosql_field": column["name"],
                    "type": self._map_sql_to_nosql_type(column.get("type", "VARCHAR")),
                    "required": not column.get("nullable", True),
                    "indexed": column.get("is_unique", False)
                }
                field_mappings.append(field_mapping)
        
        return field_mappings
    
    def _define_relationship_strategies(self, schema_analysis: dict) -> list:
        """Define strategies for handling relationships in NoSQL"""
        relationships = schema_analysis.get("relationships", [])
        strategies = []
        
        for rel in relationships:
            strategy = {
                "from_collection": self._convert_to_collection_name(rel["from_table"]),
                "to_collection": self._convert_to_collection_name(rel["to_table"]),
                "relationship_type": rel["relationship_type"],
                "strategy": self._choose_relationship_strategy(rel),
                "implementation": self._define_implementation(rel)
            }
            strategies.append(strategy)
        
        return strategies
    
    def _choose_relationship_strategy(self, relationship: dict) -> str:
        """Choose appropriate strategy for relationship"""
        rel_type = relationship["relationship_type"]
        
        if rel_type == "one_to_many":
            return "embed" if relationship.get("cardinality", "low") == "low" else "reference"
        elif rel_type == "many_to_one":
            return "reference"
        else:
            return "reference"
    
    def _define_implementation(self, relationship: dict) -> dict:
        """Define implementation details for relationship"""
        strategy = self._choose_relationship_strategy(relationship)
        
        if strategy == "embed":
            return {
                "type": "embedding",
                "description": f"Embed {relationship['to_table']} documents in {relationship['from_table']}",
                "field_name": f"{relationship['to_table']}_data"
            }
        else:
            return {
                "type": "reference",
                "description": f"Store reference to {relationship['to_table']} in {relationship['from_table']}",
                "field_name": f"{relationship['to_table']}_id"
            }
    
    def _suggest_indexes(self, collections: list) -> list:
        """Suggest indexes for NoSQL collections"""
        indexes = []
        
        for collection in collections:
            collection_name = collection["nosql_collection"]
            
            # Primary key index (always needed)
            indexes.append({
                "collection": collection_name,
                "index": {"_id": 1},
                "type": "unique",
                "description": "Primary key index"
            })
            
            # Indexes for unique fields
            for field in collection["field_mappings"]:
                if field.get("indexed"):
                    indexes.append({
                        "collection": collection_name,
                        "index": {field["nosql_field"]: 1},
                        "type": "unique" if field.get("unique") else "regular",
                        "description": f"Index on {field['nosql_field']}"
                    })
        
        return indexes
    
    def _define_embedding_strategies(self, schema_analysis: dict) -> list:
        """Define embedding strategies for related data"""
        strategies = []
        
        # Analyze tables for embedding opportunities
        tables = schema_analysis.get("tables", [])
        relationships = schema_analysis.get("relationships", [])
        
        for table in tables:
            table_relationships = [r for r in relationships if r["from_table"] == table["name"]]
            
            if len(table_relationships) > 0:
                strategy = {
                    "parent_collection": self._convert_to_collection_name(table["name"]),
                    "embedding_opportunities": [],
                    "recommendations": []
                }
                
                for rel in table_relationships:
                    if self._should_embed(rel):
                        strategy["embedding_opportunities"].append({
                            "child_table": rel["to_table"],
                            "child_collection": self._convert_to_collection_name(rel["to_table"]),
                            "reason": "Frequently accessed together"
                        })
                
                if strategy["embedding_opportunities"]:
                    strategies.append(strategy)
        
        return strategies
    
    def _should_embed(self, relationship: dict) -> bool:
        """Determine if a relationship should be embedded"""
        # Simple heuristic: embed if it's a one-to-many with low cardinality
        return (relationship["relationship_type"] == "one_to_many" and 
                relationship.get("cardinality", "low") == "low")
