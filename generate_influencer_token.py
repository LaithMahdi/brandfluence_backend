#!/usr/bin/env python
"""
Generate JWT token for influencer user
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

def generate_influencer_token():
    """Generate a fresh JWT token for the influencer"""
    
    # The influencer user
    email = "mahdilaith@gmail.com"
    
    try:
        user = User.objects.get(email=email)
        
        print(f"=== User Information ===")
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        print(f"Role: {user.role}")
        print(f"Role Type: {type(user.role)}")
        
        # Check if role is INFLUENCER
        if str(user.role) != 'INFLUENCER':
            print(f"\n⚠️  WARNING: User role is '{user.role}', not 'INFLUENCER'")
            print(f"   Fixing role...")
            user.role = 'INFLUENCER'
            user.save()
            print(f"✅ Role updated to INFLUENCER")
        
        # Refresh from database
        user.refresh_from_db()
        print(f"\n✅ After refresh - Role: {user.role}")
        
        # Generate token
        token = get_token(user)
        
        print(f"\n=== Fresh JWT Token Generated ===")
        print(f"Generated at: {datetime.now()}\n")
        print("=" * 70)
        print("TOKEN:")
        print("=" * 70)
        print(token)
        print("=" * 70)
        print("\n✅ Copy the token above and use it in your GraphQL interface")
        print("\nIn GraphQL HTTP Headers section:")
        print('{\n  "Authorization": "JWT ' + token + '"\n}')
        print("\nQuery:")
        print("""
query TestBasic {
  myInfluencerProfile {
    id
    pseudo
    biography
  }
}
        """)
        
    except User.DoesNotExist:
        print(f"❌ User not found: {email}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    generate_influencer_token()
