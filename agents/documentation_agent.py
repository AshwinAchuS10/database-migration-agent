"""
Documentation Agent for SQL to NoSQL Migration

This agent generates comprehensive documentation including migration guides,
API documentation, and user manuals for the migrated system.
"""

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config
from datetime import datetime
import json

class DocumentationAgent:
    """Agent responsible for generating comprehensive migration documentation"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.TEMPERATURE
        )
        
        self.agent = Agent(
            role="Technical Documentation Specialist",
            goal="Create comprehensive, clear, and actionable documentation for the SQL to NoSQL migration process and resulting system",
            backstory="""You are a senior technical writer with 15+ years of experience documenting complex database 
            migrations and system architectures. You excel at translating technical concepts into clear, 
            actionable documentation that enables both technical and non-technical stakeholders to understand 
            and work with migrated systems. Your documentation is known for its clarity, completeness, 
            and practical value.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_documentation(self, schema_analysis: dict, data_mapping: dict, migration_plan: dict) -> dict:
        """
        Generate comprehensive documentation for the migration
        
        Args:
            schema_analysis: Output from SchemaAnalyzerAgent
            data_mapping: Output from DataMapperAgent  
            migration_plan: Output from MigrationPlannerAgent
            
        Returns:
            Dictionary with generated documentation
        """
        documentation = {
            "migration_guide": self._create_migration_guide(schema_analysis, data_mapping, migration_plan),
            "api_documentation": self._create_api_documentation(data_mapping),
            "data_model_documentation": self._create_data_model_documentation(data_mapping),
            "troubleshooting_guide": self._create_troubleshooting_guide(migration_plan),
            "user_manual": self._create_user_manual(data_mapping),
            "technical_specifications": self._create_technical_specifications(schema_analysis, data_mapping)
        }
        
        return documentation
    
    def _create_migration_guide(self, schema_analysis: dict, data_mapping: dict, migration_plan: dict) -> str:
        """Create comprehensive migration guide"""
        guide = f"""# SQL to NoSQL Database Migration Guide

## Overview

This document provides a comprehensive guide for migrating from SQL to NoSQL database architecture. The migration involves transforming relational data structures into document-based collections optimized for MongoDB.

**Migration Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source Database:** SQL Database
**Target Database:** MongoDB
**Complexity Level:** {schema_analysis.get('migration_complexity', {}).get('level', 'Medium')}

## Migration Summary

- **Total Tables:** {len(schema_analysis.get('tables', []))}
- **Total Collections:** {len(data_mapping.get('collections', []))}
- **Estimated Duration:** {migration_plan.get('timeline', {}).get('total_duration', 'Unknown')}
- **Migration Strategy:** Phased approach with validation

## Pre-Migration Checklist

### 1. Environment Preparation

- [ ] Set up MongoDB cluster
- [ ] Configure network connectivity
- [ ] Install required tools and drivers
- [ ] Create backup of source database
- [ ] Set up monitoring and logging

### 2. Data Analysis

- [ ] Analyze data volume and growth patterns
- [ ] Identify data access patterns
- [ ] Review data quality and integrity
- [ ] Document business rules and constraints

## Migration Phases

"""
        
        # Add phase details
        phases = migration_plan.get('phases', [])
        for phase in phases:
            guide += f"""### Phase {phase['phase']}: {phase['name']}

**Duration:** {phase['duration']}
**Description:** {phase['description']}

**Tasks:**
"""
            for task in phase['tasks']:
                guide += f"- {task}\n"
            guide += "\n"
        
        guide += """## Post-Migration Validation

### Data Integrity Checks
- Record count validation
- Data type validation
- Relationship integrity validation
- Constraint validation

### Performance Validation
- Query performance testing
- Index effectiveness validation
- Load testing
- Response time benchmarking

## Rollback Procedures

In case of migration issues, follow these rollback steps:

1. **Immediate Actions**
   - Stop application traffic to new database
   - Alert technical team
   - Assess impact and severity

2. **Data Rollback**
   - Restore from pre-migration backup
   - Validate data integrity
   - Restart services with original database

3. **Application Rollback**
   - Revert application configuration
   - Update connection strings
   - Restart application services

## Support and Maintenance

### Monitoring
- Set up database monitoring
- Configure alerting for critical issues
- Monitor performance metrics

### Documentation Updates
- Update API documentation
- Revise user manuals
- Update system architecture diagrams

## Contact Information

For technical support during migration:
- **Migration Team Lead:** [Contact Information]
- **Database Administrator:** [Contact Information]
- **Emergency Contact:** [Contact Information]
"""
        
        return guide
    
    def _create_api_documentation(self, data_mapping: dict) -> str:
        """Create API documentation for the new NoSQL system"""
        api_doc = """# NoSQL Database API Documentation

## Overview

This document describes the API endpoints and data access patterns for the migrated NoSQL database system.

## Database Connection

```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['migrated_db']
```

## Collection APIs

"""
        
        collections = data_mapping.get('collections', [])
        for collection in collections:
            collection_name = collection['nosql_collection']
            sql_table = collection['sql_table']
            
            api_doc += f"""### {collection_name} Collection

**Original SQL Table:** {sql_table}

#### Document Structure
```json
{json.dumps(collection.get('document_structure', {}), indent=2)}
```

#### Common Operations

**Create Document:**
```python
collection = db['{collection_name}']
document = {{
    # Document fields based on mapping
}}
result = collection.insert_one(document)
```

**Read Documents:**
```python
# Find all documents
documents = collection.find()

# Find by specific criteria
documents = collection.find({{"field": "value"}})

# Find one document
document = collection.find_one({{"_id": object_id}})
```

**Update Document:**
```python
collection.update_one(
    {{"_id": object_id}},
    {{"$set": {{"field": "new_value"}}}}
)
```

**Delete Document:**
```python
collection.delete_one({{"_id": object_id}})
```

#### Indexes
"""
            
            # Add index information
            indexes = data_mapping.get('indexes', [])
            collection_indexes = [idx for idx in indexes if idx.get('collection') == collection_name]
            
            for index in collection_indexes:
                api_doc += f"- **{index.get('description', 'Index')}:** {index.get('index', {})}\n"
            
            api_doc += "\n"
        
        return api_doc
    
    def _create_data_model_documentation(self, data_mapping: dict) -> str:
        """Create data model documentation"""
        model_doc = """# NoSQL Data Model Documentation

## Overview

This document describes the data model for the migrated NoSQL database system, including collection structures, relationships, and access patterns.

## Collection Mappings

"""
        
        collections = data_mapping.get('collections', [])
        for collection in collections:
            model_doc += f"""### {collection['nosql_collection']} Collection

**Source Table:** {collection['sql_table']}

**Document Structure:**
```json
{json.dumps(collection.get('document_structure', {}), indent=2)}
```

**Field Mappings:**
"""
            
            for field in collection.get('field_mappings', []):
                model_doc += f"- **{field['sql_column']}** → **{field['nosql_field']}** ({field['type']})\n"
            
            model_doc += f"""
**Embedding Strategy:** {collection.get('embedding_strategy', 'reference')}

**Relationships:**
"""
            
            for rel in collection.get('relationships', []):
                model_doc += f"- {rel.get('description', 'Relationship')}\n"
            
            model_doc += "\n"
        
        # Add relationship documentation
        relationships = data_mapping.get('relationships', [])
        if relationships:
            model_doc += """## Relationship Strategies

"""
            for rel in relationships:
                model_doc += f"""### {rel['from_collection']} → {rel['to_collection']}

**Type:** {rel['relationship_type']}
**Strategy:** {rel['strategy']}
**Implementation:** {rel['implementation']['description']}

"""
        
        return model_doc
    
    def _create_troubleshooting_guide(self, migration_plan: dict) -> str:
        """Create troubleshooting guide"""
        troubleshooting = """# Migration Troubleshooting Guide

## Common Issues and Solutions

### 1. Data Migration Issues

**Problem:** Record count mismatch between SQL and MongoDB
**Symptoms:**
- Validation scripts report different record counts
- Application shows missing data

**Solutions:**
1. Check for data type conversion issues
2. Verify filter conditions in migration scripts
3. Check for NULL value handling
4. Review transaction boundaries

**Prevention:**
- Test migration scripts with sample data
- Implement comprehensive logging
- Use batch processing for large datasets

### 2. Performance Issues

**Problem:** Slow query performance in MongoDB
**Symptoms:**
- High response times
- CPU/memory usage spikes
- Timeout errors

**Solutions:**
1. Review and optimize indexes
2. Check query patterns and structure
3. Consider denormalization for frequently accessed data
4. Implement connection pooling

**Prevention:**
- Design indexes based on query patterns
- Monitor performance during migration
- Load test the new system

### 3. Application Integration Issues

**Problem:** Application errors after migration
**Symptoms:**
- Connection errors
- Data format issues
- Functionality failures

**Solutions:**
1. Update connection strings and drivers
2. Modify data access code for NoSQL patterns
3. Update data validation logic
4. Test all application workflows

**Prevention:**
- Comprehensive application testing
- Gradual rollout strategy
- Maintain backward compatibility where possible

### 4. Data Integrity Issues

**Problem:** Data corruption or inconsistency
**Symptoms:**
- Validation failures
- Business logic errors
- User-reported data issues

**Solutions:**
1. Run data validation scripts
2. Check for constraint violations
3. Verify relationship integrity
4. Review data transformation logic

**Prevention:**
- Implement comprehensive validation
- Use transaction boundaries appropriately
- Maintain data quality standards

## Emergency Procedures

### Immediate Response
1. **Assess Impact:** Determine scope and severity
2. **Notify Team:** Alert technical team and stakeholders
3. **Document Issue:** Record symptoms and timeline
4. **Implement Workaround:** If possible, implement temporary solution

### Escalation Procedures
1. **Level 1:** Technical team investigation
2. **Level 2:** Senior technical team involvement
3. **Level 3:** Vendor support or external consultation
4. **Level 4:** Executive escalation

### Rollback Decision Criteria
Consider rollback if:
- Data integrity cannot be maintained
- Performance degradation is severe
- Application functionality is compromised
- User experience is significantly impacted

## Monitoring and Alerting

### Key Metrics to Monitor
- Database connection count
- Query response times
- Error rates
- Data validation results
- Application performance metrics

### Alert Thresholds
- Response time > 2 seconds
- Error rate > 1%
- Connection failures > 5%
- Data validation failures

## Support Contacts

- **Technical Lead:** [Contact Information]
- **Database Administrator:** [Contact Information]
- **Application Support:** [Contact Information]
- **Emergency Hotline:** [Contact Information]
"""
        
        return troubleshooting
    
    def _create_user_manual(self, data_mapping: dict) -> str:
        """Create user manual for the new system"""
        user_manual = """# NoSQL Database User Manual

## Introduction

This manual provides guidance for users working with the migrated NoSQL database system. The system has been migrated from a traditional SQL database to MongoDB for improved performance and scalability.

## Getting Started

### Prerequisites
- MongoDB client tools installed
- Database connection credentials
- Basic understanding of document databases

### Connection Information
- **Database Host:** [Host Information]
- **Database Name:** migrated_db
- **Authentication:** [Authentication Details]

## Working with Collections

### Understanding Collections

Collections in MongoDB are similar to tables in SQL databases, but they store documents (JSON-like objects) instead of rows.

### Basic Operations

#### Viewing Data
```javascript
// List all collections
show collections

// View documents in a collection
db.collection_name.find()

// Count documents
db.collection_name.count()
```

#### Searching Data
```javascript
// Find specific documents
db.collection_name.find({field: "value"})

// Find with multiple criteria
db.collection_name.find({field1: "value1", field2: "value2"})

// Find with conditions
db.collection_name.find({age: {$gte: 18}})
```

#### Modifying Data
```javascript
// Insert new document
db.collection_name.insertOne({field: "value"})

// Update document
db.collection_name.updateOne(
    {_id: ObjectId("...")},
    {$set: {field: "new_value"}}
)

// Delete document
db.collection_name.deleteOne({_id: ObjectId("...")})
```

## Collection-Specific Guidance

"""
        
        collections = data_mapping.get('collections', [])
        for collection in collections:
            collection_name = collection['nosql_collection']
            user_manual += f"""### {collection_name} Collection

**Purpose:** Migrated from {collection['sql_table']} table

**Key Fields:**
"""
            
            for field in collection.get('field_mappings', [])[:5]:  # Show first 5 fields
                user_manual += f"- **{field['nosql_field']}:** {field['type']}\n"
            
            user_manual += f"""
**Common Queries:**
```javascript
// Find all documents
db.{collection_name}.find()

// Find by specific field
db.{collection_name}.find({{field_name: "value"}})
```

"""
        
        user_manual += """## Best Practices

### Query Optimization
- Use indexes for frequently queried fields
- Limit result sets with projection
- Use appropriate query operators

### Data Management
- Regular backups
- Monitor collection sizes
- Clean up old or unnecessary data

### Security
- Use authentication and authorization
- Encrypt sensitive data
- Regular security audits

## Troubleshooting

### Common Issues
1. **Connection Problems:** Check network connectivity and credentials
2. **Query Performance:** Review indexes and query structure
3. **Data Format Issues:** Verify document structure and field types

### Getting Help
- Check system documentation
- Contact database administrator
- Review error logs and monitoring

## Resources

- MongoDB Official Documentation
- Database Migration Guide
- API Documentation
- Troubleshooting Guide
"""
        
        return user_manual
    
    def _create_technical_specifications(self, schema_analysis: dict, data_mapping: dict) -> str:
        """Create technical specifications document"""
        tech_specs = f"""# Technical Specifications

## System Overview

**Migration Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source System:** SQL Database
**Target System:** MongoDB
**Migration Complexity:** {schema_analysis.get('migration_complexity', {}).get('level', 'Medium')}

## Database Specifications

### Source Database
- **Type:** SQL Database
- **Tables:** {len(schema_analysis.get('tables', []))}
- **Relationships:** {len(schema_analysis.get('relationships', []))}
- **Complexity Factors:** {', '.join(schema_analysis.get('migration_complexity', {}).get('factors', []))}

### Target Database
- **Type:** MongoDB
- **Collections:** {len(data_mapping.get('collections', []))}
- **Indexes:** {len(data_mapping.get('indexes', []))}
- **Embedding Strategies:** {len(data_mapping.get('embedding_strategies', []))}

## Performance Specifications

### Expected Performance Improvements
- **Query Response Time:** 30-50% improvement
- **Concurrent Users:** 2-3x increase
- **Data Insertion:** 40-60% improvement
- **Complex Queries:** 20-40% improvement

### Resource Requirements
- **Memory:** Minimum 8GB RAM
- **Storage:** 1.5x source database size
- **CPU:** 4+ cores recommended
- **Network:** High-bandwidth connection

## Security Specifications

### Authentication
- MongoDB authentication enabled
- Role-based access control
- SSL/TLS encryption
- Network security protocols

### Data Protection
- Encryption at rest
- Encryption in transit
- Regular security audits
- Access logging and monitoring

## Monitoring Specifications

### Key Metrics
- Database performance metrics
- Query execution times
- Connection statistics
- Error rates and types

### Alerting
- Performance threshold alerts
- Error rate monitoring
- Resource usage alerts
- Security event notifications

## Backup and Recovery

### Backup Strategy
- Daily automated backups
- Point-in-time recovery capability
- Cross-region backup replication
- Regular backup validation

### Recovery Procedures
- Automated failover mechanisms
- Manual recovery procedures
- Data integrity validation
- Application reconnection protocols

## Compliance and Standards

### Data Governance
- Data retention policies
- Privacy compliance
- Audit trail maintenance
- Data quality standards

### Industry Standards
- MongoDB best practices
- Database security standards
- Performance optimization guidelines
- Documentation standards
"""
        
        return tech_specs
