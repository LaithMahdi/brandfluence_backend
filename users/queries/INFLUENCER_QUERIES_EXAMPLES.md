# Influencer Queries Examples

This document provides examples of how to query influencers using the new pagination, filtering, and totalCount features.

## Features Implemented

Following the same pattern as the Category queries, the influencer queries now support:

- **Relay-style pagination** with `edges` and `pageInfo`
- **totalCount** in the connection to show total number of results
- **Advanced filtering** through `InfluencerFilter`
- **Ordering** with customizable sort fields

## Query: All Influencers with Pagination and TotalCount

```graphql
query GetAllInfluencers($first: Int, $after: String) {
  allInfluencers(first: $first, after: $after) {
    totalCount
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
        pseudo
        biography
        localisation
        disponibiliteCollaboration
        instagramUsername
        siteWeb
        statistiquesGlobales {
          followersTotaux
          engagementMoyenGlobal
          croissanceMensuelle
        }
        selectedCategories {
          id
          name
        }
        langues
        centresInteret
        typeContenu
        createdAt
        updatedAt
      }
    }
  }
}
```

Variables:

```json
{
  "first": 10,
  "after": null
}
```

## Query: Filtered Influencers

Filter influencers by various criteria:

```graphql
query FilteredInfluencers(
  $pseudo: String
  $localisation: String
  $disponibiliteCollaboration: String
  $minFollowers: Int
  $maxFollowers: Int
  $minEngagement: Float
  $maxEngagement: Float
  $first: Int
  $after: String
) {
  allInfluencers(
    pseudo: $pseudo
    localisation: $localisation
    disponibiliteCollaboration: $disponibiliteCollaboration
    minFollowers: $minFollowers
    maxFollowers: $maxFollowers
    minEngagement: $minEngagement
    maxEngagement: $maxEngagement
    first: $first
    after: $after
  ) {
    totalCount
    edges {
      node {
        id
        pseudo
        localisation
        disponibiliteCollaboration
        statistiquesGlobales {
          followersTotaux
          engagementMoyenGlobal
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Variables:

```json
{
  "localisation": "Paris",
  "minFollowers": 10000,
  "disponibiliteCollaboration": "disponible",
  "first": 20
}
```

## Query: Influencers with Text Search

Search influencers by pseudo, biography, or interests:

```graphql
query SearchInfluencers($pseudo: String, $biography: String, $first: Int) {
  allInfluencers(pseudo: $pseudo, biography: $biography, first: $first) {
    totalCount
    edges {
      node {
        id
        pseudo
        biography
        localisation
        statistiquesGlobales {
          followersTotaux
          engagementMoyenGlobal
        }
      }
    }
  }
}
```

Variables:

```json
{
  "pseudo": "fashion",
  "first": 10
}
```

## Query: Ordered Influencers

Order results by specific fields:

```graphql
query OrderedInfluencers($orderBy: String, $first: Int) {
  allInfluencers(orderBy: $orderBy, first: $first) {
    totalCount
    edges {
      node {
        id
        pseudo
        createdAt
        localisation
      }
    }
  }
}
```

Variables:

```json
{
  "orderBy": "-created_at",
  "first": 10
}
```

Available ordering fields:

- `pseudo`, `-pseudo`
- `localisation`, `-localisation`
- `created_at`, `-created_at`
- `updated_at`, `-updated_at`

## Query: Get Single Influencer by ID

```graphql
query GetInfluencer($id: ID!) {
  influencer(id: $id) {
    id
    pseudo
    biography
    localisation
    disponibiliteCollaboration
    instagramUsername
    siteWeb
    instagramData
    selectedCategories {
      id
      name
    }
    langues
    centresInteret
    typeContenu
    statistiquesGlobales {
      followersTotaux
      engagementMoyenGlobal
      croissanceMensuelle
    }
    reseauxSociaux {
      id
      plateforme
      urlProfil
      nombreAbonnes
      tauxEngagement
      frequencePublication
    }
    previousWorks {
      id
      brandName
      campaign
      period
      results
    }
    images {
      id
      url
      isDefault
    }
    portfolioMedia {
      id
      imageUrl
      titre
      description
    }
    offresCollaboration {
      id
      typeCollaboration
      tarifMinimum
      tarifMaximum
      conditions
    }
  }
}
```

## Query: Get Current User's Influencer Profile

```graphql
query MyInfluencerProfile {
  myInfluencerProfile {
    id
    pseudo
    biography
    localisation
    disponibiliteCollaboration
    instagramUsername
    statistiquesGlobales {
      followersTotaux
      engagementMoyenGlobal
      croissanceMensuelle
    }
    selectedCategories {
      id
      name
    }
    reseauxSociaux {
      plateforme
      nombreAbonnes
      tauxEngagement
    }
  }
}
```

## Query: Get Influencer by User ID

```graphql
query GetInfluencerByUser($userId: ID!) {
  influencerByUser(userId: $userId) {
    id
    pseudo
    biography
    localisation
    statistiquesGlobales {
      followersTotaux
      engagementMoyenGlobal
    }
  }
}
```

## Query: Search Influencers (Legacy)

This is the old-style search that returns a List instead of Connection:

```graphql
query SearchInfluencersLegacy(
  $query: String!
  $localisation: String
  $minFollowers: Int
  $maxFollowers: Int
  $minEngagement: Float
  $categoryIds: [ID]
) {
  searchInfluencers(
    query: $query
    localisation: $localisation
    minFollowers: $minFollowers
    maxFollowers: $maxFollowers
    minEngagement: $minEngagement
    categoryIds: $categoryIds
  ) {
    id
    pseudo
    biography
    localisation
    statistiquesGlobales {
      followersTotaux
      engagementMoyenGlobal
    }
  }
}
```

## Available Filters

The `InfluencerFilter` supports the following filters:

### Text Filters (case-insensitive contains)

- `pseudo` - Filter by influencer pseudo/username
- `localisation` - Filter by location
- `biography` - Filter by biography text
- `centresInteret` - Filter by interests
- `instagramUsername` - Exact match or contains
- `siteWeb` - Website URL

### Enum Filters

- `disponibiliteCollaboration` - Availability status (exact match)
  - Values: `disponible`, `occupe`, `partiellement_disponible`

### Number Filters

- `minFollowers` - Minimum total followers
- `maxFollowers` - Maximum total followers
- `minEngagement` - Minimum engagement rate
- `maxEngagement` - Maximum engagement rate

### Date Filters

- `createdAt` - Exact, gte (greater than or equal), lte (less than or equal)
- `updatedAt` - Exact, gte, lte

### Ordering

- `orderBy` - Sort results by field (prefix with `-` for descending)

## Comparison with Category Queries

The influencer queries now follow the same pattern as category queries:

| Feature                     | Category | Influencer |
| --------------------------- | -------- | ---------- |
| Relay Connection            | ✅       | ✅         |
| totalCount                  | ✅       | ✅         |
| Pagination                  | ✅       | ✅         |
| Filtering                   | ✅       | ✅         |
| Ordering                    | ✅       | ✅         |
| DjangoFilterConnectionField | ✅       | ✅         |

Both now use `DjangoFilterConnectionField` which provides:

- Automatic pagination with cursor-based navigation
- totalCount for showing total results
- Advanced filtering through FilterSet classes
- Consistent API across different entity types
