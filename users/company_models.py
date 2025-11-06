from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from .influencer_models import Image


User = get_user_model()


class Address(models.Model):
    """Address model for companies"""
    
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"


class Company(models.Model):
    """Company profile extending User model"""

    COMPANY_SIZES = [
        ('S', 'Small (1-50 employees)'),
        ('M', 'Medium (51-200 employees)'),
        ('L', 'Large (201-1000 employees)'),
        ('XL', 'Extra Large (1001+ employees)'),
    ]

    DOMAIN_ACTIVITIES = [
        ('TECH', 'Technology'), 
        ('FIN', 'Finance'), 
        ('HLTH', 'Healthcare'), 
        ('EDU', 'Education'), 
        ('ENT', 'Entertainment'), 
        ('MFG', 'Manufacturing'),
        ('RET', 'Retail'),
        ('OTH', 'Other'),
    ]

    ENTREPRISE_TYPES = [
        ('PRIV', 'Private'),
        ('PUB', 'Public'),
        ('NGO', 'Non-Governmental Organization'),
        ('GOV', 'Government Agency'),
    ]
    
    DISPONIBILITE_CHOICES = [
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('partiellement_disponible', 'Partiellement disponible'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')

    # Basic Information
    company_name = models.CharField(max_length=150)
    matricule = models.CharField(max_length=100, unique=True, blank=True, null=True)
    website = models.URLField(max_length=1000, blank=True, null=True)
    
    size = models.CharField(
        max_length=2,
        choices=COMPANY_SIZES,
        blank=True,
        null=True
    )
    
    description = models.TextField(blank=True, null=True)

    domain_activity = models.CharField(
        max_length=4,
        choices=DOMAIN_ACTIVITIES,
        blank=True,
        null=True
    )

    contact_email = models.EmailField(max_length=254, blank=True, null=True)

    entreprise_type = models.CharField(
        max_length=4,
        choices=ENTREPRISE_TYPES,
        blank=True,
        null=True
    )
    
    # Address relation
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name='company',
        blank=True,
        null=True
    )

    langues = models.JSONField(default=list, blank=True)

    disponibilite_collaboration = models.CharField(
        max_length=50,
        choices=DISPONIBILITE_CHOICES,
        default='disponible'
    )
    
    # Generic relation to images
    images = GenericRelation(Image, related_query_name='company')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"





