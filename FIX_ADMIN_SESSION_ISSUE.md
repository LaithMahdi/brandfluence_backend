# SOLUTION: Clear Django Session

## The Problem

You're logged into Django admin as the ADMIN user, and the session cookie is overriding your JWT token.

## Quick Fix

### Option 1: Logout from Django Admin

1. Go to: http://127.0.0.1:8000/admin/
2. Click "Log out" in the top right
3. Go back to GraphQL interface
4. Try your query again

### Option 2: Clear Cookies

1. In your browser, press F12 (Developer Tools)
2. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
3. Under "Cookies" → "http://127.0.0.1:8000"
4. Delete these cookies:
   - sessionid
   - csrftoken
5. Refresh the GraphQL page
6. Try your query again

### Option 3: Use Incognito Mode

1. Open new Incognito/Private window
2. Go to: http://127.0.0.1:8000/graphql/
3. Add JWT token in Headers
4. Run query

## Test Query

**Headers:**

```json
{
  "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ3NzM3LCJvcmlnSWF0IjoxNzYxOTQ0MTM3LCJuYW1lIjoiTGFpdGggTWFoZGkiLCJyb2xlIjoiSU5GTFVFTkNFUiIsInVzZXJJZCI6MX0.yE2foP38rOqS64BZBhi8oL14XvvtHfTwQ3Z2L6j1zHI"
}
```

**Query:**

```graphql
query TestBasic {
  myInfluencerProfile {
    id
    pseudo
    biography
  }
}
```

## Why This Happened

Django checks authentication backends in order:

1. JWT Backend (finds no valid session, checks JWT token ✅)
2. ModelBackend (finds admin session cookie ⚠️ - this won)

When you're logged into Django admin, the session cookie takes precedence.
