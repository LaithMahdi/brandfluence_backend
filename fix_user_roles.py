"""
Script to fix incorrectly stored user roles in the database.
This fixes roles stored as 'EnumMeta.COMPANY' to 'COMPANY'.

Run with: python fix_user_roles.py
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from users.models import User, UserRole


def fix_user_roles():
    """Fix all users with incorrectly stored roles"""
    users = User.objects.all()
    fixed_count = 0
    
    print("Checking user roles...")
    print("-" * 50)
    
    for user in users:
        old_role = user.role
        
        # Check if role is incorrectly formatted
        if 'EnumMeta.' in str(old_role):
            # Extract the actual role value (e.g., 'COMPANY' from 'EnumMeta.COMPANY')
            role_value = str(old_role).split('.')[-1]
            
            # Validate that it's a valid role
            valid_roles = [role.value for role in UserRole]
            if role_value in valid_roles:
                user.role = role_value
                user.save(update_fields=['role'])
                fixed_count += 1
                print(f"✓ Fixed: {user.email}")
                print(f"  Old: {old_role} → New: {role_value}")
            else:
                print(f"✗ Invalid role for {user.email}: {role_value}")
        else:
            print(f"○ OK: {user.email} - Role: {old_role}")
    
    print("-" * 50)
    print(f"\nTotal users checked: {users.count()}")
    print(f"Total users fixed: {fixed_count}")
    
    if fixed_count > 0:
        print("\n✅ Database has been updated successfully!")
    else:
        print("\n✅ All roles were already correct!")


if __name__ == '__main__':
    fix_user_roles()
