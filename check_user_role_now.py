#!/usr/bin/env python
"""
Verify the exact user state in database RIGHT NOW
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def check_user():
    """Check user state"""
    
    email = "mahdilaith@gmail.com"
    
    try:
        user = User.objects.get(email=email)
        
        print("=== Current Database State ===")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Role repr: {repr(user.role)}")
        print(f"Role type: {type(user.role)}")
        print(f"Role == 'INFLUENCER': {user.role == 'INFLUENCER'}")
        print(f"Role == 'ADMIN': {user.role == 'ADMIN'}")
        print(f"str(role): {str(user.role)}")
        
        # Check if it's a database issue
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT email, role FROM users WHERE email = %s", [email])
            row = cursor.fetchone()
            print(f"\n=== Direct Database Query ===")
            print(f"Email: {row[0]}")
            print(f"Role (raw): {row[1]}")
        
    except User.DoesNotExist:
        print(f"❌ User not found: {email}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_user()
