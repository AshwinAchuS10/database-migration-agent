"""
Migration Planner Agent for SQL to NoSQL Migration

This agent creates detailed migration plans, scripts, and execution strategies
based on schema analysis and data mapping results.
"""

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config
import json
from datetime import datetime

class MigrationPlannerAgent:
    """Agent responsible for creating detailed migration plans and scripts"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.TEMPERATURE
        )
        
        self.agent = Agent(
            role="Database Migration Strategist",
            goal="Create comprehensive migration plans with detailed scripts, validation steps, and rollback procedures for SQL to NoSQL database migration",
            backstory="""You are a senior database migration specialist with 20+ years of experience in large-scale 
            database migrations. You have successfully migrated hundreds of databases from SQL to NoSQL systems, 
            handling everything from small applications to enterprise-level systems with millions of records. 
            Your expertise includes creating zero-downtime migration strategies, data validation procedures, 
            and comprehensive rollback plans.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_migration_plan(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """
        Create comprehensive migration plan based on analysis and mapping
        
        Args:
            schema_analysis: Output from SchemaAnalyzerAgent
            data_mapping: Output from DataMapperAgent
            
        Returns:
            Dictionary with detailed migration plan
        """
        migration_plan = {
            "migration_overview": self._create_migration_overview(schema_analysis, data_mapping),
            "phases": self._define_migration_phases(schema_analysis, data_mapping),
            "scripts": self._generate_migration_scripts(data_mapping),
            "validation_plan": self._create_validation_plan(schema_analysis, data_mapping),
            "rollback_plan": self._create_rollback_plan(schema_analysis, data_mapping),
            "timeline": self._estimate_timeline(schema_analysis, data_mapping),
            "risk_assessment": self._assess_risks(schema_analysis, data_mapping)
        }
        
        return migration_plan
    
    def _create_migration_overview(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """Create high-level migration overview"""
        tables = schema_analysis.get("tables", [])
        collections = data_mapping.get("collections", [])
        
        return {
            "source_database": "SQL Database",
            "target_database": "MongoDB",
            "total_tables": len(tables),
            "total_collections": len(collections),
            "migration_strategy": "Phased approach with validation",
            "estimated_duration": self._estimate_duration(schema_analysis),
            "complexity_level": schema_analysis.get("migration_complexity", {}).get("level", "Medium")
        }
    
    def _define_migration_phases(self, schema_analysis: dict, data_mapping: dict) -> list:
        """Define migration phases"""
        phases = [
            {
                "phase": 1,
                "name": "Preparation and Setup",
                "description": "Set up target database, create collections, and prepare migration environment",
                "tasks": [
                    "Create MongoDB database and collections",
                    "Set up indexes as defined in mapping",
                    "Prepare migration scripts and tools",
                    "Set up monitoring and logging"
                ],
                "duration": "1-2 days",
                "dependencies": []
            },
            {
                "phase": 2,
                "name": "Data Migration - Core Tables",
                "description": "Migrate core business tables with minimal dependencies",
                "tasks": [
                    "Migrate lookup and reference tables",
                    "Migrate core entity tables",
                    "Validate data integrity",
                    "Test basic functionality"
                ],
                "duration": "2-3 days",
                "dependencies": ["Phase 1"]
            },
            {
                "phase": 3,
                "name": "Data Migration - Related Tables",
                "description": "Migrate tables with foreign key relationships",
                "tasks": [
                    "Migrate related tables in dependency order",
                    "Update embedded documents",
                    "Create and validate references",
                    "Test relationship integrity"
                ],
                "duration": "3-5 days",
                "dependencies": ["Phase 2"]
            },
            {
                "phase": 4,
                "name": "Validation and Testing",
                "description": "Comprehensive validation and performance testing",
                "tasks": [
                    "Run data validation scripts",
                    "Performance testing and optimization",
                    "Application integration testing",
                    "User acceptance testing"
                ],
                "duration": "2-3 days",
                "dependencies": ["Phase 3"]
            },
            {
                "phase": 5,
                "name": "Cutover and Go-Live",
                "description": "Final cutover to new database system",
                "tasks": [
                    "Final data synchronization",
                    "Application deployment",
                    "Monitoring and support",
                    "Documentation updates"
                ],
                "duration": "1 day",
                "dependencies": ["Phase 4"]
            }
        ]
        
        return phases
    
    def _generate_migration_scripts(self, data_mapping: dict) -> dict:
        """Generate migration scripts for each collection"""
        scripts = {
            "python_scripts": [],
            "mongodb_scripts": [],
            "validation_scripts": []
        }
        
        collections = data_mapping.get("collections", [])
        
        for collection in collections:
            # Generate Python migration script
            python_script = self._create_python_migration_script(collection)
            scripts["python_scripts"].append(python_script)
            
            # Generate MongoDB setup script
            mongodb_script = self._create_mongodb_setup_script(collection)
            scripts["mongodb_scripts"].append(mongodb_script)
        
        # Generate validation script
        validation_script = self._create_validation_script(collections)
        scripts["validation_scripts"].append(validation_script)
        
        return scripts
    
    def _create_python_migration_script(self, collection: dict) -> dict:
        """Create Python script for migrating a specific collection"""
        sql_table = collection["sql_table"]
        nosql_collection = collection["nosql_collection"]
        
        script_content = f'''"""
Migration script for {sql_table} -> {nosql_collection}
Generated by Migration Planner Agent
"""

import pymongo
import sqlalchemy
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import json
from datetime import datetime

def migrate_{sql_table.lower()}():
    """Migrate {sql_table} table to {nosql_collection} collection"""
    
    # Database connections
    sql_engine = create_engine('{Config.SQL_CONNECTION_STRING}')
    mongo_client = MongoClient('{Config.MONGODB_CONNECTION_STRING}')
    db = mongo_client['migrated_db']
    collection = db['{nosql_collection}']
    
    try:
        # Query SQL data
        with sql_engine.connect() as conn:
            query = text("SELECT * FROM {sql_table}")
            result = conn.execute(query)
            rows = result.fetchall()
        
        # Transform and insert into MongoDB
        documents = []
        for row in rows:
            doc = {{
                # Map SQL columns to document fields
                {self._generate_field_mappings(collection)}
            }}
            documents.append(doc)
        
        # Batch insert to MongoDB
        if documents:
            collection.insert_many(documents)
            print(f"Migrated {{len(documents)}} documents to {nosql_collection}")
        
    except Exception as e:
        print(f"Error migrating {sql_table}: {{str(e)}}")
        raise
    finally:
        sql_engine.dispose()
        mongo_client.close()

if __name__ == "__main__":
    migrate_{sql_table.lower()}()
'''
        
        return {
            "filename": f"migrate_{sql_table.lower()}.py",
            "content": script_content,
            "description": f"Migration script for {sql_table} table"
        }
    
    def _generate_field_mappings(self, collection: dict) -> str:
        """Generate field mapping code for migration script"""
        mappings = []
        for field in collection.get("field_mappings", []):
            sql_col = field["sql_column"]
            nosql_field = field["nosql_field"]
            mappings.append(f'                "{nosql_field}": row.{sql_col},')
        
        return "\\n".join(mappings)
    
    def _create_mongodb_setup_script(self, collection: dict) -> dict:
        """Create MongoDB setup script for a collection"""
        nosql_collection = collection["nosql_collection"]
        
        script_content = f'''-- MongoDB setup script for {nosql_collection} collection
-- Generated by Migration Planner Agent

use migrated_db;

-- Create collection
db.createCollection("{nosql_collection}");

-- Create indexes
{self._generate_index_commands(collection)}

-- Create validation rules
{self._generate_validation_rules(collection)}
'''
        
        return {
            "filename": f"setup_{nosql_collection}.js",
            "content": script_content,
            "description": f"MongoDB setup script for {nosql_collection} collection"
        }
    
    def _generate_index_commands(self, collection: dict) -> str:
        """Generate MongoDB index creation commands"""
        index_commands = []
        
        # Primary key index
        index_commands.append(f'db.{collection["nosql_collection"]}.createIndex({{"_id": 1}});')
        
        # Other indexes based on field mappings
        for field in collection.get("field_mappings", []):
            if field.get("indexed"):
                index_commands.append(f'db.{collection["nosql_collection"]}.createIndex({{"{field["nosql_field"]}": 1}});')
        
        return "\\n".join(index_commands)
    
    def _generate_validation_rules(self, collection: dict) -> str:
        """Generate MongoDB validation rules"""
        validation_rules = []
        
        for field in collection.get("field_mappings", []):
            if field.get("required"):
                validation_rules.append(f'"{field["nosql_field"]}": {{"$exists": true}}')
        
        if validation_rules:
            return f'''db.runCommand({{
    collMod: "{collection["nosql_collection"]}",
    validator: {{
        $jsonSchema: {{
            bsonType: "object",
            required: [{", ".join(f'"{field["nosql_field"]}"' for field in collection.get("field_mappings", []) if field.get("required"))}]
        }}
    }}
}});'''
        return ""
    
    def _create_validation_script(self, collections: list) -> dict:
        """Create comprehensive validation script"""
        script_content = '''"""
Data validation script for SQL to NoSQL migration
Generated by Migration Planner Agent
"""

import pymongo
import sqlalchemy
from sqlalchemy import create_engine, text
from pymongo import MongoClient

def validate_migration():
    """Validate data integrity after migration"""
    
    sql_engine = create_engine('{Config.SQL_CONNECTION_STRING}')
    mongo_client = MongoClient('{Config.MONGODB_CONNECTION_STRING}')
    db = mongo_client['migrated_db']
    
    validation_results = {
        "total_tables": 0,
        "validated_tables": 0,
        "errors": [],
        "warnings": []
    }
    
    try:
        # Validate each collection
        collections = db.list_collection_names()
        
        for collection_name in collections:
            validation_results["total_tables"] += 1
            
            # Count records in both databases
            sql_count = get_sql_count(sql_engine, collection_name)
            mongo_count = db[collection_name].count_documents({{}})
            
            if sql_count != mongo_count:
                validation_results["errors"].append(f"Record count mismatch for {collection_name}: SQL={sql_count}, MongoDB={mongo_count}")
            else:
                validation_results["validated_tables"] += 1
                print(f"✓ {collection_name}: {mongo_count} records validated")
        
        # Summary
        print(f"\\nValidation Summary:")
        print(f"Total tables: {validation_results['total_tables']}")
        print(f"Validated: {validation_results['validated_tables']}")
        print(f"Errors: {len(validation_results['errors'])}")
        
        return validation_results
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return validation_results
    finally:
        sql_engine.dispose()
        mongo_client.close()

def get_sql_count(engine, table_name):
    """Get record count from SQL table"""
    with engine.connect() as conn:
        query = text(f"SELECT COUNT(*) FROM {table_name}")
        result = conn.execute(query)
        return result.scalar()

if __name__ == "__main__":
    validate_migration()
'''
        
        return {
            "filename": "validate_migration.py",
            "content": script_content,
            "description": "Comprehensive data validation script"
        }
    
    def _create_validation_plan(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """Create detailed validation plan"""
        return {
            "data_integrity_checks": [
                "Record count validation",
                "Primary key uniqueness validation",
                "Foreign key relationship validation",
                "Data type validation",
                "Constraint validation"
            ],
            "performance_checks": [
                "Query performance comparison",
                "Index effectiveness validation",
                "Memory usage analysis",
                "Response time benchmarking"
            ],
            "functional_checks": [
                "Application integration testing",
                "API endpoint validation",
                "User workflow testing",
                "Error handling validation"
            ],
            "validation_scripts": [
                "validate_migration.py",
                "validate_performance.py",
                "validate_functionality.py"
            ]
        }
    
    def _create_rollback_plan(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """Create rollback plan for migration"""
        return {
            "rollback_triggers": [
                "Data integrity failures",
                "Performance degradation",
                "Application errors",
                "User acceptance issues"
            ],
            "rollback_steps": [
                "Stop application traffic to new database",
                "Restore from backup if necessary",
                "Revert application configuration",
                "Restart services with original database",
                "Validate system functionality"
            ],
            "rollback_scripts": [
                "rollback_data.py",
                "rollback_config.py",
                "rollback_validation.py"
            ],
            "rollback_timeline": "2-4 hours",
            "data_backup_strategy": "Full backup before migration start"
        }
    
    def _estimate_timeline(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """Estimate migration timeline"""
        complexity = schema_analysis.get("migration_complexity", {})
        complexity_level = complexity.get("level", "Medium")
        
        base_days = {
            "Low": 5,
            "Medium": 10,
            "High": 20
        }
        
        estimated_days = base_days.get(complexity_level, 10)
        
        return {
            "total_duration": f"{estimated_days} days",
            "preparation": "2-3 days",
            "migration": f"{estimated_days - 4} days",
            "validation": "2-3 days",
            "factors": complexity.get("factors", [])
        }
    
    def _assess_risks(self, schema_analysis: dict, data_mapping: dict) -> dict:
        """Assess migration risks"""
        risks = []
        
        complexity = schema_analysis.get("migration_complexity", {})
        if complexity.get("level") == "High":
            risks.append({
                "risk": "High complexity migration",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Extended testing and validation phases"
            })
        
        # Check for large tables
        tables = schema_analysis.get("tables", [])
        for table in tables:
            if table.get("estimated_rows", 0) > 1000000:
                risks.append({
                    "risk": f"Large table migration: {table['name']}",
                    "impact": "Medium",
                    "probability": "High",
                    "mitigation": "Batch processing and monitoring"
                })
        
        return {
            "identified_risks": risks,
            "overall_risk_level": "Medium" if len(risks) < 3 else "High",
            "recommendations": [
                "Perform thorough testing in staging environment",
                "Implement comprehensive monitoring",
                "Prepare detailed rollback procedures",
                "Schedule migration during low-traffic periods"
            ]
        }
    
    def _estimate_duration(self, schema_analysis: dict) -> str:
        """Estimate total migration duration"""
        complexity = schema_analysis.get("migration_complexity", {})
        level = complexity.get("level", "Medium")
        
        duration_map = {
            "Low": "3-5 days",
            "Medium": "7-10 days", 
            "High": "15-20 days"
        }
        
        return duration_map.get(level, "7-10 days")
