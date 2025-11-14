# User Queries Restructuring

This document outlines the restructuring of user queries to match the category package structure.

## New Structure

```
users/
├── filters/
│   ├── __init__.py
│   └── user_filter.py
├── queries/
│   ├── __init__.py
│   ├── user_queries.py (main aggregator)
│   ├── user_single.py (single user & me queries)
│   ├── user_list.py (all users with filtering)
│   ├── influencer_queries.py
│   ├── company_queries.py
│   └── README.md
```

## Files Created/Modified

### 1. **users/filters/user_filter.py** (NEW)

- Defines `UserFilter` using django-filters
- Supports filtering by: email, name, role, verification status, active status, etc.
- Includes ordering by: email, name, created_at, updated_at, is_active, role

### 2. **users/queries/user_single.py** (NEW)

- Contains `UserSingleQuery` class
- Queries:
  - `user(id: ID!)` - Get single user by relay ID
  - `me` - Get current authenticated user

### 3. **users/queries/user_list.py** (NEW)

- Contains `UserListQuery` class
- Queries:
  - `allUsers` - Get all users with pagination and filtering (admin only)
- Uses `DjangoFilterConnectionField` with `UserFilter`
- Automatically excludes staff users
- Requires admin authentication

### 4. **users/queries/user_queries.py** (MODIFIED)

- Now inherits from `UserSingleQuery` and `UserListQuery`
- Simplified to aggregate all user queries
- Matches the category pattern

### 5. **users/queries/**init**.py** (MODIFIED)

- Updated to export all query classes
- Includes new `UserSingleQuery` and `UserListQuery`

### 6. **users/queries/README.md** (NEW)

- Documentation for user queries structure and usage

## Benefits

1. **Modular Structure**: Each query type is in its own file
2. **Consistent with Category App**: Follows the same pattern as the category package
3. **Better Filtering**: Uses django-filters for more powerful filtering capabilities
4. **Easy to Maintain**: Separated concerns make it easier to modify individual queries
5. **Scalable**: Easy to add more query types in the future

## Usage

The usage remains the same in your main schema:

```python
from users.queries import UserQueries

class Query(UserQueries, graphene.ObjectType):
    pass
```

## GraphQL Query Examples

### Get current user

```graphql
query {
  me {
    id
    email
    name
    role
  }
}
```

### Get all users with filtering

```graphql
query {
  allUsers(
    email_Icontains: "example"
    role: "INFLUENCER"
    isActive: true
    first: 10
  ) {
    totalCount
    edges {
      node {
        id
        email
        name
        role
      }
    }
  }
}
```

### Get single user by ID

```graphql
query {
  user(id: "VXNlck5vZGU6MQ==") {
    id
    email
    name
    role
  }
}
```
