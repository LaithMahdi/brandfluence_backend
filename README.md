# Brandfluence - Django GraphQL API

A professional Django backend with GraphQL API built using Graphene-Django. This project provides user authentication with JWT tokens, role-based access control, and category management.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Authentication](#authentication)
- [Deployment](#deployment)
- [Using GraphQL](#using-graphql)
- [Learning Resources](#learning-resources)

## ✨ Features

- **User Authentication**: JWT token-based authentication with refresh tokens
- **Role-Based Access**: Admin, Company, and Influencer roles
- **User Verification**: Email verification and admin approval system
- **GraphQL API**: Full GraphQL implementation with queries and mutations
- **Category Management**: Complete CRUD operations for categories
- **Pagination**: Relay-style pagination with connection and edges
- **Filtering**: Advanced filtering by name, description, date, and status
- **Admin Panel**: Enhanced Django admin with custom actions and filters
- **Vercel Ready**: Configured for easy deployment to Vercel
- **Organized Code**: Professional folder structure for mutations and queries

## 🛠 Tech Stack

- **Django 5.2.7**: Python web framework
- **Graphene-Django 3.2.3**: GraphQL library for Django
- **django-graphql-jwt**: JWT authentication for GraphQL
- **PostgreSQL/SQLite**: Database support
- **WhiteNoise**: Static file serving
- **Python 3.x**: Programming language

**Key Libraries:**

- `graphene-django-cud`: Create, Update, Delete mutations
- `django-graphql-jwt`: JWT authentication
- `django-filter`: Advanced filtering
- `django-cors-headers`: CORS support
- `whitenoise`: Static file serving

## 📁 Project Structure

```
brandfluence/
│
├── brandfluence/           # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   └── schema.py           # Main GraphQL schema
│
├── users/                  # User authentication app
│   ├── models.py           # Custom User model
│   ├── admin.py            # User admin configuration
│   ├── user_node.py        # GraphQL user node
│   ├── schema.py           # User GraphQL schema
│   ├── queries/            # User queries
│   ├── mutations/          # User & auth mutations
│   ├── AUTHENTICATION.md   # Auth documentation
│   └── AUTH_EXAMPLES.md    # Code examples
│
├── category/               # Category app
│   ├── models.py           # Database model
│   ├── admin.py            # Admin configuration
│   ├── category_node.py    # GraphQL node definition
│   ├── category_filter.py  # Filtering options
│   ├── schema.py           # Category GraphQL schema
│   ├── queries/            # All GraphQL queries
│   └── mutations/          # All GraphQL mutations
│
├── vercel.json             # Vercel deployment config
├── vercel_app.py           # WSGI handler for Vercel
├── build_files.sh          # Build script
├── db.sqlite3              # SQLite database (dev)
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

## 🔑 Admin Password Management

If you forget your admin password or need to reset it, use the provided scripts:

### Quick Password Reset

```bash
# List all superusers in the database
python reset_admin_quick.py

# Reset password for a specific admin
python reset_admin_quick.py admin@example.com NewPassword123
```

### Interactive Password Reset

```bash
# Interactive mode with prompts
python reset_admin_password.py
```

**Example:**

```bash
# Reset password for admin@brandfluence.com
python reset_admin_quick.py admin@brandfluence.com Admin123456

# Output:
# ✅ Password successfully reset for admin@brandfluence.com
#    Name: admin
#    Role: ADMIN
```

**Note:** Password must be at least 8 characters long.

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
  - Manage users and categories

## � Importing Influencer Accounts

You can easily import influencer accounts from JSON files using the provided management command.

### Quick Start

**1. Preview the import (Dry Run):**

```bash
python manage.py import_influencers --dry-run
```

**2. Import from default file (`influencer_accounts.json`):**

Navigate to the project directory:

```bash
cd c:\Users\SBS\Music\brandfluence
```

Preview what will be imported (recommended first step):

```bash
python manage.py import_influencers --dry-run
```

If everything looks good, run the actual import:

```bash
python manage.py import_influencers
```

**3. Import from custom file:**

```bash
python manage.py import_influencers --file=path/to/your/file.json
```

**4. Update existing users:**

```bash
python manage.py import_influencers --update
```

### Sample Data Included

The `influencer_accounts.json` file includes 5 sample influencers:

- **Sarah Martin** - Fashion & Lifestyle (125K Instagram followers)
- **Alexandre Dubois** - Fitness Coach (95K Instagram followers)
- **Lisa Rousseau** - Travel Blogger (178K Instagram followers)
- **Marc Lefebvre** - Food & Chef (156K Instagram followers)
- **Emma Laurent** - Beauty & Makeup (142K Instagram followers)

### What Gets Imported

For each influencer:

- ✅ User account (email, name, phone, role, verification status)
- ✅ Influencer profile (bio, location, interests, languages)
- ✅ Social media accounts (Instagram, TikTok, YouTube with engagement metrics)
- ✅ Previous collaboration works
- ✅ Collaboration offers with pricing
- ✅ Categories (auto-created if they don't exist)

### Command Options

| Option      | Description                                             |
| ----------- | ------------------------------------------------------- |
| `--file`    | Path to JSON file (default: `influencer_accounts.json`) |
| `--dry-run` | Preview import without saving to database               |
| `--update`  | Update existing users instead of skipping them          |

### JSON File Structure

Each influencer entry should have:

```json
{
  "email": "email@example.com",
  "password": "SecurePassword123!",
  "name": "Full Name",
  "phone_number": "+33612345678",
  "role": "INFLUENCER",
  "email_verified": true,
  "is_verify_by_admin": true,
  "influencer_profile": {
    "instagram_username": "username",
    "pseudo": "Nickname",
    "biography": "Bio text...",
    "site_web": "https://website.com",
    "localisation": "City, Country",
    "langues": ["Français", "Anglais"],
    "centres_interet": ["Category1", "Category2"],
    "type_contenu": ["Photo", "Vidéo", "Story"],
    "disponibilite_collaboration": "disponible",
    "selected_categories": ["Category1", "Category2"],
    "reseaux_sociaux": [...],
    "previous_works": [...],
    "offres_collaboration": [...]
  }
}
```

**📖 For detailed documentation, see:** `INFLUENCER_IMPORT_README.md`

## �🔐 Authentication

This project uses JWT (JSON Web Token) authentication. See detailed guides:

- **Full Guide**: `users/AUTHENTICATION.md`
- **Code Examples**: `users/AUTH_EXAMPLES.md`

### Quick Start

**1. Register a User:**

```graphql
mutation {
  registerUser(
    email: "user@example.com"
    password: "securepass123"
    name: "John Doe"
    role: INFLUENCER
  ) {
    user {
      id
      email
      name
    }
    success
  }
}
```

**2. Login:**

```graphql
mutation {
  tokenAuth(email: "user@example.com", password: "securepass123") {
    token
    refreshToken
    user {
      id
      email
      name
      role
    }
  }
}
```

**3. Use Token in Headers:**

Add to HTTP Headers in GraphQL Playground:

```json
{
  "Authorization": "Bearer YOUR_TOKEN_HERE"
}
```

**4. Get Current User:**

```graphql
query {
  me {
    id
    email
    name
    role
    emailVerified
  }
}
```

### User Roles

- **ADMIN**: Full system access
- **COMPANY**: Company/brand account
- **INFLUENCER**: Influencer account (default)

### Login Requirements

Users must meet these criteria to login:

- ✅ Email verified
- ✅ Verified by admin
- ✅ Not banned
- ✅ Account active

## 🚀 Deployment

### Deploy to Vercel

See detailed guides:

- **Quick Start**: `DEPLOY_QUICK.md` (5 minutes)
- **Full Guide**: `VERCEL_DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`

**Quick Deploy:**

1. Push to GitHub
2. Import to Vercel
3. Add environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=.vercel.app
   ```
4. Deploy!

**Generate Secret Key:**

```bash
python generate_secret_key.py
```

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

# Reset superadmin password
python reset_admin_quick.py                                    # List all superusers
python reset_admin_quick.py admin@example.com NewPassword123  # Reset password
```

### Database Management

#### Reset/Drop Database

**For SQLite (Local Development):**

```bash
# Option 1: Delete the database file
# Windows
del db.sqlite3

# Mac/Linux
rm db.sqlite3

# Then recreate tables
python manage.py migrate
```

**For PostgreSQL (Neon/Cloud Hosted):**

The `reset_db` command doesn't work with cloud databases due to active connections:

```bash
# ❌ This will fail with "database is being accessed by other users"
python manage.py reset_db --noinput
```

**Solution - Use these alternatives:**

**Method 1: Drop and Recreate Tables (Recommended)**

```bash
# 1. Delete all migrations except __init__.py from each app
# Windows
del /S users\migrations\0*.py
del /S category\migrations\0*.py

# Mac/Linux
find users/migrations -name "0*.py" -delete
find category/migrations -name "0*.py" -delete

# 2. Drop all tables using Django shell
python manage.py shell

# In the shell, run:
from django.db import connection
cursor = connection.cursor()

# Get all table names
cursor.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public'
""")
tables = cursor.fetchall()

# Drop each table
for table in tables:
    cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')
    print(f"Dropped {table[0]}")

connection.commit()
exit()

# 3. Recreate migrations and tables
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Method 2: Using Neon Console (Easiest)**

1. Go to [Neon Console](https://console.neon.tech/)
2. Select your project
3. Navigate to your database
4. Click on "SQL Editor"
5. Run this SQL:

```sql
-- Drop all tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO public;
```

6. Back in your terminal:

```bash
python manage.py migrate
python manage.py createsuperuser
```

**Method 3: Selective Table Deletion**

If you only want to clear data without dropping the database:

```bash
python manage.py shell

# In the shell:
from users.models import User, VerifyToken
from category.models import Category

# Delete all data
User.objects.all().delete()
VerifyToken.objects.all().delete()
Category.objects.all().delete()

exit()

# Create new superuser
python manage.py createsuperuser
```

#### Migration Troubleshooting

```bash
# Show migration status
python manage.py showmigrations

# Fake migrations (mark as applied without running)
python manage.py migrate --fake

# Fake initial migrations only
python manage.py migrate --fake-initial

# Rollback specific migration
python manage.py migrate users 0001

# Rollback all migrations for an app
python manage.py migrate users zero
```

#### Database Connection Issues

If you see "database is being accessed by other users":

- Close all database connections (pgAdmin, DBeaver, etc.)
- Stop all running Django servers
- Close any Python shells connected to the database
- Wait a few minutes for idle connections to timeout
- For Neon databases, connections are automatically managed and may take time to close

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

### Managing Dependencies

**Update requirements.txt after installing new packages:**

```bash
# Freeze all installed packages to requirements.txt
pip freeze > requirements.txt
```

**Install a new package and update requirements:**

```bash
# Example: Install a new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

**Best Practice - Use pipreqs for cleaner requirements:**

```bash
# Install pipreqs
pip install pipreqs

# Generate requirements.txt based on actual imports in your code
pipreqs . --force
```

## 📧 Need Help?

- Check the GraphQL Playground documentation (click "Docs" in the playground)
- Read the inline comments in the code
- Review the `category/README.md` for detailed examples
- Django documentation: https://docs.djangoproject.com/
- Graphene-Django documentation: https://docs.graphene-python.org/projects/django/

---

**Happy Coding! 🚀**

Built with ❤️ using Django and GraphQL
