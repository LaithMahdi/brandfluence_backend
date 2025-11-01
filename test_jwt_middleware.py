#!/usr/bin/env python
"""
Test JWT authentication in GraphQL context
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from graphql_jwt.middleware import JSONWebTokenMiddleware

User = get_user_model()

def test_jwt_auth():
    """Test if JWT middleware properly authenticates the user"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ1NDU4LCJvcmlnSWF0IjoxNzYxOTQxODU4fQ.gA0g6dXWL1W-I_Yu5zQ9xIPGkiPzLQZp15caktUdZvM"
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.post('/graphql/', 
                          content_type='application/json',
                          HTTP_AUTHORIZATION=f'JWT {token}')
    
    print("=== Testing JWT Middleware ===")
    print(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
    
    # Try to get user from middleware
    try:
        from graphql_jwt.utils import get_payload, get_user_by_payload
        from graphql_jwt.exceptions import JSONWebTokenError
        
        try:
            payload = get_payload(token)
            print(f"\n✅ Payload extracted: {payload}")
            
            user = get_user_by_payload(payload)
            print(f"\n✅ User authenticated from JWT:")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.role}")
            print(f"   Is authenticated: {user.is_authenticated}")
            
            # Test the query condition
            if not user.is_authenticated:
                print("\n❌ user.is_authenticated is False!")
            elif user.role != 'INFLUENCER':
                print(f"\n❌ user.role is '{user.role}', not 'INFLUENCER'!")
            else:
                print("\n✅ User passes all checks - query should work!")
                
        except JSONWebTokenError as e:
            print(f"\n❌ JWT Error: {e}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_jwt_auth()
