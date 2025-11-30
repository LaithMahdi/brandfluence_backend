from django_filters import FilterSet, OrderingFilter, CharFilter, NumberFilter, DateFilter
from ..models import Offer

class OfferFilter(FilterSet):
    """Filters for searching and filtering offers in GraphQL queries"""
    
    title = CharFilter(field_name='title', lookup_expr='icontains')
    min_budget = NumberFilter(field_name='min_budget', lookup_expr='gte')
    max_budget = NumberFilter(field_name='max_budget', lookup_expr='lte')
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    created_by = CharFilter(field_name='created_by__username', lookup_expr='icontains')
    
    class Meta:
        model = Offer
        fields = ['title', 'min_budget', 'max_budget', 'start_date', 'end_date', 'created_by']
        
    ordering = OrderingFilter(
        fields=(
            ('title', 'title'),
            ('min_budget', 'min_budget'),
            ('max_budget', 'max_budget'),
            ('start_date', 'start_date'),
            ('end_date', 'end_date'),
            ('created_at', 'created_at'),
        )
    )
