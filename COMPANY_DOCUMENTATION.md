# Company Profile Management - Documentation

## Overview

This module provides a complete GraphQL API for managing company profiles, including address management, image uploads, and profile completion tracking.

## Models

### Address Model

Located in `users/company_models.py`

```python
class Address:
    - address: CharField (max 255)
    - city: CharField (max 100)
    - state: CharField (max 100, optional)
    - postal_code: CharField (max 20, optional)
    - country: CharField (max 100)
    - created_at: DateTimeField
    - updated_at: DateTimeField
```

### Company Model

Located in `users/company_models.py`

```python
class Company:
    - user: OneToOneField(User) - Links to user with COMPANY role
    - company_name: CharField (max 150, required)
    - matricule: CharField (max 100, unique, optional) - Company registration number
    - website: URLField (optional)
    - size: CharField - Choices: S, M, L, XL
    - description: TextField (optional)
    - domain_activity: CharField - Choices: TECH, FIN, HLTH, EDU, ENT, MFG, RET, OTH
    - contact_email: EmailField (optional)
    - entreprise_type: CharField - Choices: PRIV, PUB, NGO, GOV
    - address: OneToOneField(Address, optional)
    - langues: JSONField (list of languages)
    - disponibilite_collaboration: CharField - Choices: disponible, occupe, partiellement_disponible
    - images: GenericRelation(Image) - Multiple images support
    - created_at: DateTimeField
    - updated_at: DateTimeField
```

## GraphQL API

### Mutations

#### 1. Create Company Profile

```graphql
mutation CreateCompanyProfile {
  createCompanyProfile(
    companyName: "TechCorp Inc."
    matricule: "REG123456"
    website: "https://techcorp.com"
    size: "M"
    description: "A leading technology company"
    domainActivity: "TECH"
    contactEmail: "contact@techcorp.com"
    entrepriseType: "PRIV"
    langues: ["English", "French"]
    disponibiliteCollaboration: "disponible"
    address: {
      address: "123 Tech Street"
      city: "Paris"
      state: "Île-de-France"
      postalCode: "75001"
      country: "France"
    }
    images: [
      { url: "https://example.com/logo.png", isDefault: true, isPublic: true }
    ]
  ) {
    success
    message
    company {
      id
      companyName
      matricule
      address {
        address
        city
        country
      }
      images {
        id
        url
        isDefault
      }
    }
  }
}
```

#### 2. Update Company Profile

```graphql
mutation UpdateCompanyProfile {
  updateCompanyProfile(
    companyName: "TechCorp International"
    description: "Updated description"
    size: "L"
    address: { address: "456 New Street", city: "Lyon", country: "France" }
  ) {
    success
    message
    company {
      id
      companyName
      description
      address {
        address
        city
      }
    }
  }
}
```

#### 3. Add Company Image

```graphql
mutation AddCompanyImage {
  addCompanyImage(
    url: "https://example.com/image.png"
    isDefault: false
    isPublic: true
  ) {
    success
    message
    image {
      id
      url
      isDefault
    }
  }
}
```

#### 4. Remove Company Image

```graphql
mutation RemoveCompanyImage {
  removeCompanyImage(imageId: "1") {
    success
    message
  }
}
```

#### 5. Complete Company Profile

```graphql
mutation CompleteCompanyProfile {
  completeCompanyProfile {
    success
    message
    company {
      id
      companyName
      user {
        isCompletedProfile
      }
    }
  }
}
```

### Queries

#### 1. Get My Company Profile

```graphql
query MyCompanyProfile {
  myCompanyProfile {
    id
    companyName
    matricule
    website
    size
    description
    domainActivity
    contactEmail
    entrepriseType
    langues
    disponibiliteCollaboration
    address {
      id
      address
      city
      state
      postalCode
      country
    }
    images {
      id
      url
      isDefault
      isPublic
    }
    user {
      email
      name
      isCompletedProfile
    }
    createdAt
    updatedAt
  }
}
```

#### 2. Get Company by ID

```graphql
query GetCompany {
  company(id: "1") {
    id
    companyName
    matricule
    website
    address {
      address
      city
      country
    }
  }
}
```

#### 3. Get Company by User ID

```graphql
query GetCompanyByUser {
  companyByUser(userId: "1") {
    id
    companyName
    user {
      email
      name
    }
  }
}
```

#### 4. List Companies with Filters

```graphql
query ListCompanies {
  companies(
    first: 10
    skip: 0
    domainActivity: "TECH"
    size: "M"
    country: "France"
    disponibiliteCollaboration: "disponible"
  ) {
    id
    companyName
    size
    domainActivity
    address {
      city
      country
    }
  }
}
```

#### 5. Get Companies Count

```graphql
query CompaniesCount {
  companiesCount(domainActivity: "TECH", size: "M", country: "France")
}
```

## Workflow

### 1. User Registration

- User registers with role = "COMPANY"
- User verifies email
- User is now ready to create company profile

### 2. Company Profile Creation

1. Use `createCompanyProfile` mutation
2. Provide required fields: `companyName`
3. Optionally provide address, images, and other details
4. System creates Company record linked to User

### 3. Profile Completion

1. User updates profile with all necessary information
2. System validates required fields (company_name, address)
3. Use `completeCompanyProfile` mutation
4. System marks `user.is_completed_profile = True`

### 4. Profile Management

- Update company details using `updateCompanyProfile`
- Add/remove images using image mutations
- Query company data using provided queries

## Field Choices

### Company Size

- `S`: Small (1-50 employees)
- `M`: Medium (51-200 employees)
- `L`: Large (201-1000 employees)
- `XL`: Extra Large (1001+ employees)

### Domain Activity

- `TECH`: Technology
- `FIN`: Finance
- `HLTH`: Healthcare
- `EDU`: Education
- `ENT`: Entertainment
- `MFG`: Manufacturing
- `RET`: Retail
- `OTH`: Other

### Enterprise Type

- `PRIV`: Private
- `PUB`: Public
- `NGO`: Non-Governmental Organization
- `GOV`: Government Agency

### Disponibilité Collaboration

- `disponible`: Available
- `occupe`: Busy
- `partiellement_disponible`: Partially available

## Database Migration

To apply the new models to your database:

```bash
# Create migrations
python manage.py makemigrations users

# Apply migrations
python manage.py migrate users
```

## Admin Interface

Both Company and Address models are registered in the Django admin:

- `/admin/users/company/` - Manage companies
- `/admin/users/address/` - Manage addresses

## Testing Examples

### Complete Flow Example

```graphql
# 1. Login as a user with COMPANY role
mutation Login {
  login(email: "company@example.com", password: "password") {
    success
    token
    user {
      role
    }
  }
}

# 2. Create company profile
mutation CreateProfile {
  createCompanyProfile(
    companyName: "My Company"
    matricule: "REG789"
    address: { address: "123 Street", city: "Paris", country: "France" }
  ) {
    success
    company {
      id
      companyName
    }
  }
}

# 3. Complete profile
mutation Complete {
  completeCompanyProfile {
    success
    company {
      user {
        isCompletedProfile
      }
    }
  }
}

# 4. Query profile
query MyProfile {
  myCompanyProfile {
    id
    companyName
    matricule
    address {
      address
      city
      country
    }
  }
}
```

## Security & Permissions

- **Authentication Required**: All mutations require user to be authenticated
- **Role Validation**: User must have COMPANY role to create/update company profile
- **Ownership Check**: Users can only modify their own company profile
- **Image Management**: Only the company owner can add/remove images

## Notes

- Each user with COMPANY role can have only ONE company profile
- Company name is required for profile creation
- Address and company_name are required for profile completion
- Images use a generic relation system and can be shared across models
- Matricule (registration number) must be unique if provided
