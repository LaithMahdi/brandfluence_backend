"""Utility functions for user management"""
import uuid
import random
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.apps import apps
from graphql_jwt.utils import jwt_payload as default_jwt_payload


def jwt_payload_handler(user, context=None):
    """
    Custom JWT payload handler to include name, email, and role in token
    
    Args:
        user: User instance
        context: GraphQL context (optional)
        
    Returns:
        Dictionary with JWT payload
    """
    # Get default payload (includes username, exp, origIat)
    payload = default_jwt_payload(user, context)
    
    # Add custom fields
    payload['email'] = user.email
    payload['name'] = user.name
    payload['role'] = user.role
    payload['userId'] = user.id
    
    return payload


def generate_verification_code():
    """Generate a random 6-digit verification code"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def generate_verification_token(user):
    """
    Generate a unique verification token and code for a user
    
    Args:
        user: User instance
        
    Returns:
        VerifyToken instance
    """
    VerifyToken = apps.get_model('users', 'VerifyToken')
    
    # Generate unique token
    token = str(uuid.uuid4())
    
    # Generate 6-digit code
    code = generate_verification_code()
    
    # Set expiration (24 hours from now)
    expires_at = timezone.now() + timedelta(hours=24)
    
    # Create verification token
    verify_token = VerifyToken.objects.create(
        user=user,
        token=token,
        code=code,
        expires_at=expires_at
    )
    
    return verify_token


def send_verification_email(user, token, code):
    """
    Send verification email to user
    
    Args:
        user: User instance
        token: Token string
        code: 6-digit verification code
        
    Returns:
        Boolean indicating success
    """
    try:
        # Generate verification link
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{token}?email={user.email}"
        
        # Render HTML email
        html_message = render_to_string('emails/verify_email.html', {
            'user_name': user.name,
            'verification_link': verification_link,
            'verification_code': code,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject='Verify Your Email - BrandFluence',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False


def verify_email_token(token, email):
    """
    Verify an email token
    
    Args:
        token: Token string
        email: User email
        
    Returns:
        Tuple of (success: bool, message: str, user: User or None)
    """
    VerifyToken = apps.get_model('users', 'VerifyToken')
    
    try:
        # Get the verification token
        verify_token = VerifyToken.objects.get(
            token=token,
            user__email=email
        )
        
        # Check if token is already used
        if verify_token.is_used:
            return False, "This verification link has already been used.", None
        
        # Check if token is expired
        if verify_token.expires_at < timezone.now():
            return False, "This verification link has expired. Please request a new one.", None
        
        # Get the user
        user = verify_token.user
        
        # Mark token as used
        verify_token.mark_as_used()
        
        # Verify the user's email
        user.verify_email()
        
        return True, "Email verified successfully! You can now log in.", user
        
    except VerifyToken.DoesNotExist:
        return False, "Invalid verification link.", None
    except Exception as e:
        print(f"Error verifying email token: {str(e)}")
        return False, "An error occurred while verifying your email.", None


def verify_email_code(code, email):
    """
    Verify an email using 6-digit code
    
    Args:
        code: 6-digit verification code
        email: User email
        
    Returns:
        Tuple of (success: bool, message: str, user: User or None)
    """
    VerifyToken = apps.get_model('users', 'VerifyToken')
    
    try:
        # Get the verification token by code and email
        verify_token = VerifyToken.objects.filter(
            code=code,
            user__email=email,
            is_used=False
        ).order_by('-created_at').first()
        
        if not verify_token:
            return False, "Invalid verification code.", None
        
        # Check if token is expired
        if verify_token.expires_at < timezone.now():
            return False, "This verification code has expired. Please request a new one.", None
        
        # Get the user
        user = verify_token.user
        
        # Mark token as used
        verify_token.mark_as_used()
        
        # Verify the user's email
        user.verify_email()
        
        return True, "Email verified successfully! You can now log in.", user
        
    except Exception as e:
        print(f"Error verifying email code: {str(e)}")
        return False, "An error occurred while verifying your email.", None
