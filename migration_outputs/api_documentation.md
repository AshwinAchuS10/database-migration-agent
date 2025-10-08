# NoSQL Database API Documentation

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

### users Collection

**Original SQL Table:** users

#### Document Structure
```json
{
  "_id": "ObjectId (auto-generated)",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Common Operations

**Create Document:**
```python
collection = db['users']
document = {
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
result = collection.insert_one(document)
```

**Read Documents:**
```python
# Find all documents
documents = collection.find()

# Find by specific criteria
documents = collection.find({"username": "john_doe"})

# Find one document
document = collection.find_one({"_id": object_id})
```

**Update Document:**
```python
collection.update_one(
    {"_id": object_id},
    {"$set": {"field": "new_value"}}
)
```

**Delete Document:**
```python
collection.delete_one({"_id": object_id})
```

#### Indexes
- **Primary key index:** {"_id": 1}
- **Username index:** {"username": 1}
- **Email index:** {"email": 1}
