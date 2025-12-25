from django_filters import FilterSet, OrderingFilter, CharFilter, NumberFilter, DateTimeFilter
from ..models import OfferApplication


class OfferApplicationFilter(FilterSet):
    """Filters for searching and filtering offer applications in GraphQL queries"""
    
    # Text filters
    proposal = CharFilter(field_name='proposal', lookup_expr='icontains')
    cover_letter = CharFilter(field_name='cover_letter', lookup_expr='icontains')
    
    # Status filter
    status = CharFilter(field_name='status', lookup_expr='iexact')
    
    # Number filters
    min_asking_price = NumberFilter(field_name='asking_price', lookup_expr='gte')
    max_asking_price = NumberFilter(field_name='asking_price', lookup_expr='lte')
    min_reach = NumberFilter(field_name='estimated_reach', lookup_expr='gte')
    max_reach = NumberFilter(field_name='estimated_reach', lookup_expr='lte')
    min_delivery_days = NumberFilter(field_name='delivery_days', lookup_expr='gte')
    max_delivery_days = NumberFilter(field_name='delivery_days', lookup_expr='lte')
    
    # Relation filters
    offer_id = CharFilter(field_name='offer__id', lookup_expr='exact')
    user_id = CharFilter(field_name='user__id', lookup_expr='exact')
    user_name = CharFilter(field_name='user__name', lookup_expr='icontains')
    
    class Meta:
        model = OfferApplication
        fields = {
            'submitted_at': ['exact', 'gte', 'lte'],
            'updated_at': ['exact', 'gte', 'lte'],
            'reviewed_at': ['exact', 'gte', 'lte'],
        }
    
    ordering = OrderingFilter(
        fields=(
            ('submitted_at', 'submitted_at'),
            ('updated_at', 'updated_at'),
            ('asking_price', 'asking_price'),
            ('estimated_reach', 'estimated_reach'),
            ('delivery_days', 'delivery_days'),
            ('status', 'status'),
            ('user__name', 'user_name'),
        )
    )
