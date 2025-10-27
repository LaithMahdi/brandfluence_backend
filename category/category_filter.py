from django_filters import FilterSet, OrderingFilter, CharFilter, BooleanFilter, DateTimeFilter
from .models import Category


class CategoryFilter(FilterSet):
    """Filters for searching and filtering categories in GraphQL queries"""
    
    name_contains = CharFilter(field_name='name', lookup_expr='icontains')
    description_contains = CharFilter(field_name='description', lookup_expr='icontains')
    is_active = BooleanFilter(field_name='is_active')
    created_after = DateTimeFilter(field_name='created', lookup_expr='gte')
    created_before = DateTimeFilter(field_name='created', lookup_expr='lte')
    modified_after = DateTimeFilter(field_name='modified', lookup_expr='gte')
    modified_before = DateTimeFilter(field_name='modified', lookup_expr='lte')
    
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