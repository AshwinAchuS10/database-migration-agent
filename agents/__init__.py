"""
Multi-Agent System for SQL to NoSQL Database Migration

This package contains specialized agents for database migration:
- SchemaAnalyzerAgent: Analyzes SQL schema and relationships
- DataMapperAgent: Maps SQL data structures to NoSQL document structures
- MigrationPlannerAgent: Creates detailed migration strategy and scripts
- DocumentationAgent: Generates comprehensive migration documentation
"""

from .schema_analyzer_agent import SchemaAnalyzerAgent
from .data_mapper_agent import DataMapperAgent
from .migration_planner_agent import MigrationPlannerAgent
from .documentation_agent import DocumentationAgent

__all__ = [
    'SchemaAnalyzerAgent',
    'DataMapperAgent', 
    'MigrationPlannerAgent',
    'DocumentationAgent'
]
