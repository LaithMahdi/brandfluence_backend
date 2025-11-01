#!/usr/bin/env python
"""
Decode JWT token and check user
"""
import os
import sys
import django
import jwt
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def decode_token():
    """Decode the JWT token"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haGRpbGFpdGhAZ21haWwuY29tIiwiZXhwIjoxNzYxOTQ1NDU4LCJvcmlnSWF0IjoxNzYxOTQxODU4fQ.gA0g6dXWL1W-I_Yu5zQ9xIPGkiPzLQZp15caktUdZvM"
    
    try:
        # Decode without verification first to see payload
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        print("=== JWT Token Payload ===")
        print(f"Email: {decoded.get('email')}")
        print(f"Expiration: {datetime.fromtimestamp(decoded.get('exp'))}")
        print(f"Issued at: {datetime.fromtimestamp(decoded.get('origIat'))}")
        
        # Check if token is expired
        exp_timestamp = decoded.get('exp')
        current_timestamp = datetime.now().timestamp()
        
        if current_timestamp > exp_timestamp:
            print("\n❌ TOKEN IS EXPIRED!")
            print(f"   Expired at: {datetime.fromtimestamp(exp_timestamp)}")
            print(f"   Current time: {datetime.now()}")
        else:
            print(f"\n✅ Token is valid (expires in {int((exp_timestamp - current_timestamp) / 60)} minutes)")
        
        # Check user in database
        email = decoded.get('email')
        try:
            user = User.objects.get(email=email)
            print(f"\n=== User Information ===")
            print(f"Email: {user.email}")
            print(f"Name: {user.name}")
            print(f"Role: {user.role}")
            print(f"Is Active: {user.is_active}")
            print(f"Is Staff: {user.is_staff}")
            print(f"Profile Completed: {user.is_completed_profile}")
            
            if user.role != 'INFLUENCER':
                print(f"\n❌ USER ROLE IS NOT 'INFLUENCER'!")
                print(f"   Current role: {user.role}")
                print(f"\n🔧 To fix, run:")
                print(f"   user = User.objects.get(email='{email}')")
                print(f"   user.role = 'INFLUENCER'")
                print(f"   user.save()")
            else:
                print(f"\n✅ User role is correct: INFLUENCER")
                
        except User.DoesNotExist:
            print(f"\n❌ User not found with email: {email}")
            
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    decode_token()
