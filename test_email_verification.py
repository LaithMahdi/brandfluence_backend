"""
Test script for email verification system
Run this to test if everything is set up correctly
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.utils import generate_verification_token, send_verification_email, verify_email_token
from django.conf import settings

User = get_user_model()

def test_email_configuration():
    """Test if email is configured correctly"""
    print("\n=== Testing Email Configuration ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
    print("✓ Email configuration loaded successfully\n")

def test_token_generation():
    """Test token generation"""
    print("=== Testing Token Generation ===")
    
    # Create a test user (or get existing)
    try:
        user = User.objects.filter(email='test@example.com').first()
        if not user:
            print("No test user found. Create one first using registerUser mutation.")
            return None
        
        # Generate token
        verify_token = generate_verification_token(user)
        print(f"✓ Token generated successfully: {verify_token.token}")
        print(f"✓ Expires at: {verify_token.expires_at}")
        print(f"✓ Is used: {verify_token.is_used}")
        
        return verify_token
    except Exception as e:
        print(f"✗ Error generating token: {str(e)}")
        return None

def test_email_sending(test_email=None):
    """Test sending verification email"""
    print("\n=== Testing Email Sending ===")
    
    if not test_email:
        print("Please provide a test email address as argument")
        return
    
    try:
        user = User.objects.filter(email=test_email).first()
        if not user:
            print(f"✗ No user found with email: {test_email}")
            return
        
        # Generate token
        verify_token = generate_verification_token(user)
        
        # Send email
        success = send_verification_email(user, verify_token.token)
        
        if success:
            print(f"✓ Email sent successfully to {test_email}")
            print(f"✓ Verification link: {settings.FRONTEND_URL}/verify-email/{verify_token.token}?email={user.email}")
        else:
            print("✗ Failed to send email")
    except Exception as e:
        print(f"✗ Error sending email: {str(e)}")

def test_token_verification():
    """Test token verification"""
    print("\n=== Testing Token Verification ===")
    
    try:
        user = User.objects.filter(email='test@example.com').first()
        if not user:
            print("No test user found")
            return
        
        # Generate and verify token
        verify_token = generate_verification_token(user)
        success, message, verified_user = verify_email_token(verify_token.token, user.email)
        
        if success:
            print(f"✓ Token verification successful")
            print(f"✓ Message: {message}")
            print(f"✓ User email verified: {verified_user.email_verified}")
        else:
            print(f"✗ Token verification failed: {message}")
    except Exception as e:
        print(f"✗ Error verifying token: {str(e)}")

if __name__ == '__main__':
    print("=" * 50)
    print("EMAIL VERIFICATION SYSTEM TEST")
    print("=" * 50)
    
    # Test 1: Configuration
    test_email_configuration()
    
    # Test 2: Token Generation
    token = test_token_generation()
    
    # Test 3: Token Verification
    test_token_verification()
    
    # Test 4: Email Sending (uncomment and add your email to test)
    # test_email_sending('your-email@example.com')
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)
    print("\nTo test email sending, uncomment the last line in the script")
    print("and replace 'your-email@example.com' with your actual email.")
