#!/usr/bin/env python
"""
Test BOTH tokens to see which is which
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from graphql_jwt.utils import get_payload, get_user_by_payload

def test_token(token, label):
    """Test what user a token belongs to"""
    print(f"\n{'=' * 70}")
    print(f"{label}")
    print(f"{'=' * 70}")
    print(f"Token: {token[:50]}...")
    
    try:
        payload = get_payload(token)
        email = payload.get('email')
        print(f"✅ Token is valid")
        print(f"   Email in payload: {email}")
        
        user = get_user_by_payload(payload)
        print(f"   User found: {user.email}")
        print(f"   User role: {user.role}")
        print(f"   User name: {user.name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("\n🔍 Testing Tokens\n")
    
    # OLD token (the one causing issues)
    old_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ1NDU4LCJvcmlnSWF0IjoxNzYxOTQxODU4fQ.gA0g6dXWL1W-I_Yu5zQ9xIPGkiPzLQZp15caktUdZvM"
    test_token(old_token, "OLD TOKEN (DO NOT USE)")
    
    # NEW token (the correct one)
    new_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ3MzQ0LCJvcmlnSWF0IjoxNzYxOTQzNzQ0fQ.wLTg8ZPvCeIHcyK95rrfDITFqeZADAQZNdVebWZbThQ"
    test_token(new_token, "NEW TOKEN (USE THIS ONE)")
    
    print("\n" + "=" * 70)
    print("✅ USE THE NEW TOKEN ABOVE IN YOUR GRAPHQL INTERFACE")
    print("=" * 70)
    print("\nCopy this exact line into HTTP Headers:\n")
    print('{\n  "Authorization": "JWT ' + new_token + '"\n}')
