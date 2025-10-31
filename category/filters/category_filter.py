from django_filters import FilterSet, OrderingFilter, CharFilter, BooleanFilter, DateTimeFilter
from ..models import Category


class CategoryFilter(FilterSet):
    """Filters for searching and filtering categories in GraphQL queries"""
    
    class Meta:
        model = Category
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'is_active': ['exact'],
            'created': ['exact', 'gte', 'lte'],
            'modified': ['exact', 'gte', 'lte'],
        }
        
    ordering = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('created', 'created'),
            ('modified', 'modified'),
            ('is_active', 'is_active'),
        )
    )
