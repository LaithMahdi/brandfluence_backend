#!/usr/bin/env python
"""
Test Django admin login
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

def test_admin_login():
    """Test if admin can authenticate"""
    
    print("\n=== Testing Django Admin Login ===\n")
    
    email = input("Enter admin email (default: admin@brandfluence.com): ").strip()
    if not email:
        email = 'admin@brandfluence.com'
    
    password = input("Enter admin password: ").strip()
    
    print(f"\nAttempting to authenticate: {email}")
    
    # Test authentication
    user = authenticate(username=email, password=password)
    
    if user is not None:
        print("\n✅ Authentication SUCCESSFUL!")
        print(f"\nUser Details:")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name}")
        print(f"  Role: {user.role}")
        print(f"\nPermissions:")
        print(f"  is_active: {user.is_active} {'✅' if user.is_active else '❌'}")
        print(f"  is_staff: {user.is_staff} {'✅' if user.is_staff else '❌'}")
        print(f"  is_superuser: {user.is_superuser} {'✅' if user.is_superuser else '❌'}")
        
        if user.is_staff:
            print("\n✅ User can access Django admin!")
            print(f"\n🌐 Login at: http://127.0.0.1:8000/admin/")
            print(f"📧 Email: {user.email}")
            print(f"🔑 Password: {password}")
        else:
            print("\n❌ User cannot access Django admin (is_staff=False)")
    else:
        print("\n❌ Authentication FAILED!")
        print("\nPossible reasons:")
        print("  1. Incorrect password")
        print("  2. User does not exist")
        print("  3. User account is disabled")
        
        # Try to find the user
        try:
            user = User.objects.get(email=email)
            print(f"\n✅ User exists in database")
            print(f"   is_active: {user.is_active}")
            print(f"   is_banned: {user.is_banned}")
            print("\n   → Password is incorrect. Reset it with:")
            print(f"     python reset_admin_quick.py {email} YourNewPassword")
        except User.DoesNotExist:
            print(f"\n❌ User {email} not found in database")
            print("\n   → Create a superuser with:")
            print("     python manage.py createsuperuser")

if __name__ == '__main__':
    try:
        test_admin_login()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
