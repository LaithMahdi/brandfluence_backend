from django_filters import FilterSet, OrderingFilter, CharFilter, NumberFilter, DateFilter, DateTimeFilter
from ..models import Offer


class OfferFilter(FilterSet):
    """Filters for searching and filtering offers in GraphQL queries"""
    
    class Meta:
        model = Offer
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'min_budget': ['exact', 'gte', 'lte'],
            'max_budget': ['exact', 'gte', 'lte'],
            'start_date': ['exact', 'gte', 'lte'],
            'end_date': ['exact', 'gte', 'lte'],
            'influencer_number': ['exact', 'gte', 'lte'],
            'requirement': ['exact', 'icontains'],
            'objectif': ['exact', 'icontains'],
            'created_at': ['exact', 'gte', 'lte'],
            'created_by': ['exact'],
        }
        
    ordering = OrderingFilter(
        fields=(
            ('title', 'title'),
            ('min_budget', 'min_budget'),
            ('max_budget', 'max_budget'),
            ('start_date', 'start_date'),
            ('end_date', 'end_date'),
            ('influencer_number', 'influencer_number'),
            ('created_at', 'created_at'),
        )
    )
