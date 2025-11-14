from django_filters import FilterSet, OrderingFilter, CharFilter, BooleanFilter, DateTimeFilter
from ..models import User


class UserFilter(FilterSet):
    """Filters for searching and filtering users in GraphQL queries"""
    
    class Meta:
        model = User
        fields = {
            'email': ['exact', 'icontains', 'istartswith'],
            'name': ['exact', 'icontains', 'istartswith'],
            'role': ['exact'],
            'email_verified': ['exact'],
            'phone_number_verified': ['exact'],
            'is_verify_by_admin': ['exact'],
            'is_banned': ['exact'],
            'is_active': ['exact'],
            'is_staff': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
            'updated_at': ['exact', 'gte', 'lte'],
        }
        
    ordering = OrderingFilter(
        fields=(
            ('email', 'email'),
            ('name', 'name'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('is_active', 'is_active'),
            ('role', 'role'),
        )
    )
