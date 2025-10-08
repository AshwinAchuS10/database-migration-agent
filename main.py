"""
Main entry point for the SQL to NoSQL Migration Multi-Agent System

This script demonstrates the complete migration workflow using specialized agents
to analyze, plan, and execute database migration from SQL to NoSQL systems.
"""

import os
import sys
from dotenv import load_dotenv
from config import Config
from workflow import MigrationWorkflow, create_sample_sql_schema

def main():
    """Main function to run the migration workflow"""
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Validate configuration
        Config.validate_config()
        print("✅ Configuration validated successfully")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure GOOGLE_API_KEY is set in your environment or .env file")
        sys.exit(1)
    
    print("🚀 SQL to NoSQL Migration Multi-Agent System")
    print("=" * 60)
    
    # Initialize workflow
    workflow = MigrationWorkflow()
    
    # Create sample SQL schema for demonstration
    print("\n📋 Creating sample SQL schema for demonstration...")
    sample_schema = create_sample_sql_schema()
    print(f"✅ Created schema with {len(sample_schema['tables'])} tables")
    
    # Execute migration workflow
    print("\n🔄 Starting migration workflow...")
    try:
        results = workflow.execute_migration_workflow(sample_schema)
        
        print("\n🎉 Migration workflow completed successfully!")
        print("=" * 60)
        
        # Display results summary
        summary = results["migration_summary"]
        print(f"\n📊 Migration Summary:")
        print(f"   • Source tables: {summary['total_tables']}")
        print(f"   • Target collections: {summary['total_collections']}")
        print(f"   • Complexity: {summary['complexity_level']}")
        print(f"   • Duration: {summary['estimated_duration']}")
        print(f"   • Risk level: {summary['risk_level']}")
        
        print(f"\n📁 Generated Files ({len(results['output_files'])}):")
        for filename in sorted(results['output_files']):
            print(f"   • {filename}")
        
        print(f"\n📂 All files saved to: {Config.OUTPUT_DIR}/")
        print("\n🔍 Next Steps:")
        print("   1. Review the generated migration plan")
        print("   2. Examine the data mapping structure")
        print("   3. Check the documentation for implementation guidance")
        print("   4. Run the migration scripts in your environment")
        
    except Exception as e:
        print(f"\n❌ Error during migration workflow: {str(e)}")
        print("Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
