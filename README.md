# Brandfluence - Django GraphQL API

A professional Django backend with GraphQL API built using Graphene-Django. This project provides a clean, organized structure for managing categories with full CRUD operations.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Using GraphQL](#using-graphql)
- [How It Works](#how-it-works)
- [Learning Resources](#learning-resources)

## ✨ Features

- **GraphQL API**: Full GraphQL implementation with queries and mutations
- **Category Management**: Complete CRUD operations for categories
- **Pagination**: Relay-style pagination with connection and edges
- **Filtering**: Advanced filtering by name, description, date, and status
- **Admin Panel**: Enhanced Django admin with custom actions and filters
- **Organized Code**: Professional folder structure for mutations and queries
- **Beginner Friendly**: Clean, well-documented code for GraphQL learners

## 🛠 Tech Stack

- **Django 5.2.7**: Python web framework
- **Graphene-Django 3.2.3**: GraphQL library for Django
- **SQLite**: Database (easy to get started)
- **Python 3.x**: Programming language

**Key Libraries:**

- `graphene-django-cud`: Create, Update, Delete mutations
- `graphene-django-optimizer`: Query optimization
- `django-filter`: Advanced filtering
- `django-cors-headers`: Cross-Origin Resource Sharing

## 📁 Project Structure

```
brandfluence/
│
├── brandfluence/           # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   └── schema.py           # Main GraphQL schema
│
├── category/               # Category app
│   ├── models.py           # Database model
│   ├── admin.py            # Admin configuration
│   ├── category_node.py    # GraphQL node definition
│   ├── category_filter.py  # Filtering options
│   ├── schema.py           # Category GraphQL schema
│   │
│   ├── queries/            # All GraphQL queries
│   │   ├── category_single.py
│   │   ├── category_list.py
│   │   └── category_queries.py
│   │
│   └── mutations/          # All GraphQL mutations
│       ├── create_category.py
│       ├── update_category.py
│       ├── delete_category.py
│       ├── patch_category.py
│       ├── batch_create_category.py
│       └── category_mutations.py
│
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher installed
- pip (Python package manager)
- Git (optional)

### Step 1: Get the Project

If using Git:

```bash
git clone https://github.com/LaithMahdi/brandfluence_backend
cd brandfluence
```

Or just download and extract the project folder.

### Step 2: Create Virtual Environment (Recommended)

**Windows (cmd):**

```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including Django, Graphene, and other dependencies.

### Step 4: Setup Database

```bash
python manage.py migrate
```

This creates the database tables.

### Step 5: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## 🏃 Running the Project

### Start the Development Server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### Access Points

- **GraphQL Playground**: `http://127.0.0.1:8000/graphql/`
  - Interactive interface to test queries and mutations
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
  - Login with superuser credentials
  - Manage categories through Django admin

## 🎮 Using GraphQL

Open the GraphQL Playground at `http://127.0.0.1:8000/graphql/`

### Example Queries

**Get All Categories:**

```graphql
query {
  allCategories(first: 10) {
    totalCount
    edges {
      node {
        id
        name
        description
        isActive
        createdAt
        modifiedAt
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```

**Get Single Category:**

```graphql
query {
  category(id: "Q2F0ZWdvcnlOb2RlOjE=") {
    id
    name
    description
    isActive
  }
}
```

**Filter Categories:**

```graphql
query {
  allCategories(
    first: 10
    nameContains: "tech"
    isActive: true
    orderBy: "-created"
  ) {
    totalCount
    edges {
      node {
        name
        description
      }
    }
  }
}
```

### Example Mutations

**Create Category:**

```graphql
mutation {
  createCategory(
    input: {
      name: "Technology"
      description: "Tech related content"
      isActive: true
    }
  ) {
    category {
      id
      name
      description
    }
  }
}
```

**Update Category:**

```graphql
mutation {
  updateCategory(
    input: {
      id: "Q2F0ZWdvcnlOb2RlOjE="
      name: "Updated Technology"
      description: "New description"
    }
  ) {
    category {
      id
      name
    }
  }
}
```

**Delete Category:**

```graphql
mutation {
  deleteCategory(input: { id: "Q2F0ZWdvcnlOb2RlOjE=" }) {
    found
    deletedId
  }
}
```

## 🧠 How It Works

### 1. GraphQL Schema

The GraphQL schema is defined in `brandfluence/schema.py` and combines all app schemas. It defines what data can be queried and what operations can be performed.

### 2. Category Model

Located in `category/models.py`, this defines the database structure:

- **name**: Category name (required)
- **description**: Category description
- **isActive**: Active status (default: true)
- **created/modified**: Automatic timestamps

### 3. Queries

Located in `category/queries/`:

- **category_single.py**: Get one category by ID
- **category_list.py**: Get all categories with filtering and pagination
- Returns data in Relay connection format with edges and pageInfo

### 4. Mutations

Located in `category/mutations/`:

- **create_category.py**: Create new category
- **update_category.py**: Update existing category
- **patch_category.py**: Partial update
- **delete_category.py**: Delete single or multiple categories
- **batch_create_category.py**: Create multiple categories at once

### 5. Filtering

Defined in `category/category_filter.py`:

- Search by name or description
- Filter by active status
- Filter by date ranges
- Sort by any field (ascending/descending)

### 6. Admin Panel

Enhanced in `category/admin.py`:

- List view with custom columns
- Bulk actions (activate, deactivate, delete)
- Search and filter options
- Custom status badges

## 📚 Learning Resources

### GraphQL Basics

- **Query**: Read data (like GET in REST)
- **Mutation**: Modify data (like POST, PUT, DELETE in REST)
- **Node**: A single object (like a category)
- **Connection**: List of objects with pagination
- **Edge**: Wrapper around node in connection
- **PageInfo**: Pagination metadata

### Useful Commands

```bash
# Check for errors
python manage.py check

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create sample data
python manage.py shell
>>> from category.models import Category
>>> Category.objects.create(name="Test", description="Test category")

# Run tests
python manage.py test category
```

### Next Steps

1. **Explore GraphQL Playground**: Try different queries and mutations
2. **Read Category README**: Check `category/README.md` for detailed examples
3. **Modify Code**: Try adding new fields to the Category model
4. **Create New App**: Use category app as a template for other models
5. **Learn More**: Visit [Graphene-Django Docs](https://docs.graphene-python.org/projects/django/en/latest/)

## 🆘 Common Issues

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8001
```

### Database Locked

```bash
# Stop all running servers and try again
# Or delete db.sqlite3 and run migrate again
```

### Package Import Errors

```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Not Activated

Make sure you see `(venv)` in your terminal prompt before running commands.

## 📧 Need Help?

- Check the GraphQL Playground documentation (click "Docs" in the playground)
- Read the inline comments in the code
- Review the `category/README.md` for detailed examples
- Django documentation: https://docs.djangoproject.com/
- Graphene-Django documentation: https://docs.graphene-python.org/projects/django/

---

**Happy Coding! 🚀**

Built with ❤️ using Django and GraphQL
