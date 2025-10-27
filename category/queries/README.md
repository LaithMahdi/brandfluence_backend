# Category Queries

This folder contains all GraphQL queries for the Category model, organized by functionality.

## Structure

```
queries/
├── __init__.py              # Package initialization and imports
├── category_queries.py      # Main queries collection
├── category_single.py       # Single category queries
└── category_list.py         # List category queries
```

## Available Queries

### Single Item Queries

- **category**: Get a single category by ID

### List Queries

- **all_categories**: Get all categories with filtering and pagination
- **active_categories**: Get only active categories with filtering and pagination

### Count Queries

- **category_count**: Get total count of categories
- **active_category_count**: Get count of active categories

## Usage

Import the queries collection in your schema:

```python
from category.queries import CategoryQueries

class Query(CategoryQueries, graphene.ObjectType):
    pass
```

## Filtering

All list queries support comprehensive filtering through the CategoryFilter:

```graphql
query {
  allCategories(
    nameContains: "example"
    isActive: true
    createdAfter: "2023-01-01"
    orderBy: "-created"
  ) {
    edges {
      node {
        id
        name
        description
        isActive
        ageInDays
        isRecentlyCreated
      }
    }
  }
}
```

## Pagination

All list queries use Relay-style pagination:

```graphql
query {
  allCategories(first: 10, after: "cursor") {
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
    edges {
      cursor
      node {
        id
        name
      }
    }
  }
}
```

## Extending Queries

To add new queries:

1. Create methods in the appropriate query class
2. Or create a new query file and inherit from it in `category_queries.py`

## Performance

Queries are optimized with:

- `select_related()` and `prefetch_related()` optimizations
- Efficient filtering at the database level
- Relay-style pagination for large datasets
