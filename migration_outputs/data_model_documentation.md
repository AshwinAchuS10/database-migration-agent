# NoSQL Data Model Documentation

## Overview

This document describes the data model for the migrated NoSQL database system, including collection structures, relationships, and access patterns.

## Collection Mappings

### users Collection

**Source Table:** users

**Document Structure:**
```json
{
  "_id": "ObjectId (auto-generated)",
  "username": {"type": "string", "required": true, "unique": true, "indexed": true},
  "email": {"type": "string", "required": true, "unique": true, "indexed": true},
  "first_name": {"type": "string", "required": true},
  "last_name": {"type": "string", "required": true},
  "created_at": {"type": "timestamp", "required": true},
  "updated_at": {"type": "timestamp", "required": false}
}
```

**Field Mappings:**
- **id** → **_id** (ObjectId)
- **username** → **username** (string)
- **email** → **email** (string)
- **first_name** → **first_name** (string)
- **last_name** → **last_name** (string)
- **created_at** → **created_at** (timestamp)
- **updated_at** → **updated_at** (timestamp)

**Embedding Strategy:** reference

**Relationships:**
- No direct relationships in this collection

### products Collection

**Source Table:** products

**Document Structure:**
```json
{
  "_id": "ObjectId (auto-generated)",
  "name": {"type": "string", "required": true, "indexed": true},
  "description": {"type": "string", "required": false},
  "price": {"type": "decimal128", "required": true, "indexed": true},
  "category_id": {"type": "ObjectId", "required": true, "indexed": true},
  "stock_quantity": {"type": "int32", "required": true, "indexed": true},
  "created_at": {"type": "timestamp", "required": true}
}
```

**Field Mappings:**
- **id** → **_id** (ObjectId)
- **name** → **name** (string)
- **description** → **description** (string)
- **price** → **price** (decimal128)
- **category_id** → **category_id** (ObjectId)
- **stock_quantity** → **stock_quantity** (int32)
- **created_at** → **created_at** (timestamp)

**Embedding Strategy:** reference

**Relationships:**
- Product belongs to category (many-to-one relationship)

## Relationship Strategies

### products → categories

**Type:** many_to_one
**Strategy:** reference
**Implementation:** Store reference to categories in products collection using category_id field
