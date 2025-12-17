# Role Corruption Fix - Summary

## Problem

Users were experiencing authentication errors when trying to complete their influencer profiles. The error message was:

```
"This action is only available for influencer accounts"
```

## Root Cause

The user roles in the database were corrupted with the value `'EnumMeta.INFLUENCER'` instead of just `'INFLUENCER'`. This happened because somewhere in the code, the enum's string representation was being saved instead of just the value.

### Example of Corrupted Data:

- **Expected**: `role = 'INFLUENCER'`
- **Actual**: `role = 'EnumMeta.INFLUENCER'`

## Solution Implemented

### 1. Created Utility Functions (`users/utils.py`)

Added two new helper functions:

```python
def normalize_role(role):
    """
    Normalize role value to handle corrupted data.
    Converts 'EnumMeta.INFLUENCER' -> 'INFLUENCER'
    """
    if not role:
        return role
    return role.split('.')[-1] if '.' in role else role


def check_user_role(user, expected_role):
    """
    Check if user has the expected role, handling corrupted role values.
    """
    user_role = normalize_role(user.role)
    return user_role == expected_role
```

### 2. Updated All Role Checks

Updated the following files to use the new utility functions:

#### Files Modified:

1. **users/mutations/influencer_mutations_all.py**

   - Updated `CompleteInfluencerProfile` mutation
   - Added imports for `normalize_role` and `check_user_role`
   - Changed role check from direct comparison to using `check_user_role()`

2. **users/queries/influencer_queries.py**

   - Updated `resolve_current_influencer_profile` query
   - Updated `resolve_influencer_by_user` query
   - Added imports for utility functions

3. **users/user_node.py**

   - Updated `resolve_influencer_profile` resolver
   - Now uses `check_user_role()` for role validation

4. **users/utils.py**
   - Updated `jwt_payload_handler` to normalize role in JWT tokens
   - This ensures JWTs contain clean role values

### 3. Created Database Cleanup Script

Created `fix_corrupted_roles.py` to clean up existing corrupted data in the database:

```python
# Run this script to fix all corrupted roles in the database
python fix_corrupted_roles.py
```

This script:

- Finds all users with roles containing 'EnumMeta.'
- Converts them to clean values (e.g., 'EnumMeta.INFLUENCER' -> 'INFLUENCER')
- Updates the database
- Provides a summary of changes

## Testing the Fix

### Immediate Fix (Already Applied)

The code changes allow the application to work with both:

- Clean roles: `'INFLUENCER'`, `'COMPANY'`, `'ADMIN'`
- Corrupted roles: `'EnumMeta.INFLUENCER'`, `'EnumMeta.COMPANY'`, etc.

### Permanent Fix (Recommended)

Run the database cleanup script:

```bash
cd c:\Users\SBS\Music\brandfluence
python fix_corrupted_roles.py
```

This will permanently fix the data in the database.

## Prevention

To prevent this issue in the future, always ensure that when saving enum values to the database, you use `.value`:

```python
# CORRECT ✓
user.role = UserRole.INFLUENCER.value  # Saves 'INFLUENCER'

# WRONG ✗
user.role = str(UserRole.INFLUENCER)   # Might save 'EnumMeta.INFLUENCER'
user.role = UserRole.INFLUENCER        # Might cause issues
```

## Files Changed

1. `users/utils.py` - Added utility functions
2. `users/mutations/influencer_mutations_all.py` - Updated mutation
3. `users/queries/influencer_queries.py` - Updated queries
4. `users/user_node.py` - Updated resolver
5. `fix_corrupted_roles.py` - New cleanup script
6. `check_user_role.py` - Debug script

## Next Steps

1. ✅ Code changes applied (application now handles corrupted roles)
2. ⏳ Run `fix_corrupted_roles.py` to clean up the database
3. ⏳ Test the `completeInfluencerProfile` mutation again
4. ⏳ Monitor for any similar issues with COMPANY or ADMIN roles
