#!/usr/bin/env python
"""
Test the myInfluencerProfile query
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.influencer_models import Influencer

User = get_user_model()

def test_influencer_query():
    """Test if influencer profile exists for the user"""
    
    # Find user by email from the JWT token
    email = "mahdilaith@gmail.com"
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ User found: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Is authenticated: {user.is_authenticated}")
        print(f"   Profile completed: {user.is_completed_profile}")
        
        if user.role != 'INFLUENCER':
            print(f"\n❌ User is not an influencer! Role is: {user.role}")
            return
        
        # Check if influencer profile exists
        try:
            influencer = Influencer.objects.get(user=user)
            print(f"\n✅ Influencer profile found!")
            print(f"   ID: {influencer.id}")
            print(f"   Pseudo: {influencer.pseudo}")
            print(f"   Instagram: {influencer.instagram_username}")
            print(f"   Location: {influencer.localisation}")
            print(f"   Biography: {influencer.biography[:100] if influencer.biography else 'None'}...")
            
            # Check related data
            print(f"\n📊 Related Data:")
            print(f"   Images: {influencer.images.count()}")
            print(f"   Instagram Reels: {influencer.instagram_reels.count()}")
            print(f"   Instagram Posts: {influencer.instagram_posts.count()}")
            print(f"   Social Networks: {influencer.reseaux_sociaux.count()}")
            print(f"   Categories: {influencer.selected_categories.count()}")
            print(f"   Portfolio Media: {influencer.portfolio_media.count()}")
            
        except Influencer.DoesNotExist:
            print(f"\n❌ Influencer profile not found for this user!")
            print(f"   User needs to complete the profile first.")
            
    except User.DoesNotExist:
        print(f"❌ User not found with email: {email}")

if __name__ == '__main__':
    try:
        test_influencer_query()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
