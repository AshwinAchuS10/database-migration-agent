# NoSQL Database User Manual

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

### users Collection

**Purpose:** Migrated from users table

**Key Fields:**
- **username:** Unique username (string)
- **email:** Unique email address (string)
- **first_name:** User's first name (string)
- **last_name:** User's last name (string)
- **created_at:** Account creation timestamp
- **updated_at:** Last update timestamp

**Common Queries:**
```javascript
// Find all users
db.users.find()

// Find user by username
db.users.find({username: "john_doe"})

// Find users created in last month
db.users.find({created_at: {$gte: new Date("2024-01-01")}})
```

### products Collection

**Purpose:** Migrated from products table

**Key Fields:**
- **name:** Product name (string)
- **description:** Product description (string)
- **price:** Product price (decimal)
- **category_id:** Reference to category (ObjectId)
- **stock_quantity:** Available stock (integer)
- **created_at:** Product creation timestamp

**Common Queries:**
```javascript
// Find all products
db.products.find()

// Find products by category
db.products.find({category_id: ObjectId("...")})

// Find products in price range
db.products.find({price: {$gte: 10, $lte: 100}})
```

## Best Practices

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
