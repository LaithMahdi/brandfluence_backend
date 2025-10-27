"""
Django filters for Category model.

This module defines filtering options for Category GraphQL queries,
providing flexible search and filter capabilities.
"""
from django_filters import (
    FilterSet, 
    OrderingFilter, 
    CharFilter, 
    BooleanFilter,
    DateTimeFilter
)
from .models import Category


class CategoryFilter(FilterSet):
    """
    Filter class for Category model.
    
    Provides comprehensive filtering options for category queries
    including text search, status filtering, and date range filtering.
    """
    
    # Custom filters
    name_contains = CharFilter(
        field_name='name', 
        lookup_expr='icontains',
        help_text='Filter by name containing the given text (case-insensitive)'
    )
    
    description_contains = CharFilter(
        field_name='description', 
        lookup_expr='icontains',
        help_text='Filter by description containing the given text (case-insensitive)'
    )
    
    is_active = BooleanFilter(
        field_name='is_active',
        help_text='Filter by active status'
    )
    
    created_after = DateTimeFilter(
        field_name='created',
        lookup_expr='gte',
        help_text='Filter categories created after the given date'
    )
    
    created_before = DateTimeFilter(
        field_name='created',
        lookup_expr='lte',
        help_text='Filter categories created before the given date'
    )
    
    modified_after = DateTimeFilter(
        field_name='modified',
        lookup_expr='gte',
        help_text='Filter categories modified after the given date'
    )
    
    modified_before = DateTimeFilter(
        field_name='modified',
        lookup_expr='lte',
        help_text='Filter categories modified before the given date'
    )
    
    class Meta:
        model = Category
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'is_active': ['exact'],
            'created': ['exact', 'gte', 'lte'],
            'modified': ['exact', 'gte', 'lte'],
        }
        
    # Ordering options
    ordering = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('created', 'created'),
            ('modified', 'modified'),
            ('is_active', 'is_active'),
        ),
        field_labels={
            'name': 'Name',
            'created': 'Creation Date',
            'modified': 'Modification Date',
            'is_active': 'Active Status',
        },
        help_text='Order results by the specified field'
    )