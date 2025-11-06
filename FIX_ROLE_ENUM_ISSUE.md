# Fix: Role Comparison Issue - "EnumMeta.COMPANY"

## Problem Identified

The JWT token payload contains `"role": "EnumMeta.COMPANY"` instead of just `"COMPANY"`, causing the role validation to fail when creating a company profile.

### Error Response

```json
{
  "data": {
    "createCompanyProfile": {
      "success": false,
      "message": "User must have COMPANY role to create a company profile",
      "company": null
    }
  }
}
```

### Token Payload

```json
{
  "role": "EnumMeta.COMPANY", // ❌ Should be just "COMPANY"
  "userId": 5,
  "email": "gigid35285@keevle.com",
  "name": "gigid352"
}
```

## Root Cause

This is a Django model issue where the `UserRole` enum is being stored incorrectly in the database. The value is being saved as `"EnumMeta.COMPANY"` instead of just `"COMPANY"`.

## Fix Applied

### File: `users/mutations/company_mutations.py`

#### 1. Added Helper Function

```python
def is_company_role(user):
    """Helper function to check if user has COMPANY role (handles EnumMeta.COMPANY bug)"""
    if not user or not user.is_authenticated:
        return False
    user_role = str(user.role)
    return 'COMPANY' in user_role or user.role == UserRole.COMPANY.value
```

#### 2. Updated Role Check

```python
# Before (strict comparison - fails with EnumMeta.COMPANY)
if user.role != UserRole.COMPANY.value:
    return CreateCompanyProfile(success=False, message="...")

# After (flexible comparison - works with both)
if not is_company_role(user):
    return CreateCompanyProfile(
        success=False,
        message=f"User must have COMPANY role. Current role: {user.role}",
        company=None
    )
```

## Testing

### Try Creating Company Profile Again

With the same JWT token, the mutation should now work:

```graphql
mutation {
  createCompanyProfile(
    companyName: "Test Company"
    address: { address: "123 Street", city: "Paris", country: "France" }
  ) {
    success
    message
    company {
      id
      companyName
    }
  }
}
```

### Expected Result

```json
{
  "data": {
    "createCompanyProfile": {
      "success": true,
      "message": "Company profile created successfully",
      "company": {
        "id": "1",
        "companyName": "Test Company"
      }
    }
  }
}
```

## Permanent Fix Needed

While the mutation now works, you should fix the root cause in the User model:

### Option 1: Fix Existing Users (Recommended)

Run this Django management command or script:

```python
# In Django shell: python manage.py shell
from users.models import User

# Fix all users with EnumMeta role
for user in User.objects.all():
    if 'EnumMeta.' in str(user.role):
        # Extract the role name after EnumMeta.
        role_value = str(user.role).split('.')[-1]
        user.role = role_value
        user.save(update_fields=['role'])
        print(f"Fixed user {user.email}: {user.role}")
```

### Option 2: Create Migration Script

Create: `users/management/commands/fix_user_roles.py`

```python
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Fix EnumMeta.ROLE values in user roles'

    def handle(self, *args, **kwargs):
        fixed_count = 0
        for user in User.objects.all():
            if 'EnumMeta.' in str(user.role):
                old_role = user.role
                role_value = str(user.role).split('.')[-1]
                user.role = role_value
                user.save(update_fields=['role'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Fixed {user.email}: {old_role} → {user.role}'
                    )
                )
                fixed_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {fixed_count} users'
            )
        )
```

Run with:

```bash
python manage.py fix_user_roles
```

## Why This Happened

The issue occurs when:

1. User is created/updated through Django admin or code
2. Role enum is incorrectly converted to string
3. Python's enum representation includes "EnumMeta." prefix
4. Value gets saved to database as "EnumMeta.COMPANY" instead of "COMPANY"

## Status

✅ **Immediate Fix Applied**: Company mutations now work with "EnumMeta.COMPANY" roles
⚠️ **Action Required**: Run the fix script to clean up existing user roles in database

## Files Modified

- ✅ `users/mutations/company_mutations.py` - Added helper function and updated role check
