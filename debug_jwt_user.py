#!/usr/bin/env python
"""
Test what user the JWT middleware returns
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from graphql_jwt.utils import get_payload, get_user_by_payload
from django.contrib.auth import get_user_model

User = get_user_model()

def test_jwt_user():
    """Test what user the JWT returns"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ3NjEwLCJvcmlnSWF0IjoxNzYxOTQ0MDEwLCJuYW1lIjoiTGFpdGggTWFoZGkiLCJyb2xlIjoiSU5GTFVFTkNFUiIsInVzZXJJZCI6MX0.5TwUjJm-YOobYV-bFmeumuuV0HNQDqX7K9T02jFbV1I"
    
    try:
        payload = get_payload(token)
        print("=== JWT Payload ===")
        print(f"role in payload: {payload.get('role')}")
        print(f"userId in payload: {payload.get('userId')}")
        
        print("\n=== Getting User from JWT ===")
        user = get_user_by_payload(payload)
        print(f"User: {user}")
        print(f"User ID: {user.id}")
        print(f"User email: {user.email}")
        print(f"User role: {user.role}")
        print(f"User role type: {type(user.role)}")
        print(f"User role repr: {repr(user.role)}")
        
        print("\n=== Checking Database ===")
        db_user = User.objects.get(pk=user.pk)
        print(f"DB User role: {db_user.role}")
        print(f"DB User role type: {type(db_user.role)}")
        print(f"DB User role repr: {repr(db_user.role)}")
        
        print("\n=== Comparison ===")
        print(f"user.role == 'INFLUENCER': {user.role == 'INFLUENCER'}")
        print(f"user.role == 'ADMIN': {user.role == 'ADMIN'}")
        print(f"str(user.role) == 'INFLUENCER': {str(user.role) == 'INFLUENCER'}")
        print(f"str(user.role) == 'ADMIN': {str(user.role) == 'ADMIN'}")
        
        # Check if it's the right user
        print(f"\n=== Is this user ID 1? ===")
        print(f"user.id == 1: {user.id == 1}")
        
        # Check all users with ID 1
        all_user_1 = User.objects.filter(pk=1)
        for u in all_user_1:
            print(f"\nUser ID 1 in database:")
            print(f"  Email: {u.email}")
            print(f"  Name: {u.name}")
            print(f"  Role: {u.role}")
            print(f"  Is Staff: {u.is_staff}")
            print(f"  Is Superuser: {u.is_superuser}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_jwt_user()
