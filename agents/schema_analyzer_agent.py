"""
Schema Analyzer Agent for SQL to NoSQL Migration

This agent analyzes SQL database schemas, identifies relationships,
constraints, and data patterns to inform the migration strategy.
"""

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config

class SchemaAnalyzerAgent:
    """Agent responsible for analyzing SQL database schema and relationships"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.TEMPERATURE
        )
        
        self.agent = Agent(
            role="Database Schema Analyst",
            goal="Analyze SQL database schema to understand structure, relationships, and constraints for NoSQL migration planning",
            backstory="""You are an expert database architect with 15+ years of experience in both SQL and NoSQL databases. 
            You specialize in analyzing complex relational database schemas and understanding how they can be optimally 
            restructured for document-based NoSQL systems. Your expertise includes identifying normalization patterns, 
            foreign key relationships, and data access patterns that inform migration strategies.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def analyze_schema(self, schema_info: dict) -> dict:
        """
        Analyze SQL schema and return structured analysis
        
        Args:
            schema_info: Dictionary containing SQL schema information
            
        Returns:
            Dictionary with schema analysis results
        """
        task_description = f"""
        Analyze the following SQL database schema and provide a comprehensive analysis:
        
        Schema Information:
        {schema_info}
        
        Please provide analysis covering:
        1. Table relationships and foreign key dependencies
        2. Data types and constraints
        3. Index patterns and performance implications
        4. Normalization level and potential denormalization opportunities
        5. Data volume estimates and access patterns
        6. Migration complexity assessment
        """
        
        # This would typically involve actual database introspection
        # For this example, we'll simulate the analysis
        analysis_result = {
            "tables": schema_info.get("tables", []),
            "relationships": self._identify_relationships(schema_info),
            "constraints": self._analyze_constraints(schema_info),
            "migration_complexity": self._assess_complexity(schema_info),
            "recommendations": self._generate_recommendations(schema_info)
        }
        
        return analysis_result
    
    def _identify_relationships(self, schema_info: dict) -> list:
        """Identify foreign key relationships between tables"""
        relationships = []
        tables = schema_info.get("tables", [])
        
        for table in tables:
            for column in table.get("columns", []):
                if column.get("is_foreign_key"):
                    relationships.append({
                        "from_table": table["name"],
                        "from_column": column["name"],
                        "to_table": column.get("references_table"),
                        "to_column": column.get("references_column"),
                        "relationship_type": "one_to_many" if column.get("nullable") else "many_to_one"
                    })
        
        return relationships
    
    def _analyze_constraints(self, schema_info: dict) -> dict:
        """Analyze database constraints and their implications"""
        return {
            "primary_keys": self._extract_primary_keys(schema_info),
            "unique_constraints": self._extract_unique_constraints(schema_info),
            "check_constraints": self._extract_check_constraints(schema_info),
            "not_null_constraints": self._extract_not_null_constraints(schema_info)
        }
    
    def _extract_primary_keys(self, schema_info: dict) -> list:
        """Extract primary key information"""
        primary_keys = []
        for table in schema_info.get("tables", []):
            for column in table.get("columns", []):
                if column.get("is_primary_key"):
                    primary_keys.append({
                        "table": table["name"],
                        "column": column["name"],
                        "type": column.get("type")
                    })
        return primary_keys
    
    def _extract_unique_constraints(self, schema_info: dict) -> list:
        """Extract unique constraint information"""
        unique_constraints = []
        for table in schema_info.get("tables", []):
            for column in table.get("columns", []):
                if column.get("is_unique"):
                    unique_constraints.append({
                        "table": table["name"],
                        "column": column["name"]
                    })
        return unique_constraints
    
    def _extract_check_constraints(self, schema_info: dict) -> list:
        """Extract check constraint information"""
        # Simplified implementation
        return []
    
    def _extract_not_null_constraints(self, schema_info: dict) -> list:
        """Extract not null constraint information"""
        not_null_constraints = []
        for table in schema_info.get("tables", []):
            for column in table.get("columns", []):
                if not column.get("nullable", True):
                    not_null_constraints.append({
                        "table": table["name"],
                        "column": column["name"]
                    })
        return not_null_constraints
    
    def _assess_complexity(self, schema_info: dict) -> dict:
        """Assess migration complexity based on schema analysis"""
        tables = schema_info.get("tables", [])
        relationships = self._identify_relationships(schema_info)
        
        complexity_score = 0
        factors = []
        
        # Factor in number of tables
        if len(tables) > 20:
            complexity_score += 3
            factors.append("Large number of tables")
        elif len(tables) > 10:
            complexity_score += 2
            factors.append("Moderate number of tables")
        
        # Factor in relationships
        if len(relationships) > 50:
            complexity_score += 3
            factors.append("Complex relationship network")
        elif len(relationships) > 20:
            complexity_score += 2
            factors.append("Moderate relationship complexity")
        
        # Factor in data types
        complex_types = ["JSON", "BLOB", "CLOB", "XML"]
        has_complex_types = any(
            any(col.get("type", "").upper() in complex_types for col in table.get("columns", []))
            for table in tables
        )
        if has_complex_types:
            complexity_score += 2
            factors.append("Complex data types present")
        
        return {
            "score": complexity_score,
            "level": "High" if complexity_score >= 5 else "Medium" if complexity_score >= 3 else "Low",
            "factors": factors
        }
    
    def _generate_recommendations(self, schema_info: dict) -> list:
        """Generate migration recommendations based on schema analysis"""
        recommendations = []
        
        # Analyze for denormalization opportunities
        relationships = self._identify_relationships(schema_info)
        if len(relationships) > 10:
            recommendations.append({
                "type": "denormalization",
                "description": "Consider denormalizing frequently accessed related data into single documents",
                "priority": "high"
            })
        
        # Check for potential document structure patterns
        tables = schema_info.get("tables", [])
        if any(table.get("name", "").endswith("_details") for table in tables):
            recommendations.append({
                "type": "document_structure",
                "description": "Consider embedding detail tables as subdocuments in parent collections",
                "priority": "medium"
            })
        
        return recommendations
