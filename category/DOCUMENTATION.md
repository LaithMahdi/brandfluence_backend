# Category App Documentation

This document provides comprehensive information about the Category app in the Brandfluence project.

## Overview

The Category app manages category data with a professional, organized structure that separates concerns and follows Django best practices.

## Architecture

### Folder Structure

```
category/
├── __init__.py
├── admin.py                    # Enhanced Django admin configuration
├── apps.py                     # App configuration
├── models.py                   # Data models
├── views.py                    # Traditional Django views (if needed)
├── tests.py                    # Unit tests
├── schema.py                   # Main GraphQL schema
├── category_filter.py          # Enhanced filtering options
├── category_node.py            # Enhanced GraphQL node definition
├── migrations/                 # Database migrations
├── mutations/                  # GraphQL mutations (organized)
│   ├── __init__.py
│   ├── README.md
│   ├── category_mutations.py
│   ├── create_category.py
│   ├── update_category.py
│   ├── delete_category.py
│   ├── patch_category.py
│   └── batch_create_category.py
└── queries/                    # GraphQL queries (organized)
    ├── __init__.py
    ├── README.md
    ├── category_queries.py
    ├── category_single.py
    └── category_list.py
```

## Models

### Category Model

- **Fields**:

  - `name`: CharField(max_length=255) - Category name
  - `description`: TextField - Optional description
  - `is_active`: BooleanField - Active status
  - `created`: DateTimeField - Auto-created timestamp
  - `modified`: DateTimeField - Auto-updated timestamp

- **Features**:
  - Inherits from TimeStampedModel for automatic timestamp management
  - Clean string representation
  - Proper verbose names for admin interface

## GraphQL API

### Queries

#### Single Category

```graphql
query {
  category(id: "Q2F0ZWdvcnlOb2RlOjE=") {
    id
    name
    description
    isActive
    ageInDays
    isRecentlyCreated
    formattedCreated
  }
}
```

#### Category List with Filtering

```graphql
query {
  allCategories(
    nameContains: "tech"
    isActive: true
    createdAfter: "2023-01-01"
    orderBy: "-created"
    first: 10
  ) {
    edges {
      node {
        id
        name
        description
        isActive
        ageInDays
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
  }
}
```

#### Category Counts

```graphql
query {
  categoryCount
  activeCategoryCount
}
```

### Mutations

#### Create Category

```graphql
mutation {
  createCategory(
    input: {
      name: "Technology"
      description: "Tech-related categories"
      isActive: true
    }
  ) {
    category {
      id
      name
      description
    }
    errors {
      field
      messages
    }
  }
}
```

#### Update Category

```graphql
mutation {
  updateCategory(
    input: {
      id: "Q2F0ZWdvcnlOb2RlOjE="
      name: "Updated Technology"
      description: "Updated description"
    }
  ) {
    category {
      id
      name
      description
    }
    errors {
      field
      messages
    }
  }
}
```

#### Batch Operations

```graphql
mutation {
  batchCreateCategories(
    input: {
      categories: [
        { name: "Category 1", isActive: true }
        { name: "Category 2", isActive: false }
      ]
    }
  ) {
    categories {
      id
      name
    }
    errors {
      field
      messages
    }
  }
}
```

## Django Admin

### Features

- **Enhanced List View**:

  - Searchable by name and description
  - Filterable by status and dates
  - Custom display columns with formatting
  - Action buttons for quick operations
  - Pagination controls

- **Form Configuration**:

  - Organized fieldsets
  - Read-only timestamp fields in edit mode
  - Responsive design

- **Custom Actions**:
  - Bulk activate/deactivate categories
  - Custom admin styling

### Admin URL

Access the admin interface at: `/admin/category/category/`

## Filtering Options

The CategoryFilter provides comprehensive filtering:

- **Text Filters**:

  - `name_contains`: Case-insensitive name search
  - `description_contains`: Case-insensitive description search

- **Status Filters**:

  - `is_active`: Filter by active status

- **Date Filters**:

  - `created_after`: Categories created after date
  - `created_before`: Categories created before date
  - `modified_after`: Categories modified after date
  - `modified_before`: Categories modified before date

- **Ordering**:
  - Sort by name, creation date, modification date, or active status

## Custom Node Fields

The CategoryNode includes additional computed fields:

- `ageInDays`: Number of days since creation
- `isRecentlyCreated`: Boolean indicating if created in last 7 days
- `isRecentlyModified`: Boolean indicating if modified in last 7 days
- `formattedCreated`: Formatted creation date string
- `formattedModified`: Formatted modification date string

## Security & Permissions

### Mutation Permissions

Each mutation includes a `get_permissions` hook for custom authorization:

```python
@classmethod
def get_permissions(cls, root, info, input):
    # Implement your permission logic
    if not info.context.user.is_authenticated:
        return ['You must be logged in']
    return []
```

### Query Permissions

Implement custom query permissions by overriding resolvers:

```python
def resolve_all_categories(self, info, **kwargs):
    if not info.context.user.has_perm('category.view_category'):
        raise PermissionDenied("You don't have permission to view categories")
    return Category.objects.all()
```

## Testing

### Unit Tests

Create comprehensive tests in `tests.py`:

```python
from django.test import TestCase
from .models import Category

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.assertEqual(category.name, "Test Category")
        self.assertTrue(category.is_active)
```

### GraphQL Tests

Test GraphQL operations:

```python
from graphene.test import Client
from .schema import schema

class CategoryGraphQLTest(TestCase):
    def test_category_query(self):
        client = Client(schema)
        executed = client.execute('''
            query {
                allCategories {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
        ''')
        self.assertIsNone(executed.get('errors'))
```

## Performance Considerations

### Database Optimization

- Use `select_related()` and `prefetch_related()` in querysets
- Add database indexes for frequently filtered fields
- Consider pagination for large datasets

### GraphQL Optimization

- Utilize `graphene-django-optimizer` for N+1 query prevention
- Implement query complexity analysis for production
- Use DataLoader pattern for related field fetching

## Deployment

### Environment Variables

Consider using environment variables for:

- Database connection settings
- GraphQL JWT secret keys
- Debug mode settings

### Static Files

Ensure custom admin CSS/JS files are properly collected:

```bash
python manage.py collectstatic
```

## Extensions

### Adding New Features

1. **New Model Fields**: Update migrations and GraphQL nodes
2. **Custom Mutations**: Create new files in the mutations folder
3. **Advanced Filtering**: Extend CategoryFilter with new options
4. **Custom Admin Views**: Override admin templates and add custom actions

### Integration with Other Apps

The Category app is designed to be easily integrated with other apps:

```python
# In other app models
from category.models import Category

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # ... other fields
```

## Troubleshooting

### Common Issues

1. **Migration Errors**: Ensure all dependencies are installed
2. **GraphQL Errors**: Check schema registration in main schema
3. **Admin Issues**: Verify model registration and permissions
4. **Performance Issues**: Review query optimization and indexing

### Debug Mode

Enable Django debug mode for development:

```python
DEBUG = True
```

For GraphQL debugging, use GraphiQL interface at `/graphql/`
