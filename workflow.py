"""
Multi-Agent Workflow for SQL to NoSQL Database Migration

This module orchestrates the collaboration between specialized agents to perform
comprehensive database migration from SQL to NoSQL systems.
"""

from crewai import Crew, Process, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config
from agents import (
    SchemaAnalyzerAgent,
    DataMapperAgent, 
    MigrationPlannerAgent,
    DocumentationAgent
)
import json
import os
from datetime import datetime

class MigrationWorkflow:
    """Orchestrates the multi-agent migration workflow"""
    
    def __init__(self):
        """Initialize the migration workflow with all agents"""
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.TEMPERATURE
        )
        
        # Initialize all agents
        self.schema_analyzer = SchemaAnalyzerAgent()
        self.data_mapper = DataMapperAgent()
        self.migration_planner = MigrationPlannerAgent()
        self.documentation_agent = DocumentationAgent()
        
        # Create output directory
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    def execute_migration_workflow(self, sql_schema_info: dict) -> dict:
        """
        Execute the complete migration workflow
        
        Args:
            sql_schema_info: SQL database schema information
            
        Returns:
            Dictionary containing all migration results
        """
        print("🚀 Starting SQL to NoSQL Migration Workflow")
        print("=" * 50)
        
        # Phase 1: Schema Analysis
        print("\n📊 Phase 1: Analyzing SQL Schema...")
        schema_analysis = self.schema_analyzer.analyze_schema(sql_schema_info)
        self._save_results("schema_analysis.json", schema_analysis)
        print("✅ Schema analysis completed")
        
        # Phase 2: Data Mapping
        print("\n🗺️ Phase 2: Mapping SQL to NoSQL Structure...")
        data_mapping = self.data_mapper.map_sql_to_nosql(schema_analysis)
        self._save_results("data_mapping.json", data_mapping)
        print("✅ Data mapping completed")
        
        # Phase 3: Migration Planning
        print("\n📋 Phase 3: Creating Migration Plan...")
        migration_plan = self.migration_planner.create_migration_plan(schema_analysis, data_mapping)
        self._save_results("migration_plan.json", migration_plan)
        print("✅ Migration plan completed")
        
        # Phase 4: Documentation Generation
        print("\n📚 Phase 4: Generating Documentation...")
        documentation = self.documentation_agent.generate_documentation(
            schema_analysis, data_mapping, migration_plan
        )
        self._save_documentation(documentation)
        print("✅ Documentation completed")
        
        # Compile final results
        final_results = {
            "migration_summary": self._create_migration_summary(schema_analysis, data_mapping, migration_plan),
            "schema_analysis": schema_analysis,
            "data_mapping": data_mapping,
            "migration_plan": migration_plan,
            "documentation": documentation,
            "execution_timestamp": datetime.now().isoformat(),
            "output_files": self._list_output_files()
        }
        
        print("\n🎉 Migration Workflow Completed Successfully!")
        print("=" * 50)
        self._print_summary(final_results)
        
        return final_results
    
    def _save_results(self, filename: str, data: dict):
        """Save results to JSON file"""
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _save_documentation(self, documentation: dict):
        """Save documentation files"""
        for doc_type, content in documentation.items():
            filename = f"{doc_type}.md"
            filepath = os.path.join(Config.OUTPUT_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(content)
    
    def _create_migration_summary(self, schema_analysis: dict, data_mapping: dict, migration_plan: dict) -> dict:
        """Create high-level migration summary"""
        return {
            "total_tables": len(schema_analysis.get("tables", [])),
            "total_collections": len(data_mapping.get("collections", [])),
            "complexity_level": schema_analysis.get("migration_complexity", {}).get("level", "Unknown"),
            "estimated_duration": migration_plan.get("timeline", {}).get("total_duration", "Unknown"),
            "migration_phases": len(migration_plan.get("phases", [])),
            "risk_level": migration_plan.get("risk_assessment", {}).get("overall_risk_level", "Unknown")
        }
    
    def _list_output_files(self) -> list:
        """List all generated output files"""
        output_files = []
        if os.path.exists(Config.OUTPUT_DIR):
            for filename in os.listdir(Config.OUTPUT_DIR):
                if filename.endswith(('.json', '.md', '.py', '.js')):
                    output_files.append(filename)
        return output_files
    
    def _print_summary(self, results: dict):
        """Print migration summary"""
        summary = results["migration_summary"]
        
        print(f"\n📈 Migration Summary:")
        print(f"   • Tables to migrate: {summary['total_tables']}")
        print(f"   • Collections to create: {summary['total_collections']}")
        print(f"   • Complexity level: {summary['complexity_level']}")
        print(f"   • Estimated duration: {summary['estimated_duration']}")
        print(f"   • Migration phases: {summary['migration_phases']}")
        print(f"   • Risk level: {summary['risk_level']}")
        
        print(f"\n📁 Generated Files:")
        for filename in results["output_files"]:
            print(f"   • {filename}")
        
        print(f"\n📂 Output directory: {Config.OUTPUT_DIR}")

def create_sample_sql_schema() -> dict:
    """Create sample SQL schema for demonstration"""
    return {
        "database_name": "ecommerce_db",
        "tables": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "INT", "is_primary_key": True, "nullable": False, "is_unique": True},
                    {"name": "username", "type": "VARCHAR(50)", "nullable": False, "is_unique": True},
                    {"name": "email", "type": "VARCHAR(100)", "nullable": False, "is_unique": True},
                    {"name": "first_name", "type": "VARCHAR(50)", "nullable": False},
                    {"name": "last_name", "type": "VARCHAR(50)", "nullable": False},
                    {"name": "created_at", "type": "TIMESTAMP", "nullable": False},
                    {"name": "updated_at", "type": "TIMESTAMP", "nullable": True}
                ]
            },
            {
                "name": "products",
                "columns": [
                    {"name": "id", "type": "INT", "is_primary_key": True, "nullable": False, "is_unique": True},
                    {"name": "name", "type": "VARCHAR(100)", "nullable": False},
                    {"name": "description", "type": "TEXT", "nullable": True},
                    {"name": "price", "type": "DECIMAL(10,2)", "nullable": False},
                    {"name": "category_id", "type": "INT", "nullable": False, "is_foreign_key": True, "references_table": "categories", "references_column": "id"},
                    {"name": "stock_quantity", "type": "INT", "nullable": False},
                    {"name": "created_at", "type": "TIMESTAMP", "nullable": False}
                ]
            },
            {
                "name": "categories",
                "columns": [
                    {"name": "id", "type": "INT", "is_primary_key": True, "nullable": False, "is_unique": True},
                    {"name": "name", "type": "VARCHAR(50)", "nullable": False, "is_unique": True},
                    {"name": "description", "type": "TEXT", "nullable": True},
                    {"name": "parent_id", "type": "INT", "nullable": True, "is_foreign_key": True, "references_table": "categories", "references_column": "id"}
                ]
            },
            {
                "name": "orders",
                "columns": [
                    {"name": "id", "type": "INT", "is_primary_key": True, "nullable": False, "is_unique": True},
                    {"name": "user_id", "type": "INT", "nullable": False, "is_foreign_key": True, "references_table": "users", "references_column": "id"},
                    {"name": "order_date", "type": "TIMESTAMP", "nullable": False},
                    {"name": "total_amount", "type": "DECIMAL(10,2)", "nullable": False},
                    {"name": "status", "type": "VARCHAR(20)", "nullable": False},
                    {"name": "shipping_address", "type": "TEXT", "nullable": False}
                ]
            },
            {
                "name": "order_items",
                "columns": [
                    {"name": "id", "type": "INT", "is_primary_key": True, "nullable": False, "is_unique": True},
                    {"name": "order_id", "type": "INT", "nullable": False, "is_foreign_key": True, "references_table": "orders", "references_column": "id"},
                    {"name": "product_id", "type": "INT", "nullable": False, "is_foreign_key": True, "references_table": "products", "references_column": "id"},
                    {"name": "quantity", "type": "INT", "nullable": False},
                    {"name": "unit_price", "type": "DECIMAL(10,2)", "nullable": False}
                ]
            }
        ]
    }

if __name__ == "__main__":
    # Example usage
    workflow = MigrationWorkflow()
    
    # Create sample schema
    sample_schema = create_sample_sql_schema()
    
    # Execute migration workflow
    results = workflow.execute_migration_workflow(sample_schema)
    
    print(f"\n🎯 Migration workflow completed!")
    print(f"📁 Check the '{Config.OUTPUT_DIR}' directory for all generated files.")
