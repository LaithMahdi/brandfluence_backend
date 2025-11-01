#!/usr/bin/env python
"""
Generate a fresh JWT token for testing
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from datetime import datetime

User = get_user_model()

def generate_token():
    """Generate a fresh JWT token"""
    
    email = "mahdilaith@gmail.com"
    
    try:
        user = User.objects.get(email=email)
        
        # Generate token
        token = get_token(user)
        
        print("=== Fresh JWT Token Generated ===\n")
        print(f"User: {user.email}")
        print(f"Role: {user.role}")
        print(f"Generated at: {datetime.now()}\n")
        print("=" * 50)
        print("TOKEN:")
        print("=" * 50)
        print(token)
        print("=" * 50)
        print("\n✅ Copy the token above and use it in your GraphQL interface")
        print("\nIn GraphQL Headers (JSON format):")
        print('{\n  "Authorization": "JWT ' + token + '"\n}')
        
    except User.DoesNotExist:
        print(f"❌ User not found: {email}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    generate_token()
