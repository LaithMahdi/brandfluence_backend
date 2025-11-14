# User Queries

This package contains all GraphQL queries for the User model.

## Structure

- `user_single.py` - Query for getting a single user by ID and current user (me)
- `user_list.py` - Query for getting all users with filtering, pagination, and totalCount
- `user_queries.py` - Main queries class combining all user queries

## Usage

```python
from users.queries import UserQueries

class Query(UserQueries, graphene.ObjectType):
    pass
```

## Queries

### Single User

- `user(id: ID!)` - Get a single user by relay ID
- `me` - Get current authenticated user

### User List

- `allUsers` - Get all users with pagination and filtering (admin only)
  - Supports filtering by email, name, role, verification status, etc.
  - Returns totalCount for pagination
  - Excludes staff users by default
