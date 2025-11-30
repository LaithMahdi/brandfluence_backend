from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from enum import Enum


class UserRole(Enum):
    ADMIN = "ADMIN"
    COMPANY = "COMPANY"
    INFLUENCER = "INFLUENCER"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]


class CustomUserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verify_by_admin', True)
        extra_fields.setdefault('email_verified', True)
        extra_fields.setdefault('role', UserRole.ADMIN.value)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as username and role-based access"""

    email = models.EmailField(unique=True, max_length=255, db_index=True)
    name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number_verified = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_verify_by_admin = models.BooleanField(default=False)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices(),
        default=UserRole.INFLUENCER.value
    )

    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_completed_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"

    def verify_email(self):
        self.email_verified = True
        self.verified_at = timezone.now()
        self.save(update_fields=['email_verified', 'verified_at'])

    def verify_phone(self):
        self.phone_number_verified = True
        self.save(update_fields=['phone_number_verified'])

    def ban_user(self):
        self.is_banned = True
        self.is_active = False
        self.save(update_fields=['is_banned', 'is_active'])

    def unban_user(self):
        self.is_banned = False
        self.is_active = True
        self.save(update_fields=['is_banned', 'is_active'])

    def admin_verify(self):
        self.is_verify_by_admin = True
        self.save(update_fields=['is_verify_by_admin'])

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    @property
    def is_company(self):
        return self.role == UserRole.COMPANY.value

    @property
    def is_influencer(self):
        return self.role == UserRole.INFLUENCER.value


class VerifyToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_tokens')
    token = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'verify_tokens'
        verbose_name = 'Verify Token'
        verbose_name_plural = 'Verify Tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"Token for {self.user.email} - Code: {self.code} - Used: {self.is_used}"

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True, db_index=True)
    code = models.CharField(max_length=6, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"Password Reset for {self.user.email} - Code: {self.code} - Used: {self.is_used}"

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])
