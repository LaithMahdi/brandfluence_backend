# 🚀 Brandfluence - Influencer Marketing Platform

<div align="center">

**A professional Django-based influencer marketing platform with GraphQL API, AI-powered recommendations, and comprehensive brand-influencer collaboration features.**

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-Graphene-E10098.svg)](https://graphene-python.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [API Documentation](#-api-documentation)
- [Machine Learning Features](#-machine-learning-features)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Support](#-support)

---

## 🌟 Overview

**Brandfluence** is a comprehensive influencer marketing platform that connects brands with influencers through an intelligent matching system. The platform leverages machine learning algorithms to recommend the best influencer-brand matches based on various criteria including category, engagement, reach, and audience demographics.

### What Makes Brandfluence Special?

- **AI-Powered Recommendations**: Multiple ML models (Cosine Similarity, K-Nearest Neighbors, Content-Based Filtering) for intelligent influencer-brand matching
- **Three-Tier User System**: Separate workflows for Admins, Companies, and Influencers
- **Complete Campaign Management**: From offer creation to application tracking and approval
- **Real-time GraphQL API**: Modern, efficient data fetching with subscriptions support
- **Production Ready**: Dockerized with support for Google Cloud Run, Render, and Vercel deployments

---

## ✨ Key Features

### 🔐 Authentication & Authorization

- **JWT Token-based Authentication** with refresh tokens
- **Role-Based Access Control** (RBAC):
  - **Admin**: Full platform management
  - **Company**: Create offers, review applications, manage campaigns
  - **Influencer**: Browse offers, submit applications, manage profile
- **Email Verification** system with admin approval workflow
- **Phone Number Verification** for enhanced security
- **User Ban/Unban** functionality for moderation

### 👥 User Management

#### For Influencers:

- Comprehensive profile with bio, location, and social metrics
- Multiple category associations
- Portfolio management with image uploads
- Social media integration (Instagram, TikTok, YouTube, etc.)
- Engagement metrics tracking (followers, avg likes, comments)
- Availability status management
- Language preferences
- Gender demographics

#### For Companies:

- Company profile with business details
- Multi-address support
- Domain of activity classification
- Company size categorization
- Website and social media links
- Logo and brand asset management

### 📢 Campaign & Offer Management

- **Offer Creation**: Companies create detailed collaboration offers
- **Budget Management**: Min/max budget ranges with flexible pricing
- **Timeline Planning**: Start and end date specifications
- **Requirements Definition**: Detailed requirements and objectives
- **Application System**: Influencers submit proposals with:
  - Custom pricing proposals
  - Cover letters
  - Estimated reach and delivery timeline
  - Portfolio links
- **Application Tracking**: Real-time status updates (Pending, Approved, Rejected, Withdrawn)
- **Review Workflow**: Admin review with notes and rejection reasons

### 🎯 Category System

- Hierarchical category structure
- Multiple categories per influencer
- Category-based filtering and search
- Category statistics and analytics

### 🤖 Machine Learning & Recommendations

- **Multiple Recommendation Models**:
  - Cosine Similarity for content-based matching
  - K-Nearest Neighbors (KNN) for collaborative filtering
  - Content-Based Filtering for detailed feature matching
- **Feature Engineering**:
  - TF-IDF vectorization for text analysis
  - Category encoding
  - Location-based matching
  - Engagement rate calculations
- **Model Comparison & Selection**: Automated model performance evaluation
- **Real-time Recommendations**: On-demand influencer suggestions

### 🔍 Advanced Filtering & Search

- **Multi-field Filtering**: Name, description, status, dates
- **Range Queries**: Budget, follower count, engagement rates
- **Text Search**: Case-insensitive, partial matching
- **Relay-style Pagination**: Efficient cursor-based pagination
- **Ordering**: Flexible sorting on multiple fields

### 📊 Data Visualization & Analytics

- Visual data exploration tools
- Category distribution analysis
- Engagement metrics visualization
- User activity tracking

---

## 🛠 Tech Stack

### Backend Framework

- **Django 5.2.7**: Robust Python web framework
- **Graphene-Django 3.2.3**: GraphQL implementation for Django
- **django-graphql-jwt 0.4.0**: JWT authentication for GraphQL
- **Django REST Framework 3.15.2**: REST API support

### Database

- **PostgreSQL**: Production database (via psycopg2-binary)
- **SQLite**: Development database

### Machine Learning

- **scikit-learn**: ML algorithms and model training
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **TF-IDF Vectorization**: Text feature extraction

### DevOps & Deployment

- **Docker**: Containerization
- **Google Cloud Run**: Serverless deployment
- **Render**: Platform-as-a-Service
- **Gunicorn**: WSGI HTTP Server
- **WhiteNoise**: Static file serving

### Key Libraries

- **django-cors-headers**: Cross-Origin Resource Sharing
- **django-filter**: Advanced filtering
- **graphene-django-cud**: Create, Update, Delete mutations
- **graphene-django-optimizer**: Query optimization
- **graphene-file-upload**: File upload support
- **python-dotenv**: Environment variable management

---

## 🏗 Project Architecture

```
brandfluence/
│
├── 📂 brandfluence/              # Main project configuration
│   ├── settings.py               # Django settings with environment configs
│   ├── urls.py                   # Main URL routing
│   ├── schema.py                 # Root GraphQL schema
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── 📂 users/                     # User authentication & profiles
│   ├── models.py                 # Base User model with roles
│   ├── influencer_models.py      # Influencer profile & social data
│   ├── company_models.py         # Company profile & business data
│   ├── influencer_node.py        # GraphQL node definitions
│   ├── schema.py                 # User GraphQL schema
│   ├── admin.py                  # Enhanced admin interface
│   ├── queries/                  # User queries
│   ├── mutations/                # User mutations (CRUD, auth)
│   └── types/                    # GraphQL type definitions
│
├── 📂 category/                  # Category management
│   ├── models.py                 # Category model
│   ├── schema.py                 # Category GraphQL schema
│   ├── admin.py                  # Category admin
│   ├── queries/                  # Category queries with filtering
│   ├── mutations/                # Category CRUD operations
│   ├── types/                    # Category GraphQL types
│   └── filters/                  # Advanced filtering options
│
├── 📂 offer/                     # Campaign & offer management
│   ├── models.py                 # Offer & Application models
│   ├── schema.py                 # Offer GraphQL schema
│   ├── admin.py                  # Offer admin interface
│   ├── queries/                  # Offer queries
│   ├── mutations/                # Offer CRUD & application mutations
│   ├── types/                    # Offer GraphQL types
│   └── filters/                  # Offer filtering
│
├── 📂 api/                       # Data processing & ML
│   ├── views.py                  # API views
│   ├── urls.py                   # API routing
│   ├── architecture_finale.py    # System architecture
│   ├── import_to_postgres.py     # Data import utilities
│   ├── create_cosine_model.py    # Cosine similarity model
│   ├── compare_recommendation_models.py  # Model evaluation
│   ├── data/                     # Data files & datasets
│   │   ├── influenceurs_clean.csv
│   │   ├── Top_Influencers_Full_1500.csv
│   │   ├── feature_matrix.npy
│   │   └── metadata.json
│   ├── models/                   # Trained ML models
│   │   ├── best_model_cosine_similarity.pkl
│   │   ├── best_model_k-nearest_neighbors.pkl
│   │   ├── best_model_content-based_filtering.pkl
│   │   ├── scaler.pkl
│   │   ├── tfidf.pkl
│   │   └── feature_columns.pkl
│   └── visualizations/           # Data visualization tools
│
├── 📂 common/                    # Shared utilities
│   └── pagination_utils.py       # Pagination helpers
│
├── 📂 data/                      # Root data directory
│   ├── influenceurs_clean.csv    # Cleaned influencer data
│   ├── feature_matrix.npy        # ML feature matrix
│   └── metadata.json             # Dataset metadata
│
├── 📂 static/                    # Static files (CSS, JS, images)
├── 📂 templates/                 # HTML templates
│   └── emails/                   # Email templates
│
├── 📄 Dockerfile                 # Docker containerization
├── 📄 cloudbuild.yaml            # Google Cloud Build config
├── 📄 app.yaml                   # Google App Engine config
├── 📄 render.yaml                # Render deployment config
├── 📄 requirements.txt           # Python dependencies
├── 📄 manage.py                  # Django management script
├── 📄 schema.graphql             # GraphQL schema documentation
├── 📄 test_queries.graphql       # Example GraphQL queries
└── 📄 README.md                  # This file
```

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package manager (comes with Python)
- **PostgreSQL** (optional, for production): [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker** (optional, for containerized deployment): [Download Docker](https://www.docker.com/get-started)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/brandfluence.git
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

This will install all required packages including Django, GraphQL, ML libraries, and deployment tools.

---

## ⚙️ Configuration

### Step 1: Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/brandfluence

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Settings (Optional)
JWT_EXPIRATION_DELTA=7200  # 2 hours in seconds
JWT_REFRESH_EXPIRATION_DELTA=604800  # 7 days in seconds

# Cloud Storage (Optional)
CLOUDINARY_URL=cloudinary://your-cloudinary-url

# Google Cloud (for deployment)
GOOGLE_CLOUD_PROJECT=your-project-id
```

### Step 2: Generate Secret Key

You can generate a secure secret key using:

```bash
python generate_secret_key.py
```

Or use Python:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Database Setup

#### Using SQLite (Default - Development)

No configuration needed. Django will create `db.sqlite3` automatically.

#### Using PostgreSQL (Production)

1. Install PostgreSQL and create a database:

```sql
CREATE DATABASE brandfluence;
CREATE USER brandfluence_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE brandfluence TO brandfluence_user;
```

2. Update `.env` file:

```env
DATABASE_URL=postgresql://brandfluence_user:your_password@localhost:5432/brandfluence
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:

- Email: admin@example.com
- Name: Admin User
- Password: **\*\*\*\***

### Step 6: Load Initial Data (Optional)

If you have initial data files:

```bash
# Import influencer data
python api/import_to_postgres.py

# Verify data integrity
python api/check_tables.py
python verify_data_files.py
```

---

## 🏃 Running the Project

### Development Server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### Access Points

- **GraphQL Playground**: `http://127.0.0.1:8000/graphql/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **REST API**: `http://127.0.0.1:8000/api/`

### Using Docker

#### Build and Run

```bash
# Build the Docker image
docker build -t brandfluence .

# Run the container
docker run -p 8080:8080 --env-file .env brandfluence
```

#### Using Docker Compose (if you have docker-compose.yml)

```bash
docker-compose up --build
```

---

## 📡 API Documentation

### GraphQL API

The platform uses GraphQL for its primary API. Access the interactive GraphQL Playground at `/graphql/`.

#### Authentication

All authenticated requests require a JWT token in the header:

```
Authorization: JWT <your-token-here>
```

#### 1. User Registration & Authentication

**Register a New User:**

```graphql
mutation {
  register(
    email: "user@example.com"
    name: "John Doe"
    password: "securepassword123"
    role: "INFLUENCER"
    phoneNumber: "+1234567890"
  ) {
    success
    message
    user {
      id
      email
      name
      role
    }
  }
}
```

**Login:**

```graphql
mutation {
  tokenAuth(email: "user@example.com", password: "securepassword123") {
    token
    refreshToken
    payload
    user {
      id
      email
      name
      role
      isActive
      emailVerified
    }
  }
}
```

**Refresh Token:**

```graphql
mutation {
  refreshToken(refreshToken: "your-refresh-token") {
    token
    refreshToken
    payload
  }
}
```

**Verify Token:**

```graphql
mutation {
  verifyToken(token: "your-jwt-token") {
    payload
  }
}
```

#### 2. User Queries

**Get Current User:**

```graphql
query {
  me {
    id
    email
    name
    role
    phoneNumber
    emailVerified
    isVerifyByAdmin
    createdAt
  }
}
```

**Get All Users (Admin only):**

```graphql
query {
  allUsers(first: 10) {
    edges {
      node {
        id
        email
        name
        role
        isActive
        emailVerified
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

**Get User by ID:**

```graphql
query {
  user(id: "VXNlck5vZGU6MQ==") {
    id
    email
    name
    role
    createdAt
  }
}
```

#### 3. Influencer Profile Management

**Create Influencer Profile:**

```graphql
mutation {
  createInfluencer(
    input: {
      bio: "Fashion and lifestyle influencer based in Paris"
      location: "Paris, France"
      instagramUsername: "@johndoe"
      instagramFollowers: 150000
      instagramAvgLikes: 8500
      tiktokUsername: "@johndoe"
      youtubeChannel: "JohnDoeVlogs"
      disponibilite: "DISPONIBLE"
      categories: ["Q2F0ZWdvcnlOb2RlOjE=", "Q2F0ZWdvcnlOb2RlOjI="]
      languages: ["French", "English"]
      genderAudience: "MIXED"
    }
  ) {
    influencer {
      id
      bio
      location
      instagramUsername
      instagramFollowers
      categories {
        edges {
          node {
            id
            name
          }
        }
      }
    }
  }
}
```

**Update Influencer Profile:**

```graphql
mutation {
  updateInfluencer(
    id: "SW5mbHVlbmNlck5vZGU6MQ=="
    input: {
      bio: "Updated bio"
      instagramFollowers: 160000
      disponibilite: "OCCUPE"
    }
  ) {
    influencer {
      id
      bio
      instagramFollowers
      disponibilite
    }
  }
}
```

**Query Influencers:**

```graphql
query {
  allInfluencers(
    first: 10
    instagramFollowers_Gte: 10000
    disponibilite: "DISPONIBLE"
  ) {
    edges {
      node {
        id
        user {
          name
          email
        }
        bio
        location
        instagramUsername
        instagramFollowers
        instagramAvgLikes
        engagementRate
        categories {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
```

#### 4. Company Profile Management

**Create Company Profile:**

```graphql
mutation {
  createCompany(
    input: {
      companyName: "TechCorp Inc."
      companySize: "M"
      domainActivity: "TECH"
      description: "Leading technology company"
      website: "https://techcorp.com"
      linkedinUrl: "https://linkedin.com/company/techcorp"
      addresses: [
        {
          address: "123 Tech Street"
          city: "San Francisco"
          state: "CA"
          postalCode: "94105"
          country: "USA"
        }
      ]
    }
  ) {
    company {
      id
      companyName
      companySize
      website
      addresses {
        edges {
          node {
            address
            city
            country
          }
        }
      }
    }
  }
}
```

#### 5. Category Management

**Get All Categories:**

```graphql
query {
  allCategories(first: 20, ordering: "name") {
    edges {
      node {
        id
        name
        description
        isActive
        createdAt
      }
    }
  }
}
```

**Create Category (Admin only):**

```graphql
mutation {
  createCategory(
    input: {
      name: "Fashion"
      description: "Fashion and style content"
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

#### 6. Offer Management

**Create Offer (Company only):**

```graphql
mutation {
  createOffer(
    input: {
      title: "Summer Fashion Campaign"
      minBudget: "1000.00"
      maxBudget: "5000.00"
      startDate: "2025-07-01"
      endDate: "2025-08-31"
      influencerNumber: 5
      requirement: "Must have fashion-focused content"
      objectif: "Promote our summer collection to young audiences"
    }
  ) {
    offer {
      id
      title
      minBudget
      maxBudget
      startDate
      endDate
      createdBy {
        name
        email
      }
    }
  }
}
```

**Query Offers:**

```graphql
query {
  allOffers(first: 10, minBudget_Gte: "500", ordering: "-createdAt") {
    edges {
      node {
        id
        title
        minBudget
        maxBudget
        startDate
        endDate
        influencerNumber
        requirement
        objectif
        createdBy {
          name
          email
        }
        createdAt
      }
    }
  }
}
```

**Apply to Offer (Influencer only):**

```graphql
mutation {
  createOfferApplication(
    input: {
      offerId: "T2ZmZXJOb2RlOjE="
      proposal: "I would love to collaborate on this campaign..."
      askingPrice: "2500.00"
      coverLetter: "Dear Brand Team..."
      estimatedReach: 150000
      deliveryDays: 14
      portfolioLinks: [
        "https://instagram.com/post1"
        "https://youtube.com/video1"
      ]
    }
  ) {
    application {
      id
      offer {
        title
      }
      proposal
      askingPrice
      status
      submittedAt
    }
  }
}
```

**Update Application Status (Company/Admin):**

```graphql
mutation {
  updateApplicationStatus(
    applicationId: "QXBwbGljYXRpb25Ob2RlOjE="
    status: "APPROVED"
    adminNotes: "Excellent proposal, approved for collaboration"
  ) {
    application {
      id
      status
      reviewedAt
      reviewedBy {
        name
      }
    }
  }
}
```

#### 7. Search & Filtering Examples

**Advanced Influencer Search:**

```graphql
query {
  allInfluencers(
    location_Icontains: "Paris"
    instagramFollowers_Gte: 50000
    instagramFollowers_Lte: 500000
    disponibilite: "DISPONIBLE"
    categories: ["Q2F0ZWdvcnlOb2RlOjE="]
    ordering: "-instagramFollowers"
    first: 20
  ) {
    edges {
      node {
        id
        user {
          name
        }
        location
        instagramFollowers
        engagementRate
      }
    }
  }
}
```

**Date Range Offer Search:**

```graphql
query {
  allOffers(
    startDate_Gte: "2025-06-01"
    endDate_Lte: "2025-12-31"
    minBudget_Gte: "1000"
    first: 10
  ) {
    edges {
      node {
        title
        minBudget
        maxBudget
        startDate
        endDate
      }
    }
  }
}
```

### REST API Endpoints

Some utility endpoints are available via REST:

- `GET /api/health/` - Health check endpoint
- `GET /api/recommendations/<influencer_id>/` - Get influencer recommendations

---

## 🤖 Machine Learning Features

### Recommendation System

The platform includes multiple ML models for intelligent influencer-brand matching:

#### 1. Cosine Similarity Model

Best for content-based matching using TF-IDF vectorization.

```bash
# Train the model
python api/create_cosine_model.py
```

#### 2. K-Nearest Neighbors (KNN)

Collaborative filtering based on feature similarity.

#### 3. Content-Based Filtering

Uses comprehensive feature engineering including:

- Category encoding
- Location matching
- Engagement metrics
- Follower count analysis

### Model Comparison

Compare all models and select the best performer:

```bash
python api/compare_recommendation_models.py
```

This generates:

- Performance metrics (accuracy, precision, recall)
- Model comparison report
- Best model selection

### Using Recommendations

**Via GraphQL:**

```graphql
query {
  recommendInfluencers(
    companyId: "Q29tcGFueU5vZGU6MQ=="
    topN: 10
    minFollowers: 50000
    categories: ["Fashion", "Lifestyle"]
  ) {
    influencers {
      id
      name
      score
      matchReason
    }
  }
}
```

### Data Processing

**Import and Clean Data:**

```bash
# Import influencer data to database
python api/import_to_postgres.py

# Verify data quality
python api/verifier_qualite.py

# Run exploratory data analysis
python eda_analysis.py
```

---

## 🚀 Deployment

### Google Cloud Run

#### Prerequisites

- Google Cloud account
- `gcloud` CLI installed
- Docker installed

#### Steps

1. **Build and deploy:**

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build with Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Or build locally and push
docker build -t gcr.io/YOUR_PROJECT_ID/brandfluence .
docker push gcr.io/YOUR_PROJECT_ID/brandfluence

# Deploy to Cloud Run
gcloud run deploy brandfluence \
  --image gcr.io/YOUR_PROJECT_ID/brandfluence \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DEBUG=False,SECRET_KEY=your-secret-key"
```

2. **Set environment variables:**

```bash
gcloud run services update brandfluence \
  --set-env-vars="DATABASE_URL=postgresql://...,SECRET_KEY=..."
```

3. **Check deployment:**

```bash
./check_cloud_run_logs.sh
```

### Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn brandfluence.wsgi:application`
4. Add environment variables in Render dashboard
5. Deploy!

### Vercel (Serverless)

1. Install Vercel CLI:

```bash
npm install -g vercel
```

2. Deploy:

```bash
vercel --prod
```

3. Configure environment variables in Vercel dashboard

### Docker Production

```bash
# Build production image
docker build -t brandfluence:production .

# Run with production settings
docker run -d \
  -p 8080:8080 \
  -e DEBUG=False \
  -e SECRET_KEY=your-production-secret \
  -e DATABASE_URL=your-db-url \
  --name brandfluence-prod \
  brandfluence:production
```

---

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
# Test users app
python manage.py test users

# Test categories
python manage.py test category

# Test offers
python manage.py test offer
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Manual Testing

Use the included test files:

```bash
# Test login functionality
python quick_test_login.py

# Check admin status
python check_admin_status.py

# Verify user roles
python check_user_role.py

# Test token generation
python get_fresh_token.py
```

---

## 🛠 Utility Scripts

The project includes various utility scripts for management and debugging:

### User Management

- `list_all_users_roles.py` - List all users with their roles
- `find_admin_user.py` - Find admin users in the system
- `reset_admin_password.py` - Reset admin password
- `check_user_role.py` - Check specific user role
- `fix_corrupted_roles.py` - Fix role data issues

### Authentication & Tokens

- `get_fresh_token.py` - Generate fresh JWT token
- `check_token_payload.py` - Inspect token payload
- `decode_jwt.py` - Decode JWT tokens
- `cleanup_tokens.bat` - Clean expired tokens
- `run_token_cleanup.py` - Token cleanup script

### Data Management

- `check_influencer_data.py` - Verify influencer data integrity
- `check_disponibilite.py` - Check availability statuses
- `verify_data_files.py` - Verify all data files exist
- `import_to_postgres.py` - Import data to PostgreSQL

### Deployment & Testing

- `check_deployment_readiness.bat` - Pre-deployment checks
- `emergency_fix.sh` - Emergency deployment fixes
- `check_cloud_run_logs.sh` - View Cloud Run logs

---

## 📚 Project Documentation

Additional documentation files:

- [AUTHENTICATION.md](users/AUTHENTICATION.md) - Detailed authentication guide
- [AUTH_EXAMPLES.md](users/AUTH_EXAMPLES.md) - Authentication code examples
- [QUERY_RESTRUCTURE.md](users/QUERY_RESTRUCTURE.md) - Query optimization guide
- [GOOGLE_CLOUD_DEPLOYMENT.md](GOOGLE_CLOUD_DEPLOYMENT.md) - Google Cloud deployment
- [CLOUD_RUN_DEPLOYMENT_FIX.md](CLOUD_RUN_DEPLOYMENT_FIX.md) - Cloud Run troubleshooting
- [FIX_ALL_ENUMS.md](FIX_ALL_ENUMS.md) - Enum handling guide

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Keep code DRY (Don't Repeat Yourself)

### Pull Request Guidelines

- Provide clear description of changes
- Include relevant issue numbers
- Ensure all tests pass
- Update README if needed
- Add screenshots for UI changes

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

### Getting Help

- **Documentation**: Check the `/docs` folder and inline documentation
- **Issues**: [Open an issue](https://github.com/yourusername/brandfluence/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/brandfluence/discussions)

### Contact

- **Email**: support@brandfluence.com
- **Website**: https://brandfluence.com
- **Twitter**: [@brandfluence](https://twitter.com/brandfluence)

---

## 🙏 Acknowledgments

- Django community for the excellent framework
- Graphene-Django for GraphQL implementation
- All contributors who have helped improve this project
- Open source libraries that made this possible

---

## 🗺️ Roadmap

### Current Version (v1.0)

- ✅ User authentication with JWT
- ✅ Role-based access control
- ✅ Influencer and Company profiles
- ✅ Offer and Application system
- ✅ ML-powered recommendations
- ✅ GraphQL API
- ✅ Docker support
- ✅ Cloud deployment configs

### Upcoming Features (v2.0)

- 🔄 Real-time chat between brands and influencers
- 🔄 Payment integration (Stripe/PayPal)
- 🔄 Contract management system
- 🔄 Analytics dashboard
- 🔄 Email notifications
- 🔄 Mobile app (React Native)
- 🔄 Advanced analytics and reporting
- 🔄 Campaign performance tracking
- 🔄 Multi-language support

### Future Enhancements

- AI-powered content suggestions
- Automated campaign management
- Influencer verification system
- Social media integration APIs
- Content calendar management
- ROI tracking and analytics

---

## 📊 Project Stats

- **Lines of Code**: ~15,000+
- **Number of Apps**: 5 (users, category, offer, api, common)
- **GraphQL Queries**: 20+
- **GraphQL Mutations**: 30+
- **ML Models**: 3
- **Database Tables**: 10+
- **API Endpoints**: 50+

---

<div align="center">

**Made with ❤️ by the Brandfluence Team**

⭐ **Star this repo if you find it helpful!** ⭐

[Report Bug](https://github.com/yourusername/brandfluence/issues) • [Request Feature](https://github.com/yourusername/brandfluence/issues) • [Documentation](https://docs.brandfluence.com)

</div>
