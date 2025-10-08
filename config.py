"""
Configuration settings for the SQL to NoSQL Migration Multi-Agent System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the migration system"""
    
    # LLM Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = "gemini-1.5-pro"
    
    # Database Configuration
    SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING", "sqlite:///example.db")
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")
    
    # Output Configuration
    OUTPUT_DIR = "migration_outputs"
    SCHEMA_ANALYSIS_FILE = "schema_analysis.json"
    MIGRATION_PLAN_FILE = "migration_plan.json"
    DOCUMENTATION_FILE = "migration_documentation.md"
    
    # Agent Configuration
    MAX_ITERATIONS = 3
    TEMPERATURE = 0.1  # Low temperature for consistent, factual output
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return True
