# Category App - Simple Guide for Beginners

This is a GraphQL API for managing categories. Here's what each file does:

## 📁 Project Structure

```
category/
├── models.py              # Database table definition (what data to store)
├── schema.py              # Main GraphQL entry point (combines queries & mutations)
├── category_node.py       # Defines what data can be queried
├── category_filter.py     # Defines how to search/filter categories
├── admin.py               # Django admin interface setup
├── queries/               # Folder for all GraphQL queries (read data)
│   ├── category_single.py # Get one category by ID
│   ├── category_list.py   # Get all categories with pagination
│   └── category_queries.py # Combines all queries
└── mutations/             # Folder for all GraphQL mutations (write data)
    ├── create_category.py # Create new category
    ├── update_category.py # Update existing category
    ├── delete_category.py # Delete category
    ├── patch_category.py  # Update specific fields only
    ├── batch_create_category.py # Create multiple categories
    └── category_mutations.py # Combines all mutations
```

## 🔍 GraphQL Basics

### Queries (Read Data)

**Get all categories:**

```graphql
query {
  allCategories {
    edges {
      node {
        id
        name
        description
        isActive
      }
    }
    totalCount
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
  }
}
```

**Get one category:**

```graphql
query {
  category(id: "Q2F0ZWdvcnlOb2RlOjE=") {
    id
    name
    description
    isActive
    ageInDays
    formattedCreated
  }
}
```

### Mutations (Write Data)

**Create a category:**

```graphql
mutation {
  createCategory(
    input: {
      name: "Technology"
      description: "Tech categories"
      isActive: true
    }
  ) {
    category {
      id
      name
    }
  }
}
```

**Update a category:**

```graphql
mutation {
  updateCategory(input: { id: "Q2F0ZWdvcnlOb2RlOjE=", name: "Updated Name" }) {
    category {
      id
      name
    }
  }
}
```

**Delete a category:**

```graphql
mutation {
  deleteCategory(input: { id: "Q2F0ZWdvcnlOb2RlOjE=" }) {
    found
    deletedId
  }
}
```

## 🎯 Key Files Explained

### models.py

- Defines the Category database table
- Fields: name, description, is_active, created, modified

### category_node.py

- Tells GraphQL what Category data can be accessed
- Adds extra fields like `ageInDays` and `formattedCreated`
- `CategoryConnection` adds `totalCount` to query results

### queries/

All files for **reading** data:

- `category_single.py` - Get one category
- `category_list.py` - Get all categories with pagination
- Queries return data, don't change anything

### mutations/

All files for **writing** data:

- `create_category.py` - Add new category
- `update_category.py` - Change all fields
- `patch_category.py` - Change only specific fields
- `delete_category.py` - Remove category
- Mutations create, update, or delete data

### admin.py

- Django admin panel customization
- Makes it easy to manage categories in the browser
- Access at: `/admin/category/category/`

## 🚀 Quick Start

1. **Access GraphQL Playground:** Go to `/graphql/` in your browser
2. **Try a query:** Copy any query from above
3. **Test a mutation:** Try creating a category
4. **Check admin panel:** Go to `/admin/` to see your data

## 💡 Tips for Beginners

- **Query** = Read data (SELECT in SQL)
- **Mutation** = Write data (INSERT/UPDATE/DELETE in SQL)
- **Node** = A single item (one category)
- **Connection** = A list of items with pagination
- **totalCount** = Total number of items
- **edges** = The actual list of items
- **pageInfo** = Information about pagination

## 🎓 Learning Path

1. Start with simple queries (get all categories)
2. Try mutations (create a category)
3. Learn about filtering (search by name)
4. Understand pagination (first/after)
5. Explore custom fields (ageInDays, etc.)

## 📚 Need Help?

- Check `DOCUMENTATION.md` for detailed information
- Look at the code comments
- Test queries in GraphiQL at `/graphql/`
- Each file has a simple docstring at the top
