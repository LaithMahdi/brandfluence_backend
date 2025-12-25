from django_filters import FilterSet, OrderingFilter, CharFilter, NumberFilter, DateTimeFilter
from django.db.models import Sum, Avg
from ..influencer_models import Influencer


class InfluencerFilter(FilterSet):
    """Filters for searching and filtering influencers in GraphQL queries"""
    
    # Text filters
    pseudo = CharFilter(field_name='pseudo', lookup_expr='icontains')
    localisation = CharFilter(field_name='localisation', lookup_expr='icontains')
    biography = CharFilter(field_name='biography', lookup_expr='icontains')
    centres_interet = CharFilter(field_name='centres_interet', lookup_expr='icontains')
    user_name = CharFilter(field_name='user__name', lookup_expr='icontains')
    
    # Enum filters - use iexact for case-insensitive matching
    disponibilite_collaboration = CharFilter(field_name='disponibilite_collaboration', lookup_expr='iexact')
    
    # Number filters for statistics
    min_followers = NumberFilter(method='filter_min_followers')
    max_followers = NumberFilter(method='filter_max_followers')
    min_engagement = NumberFilter(method='filter_min_engagement')
    max_engagement = NumberFilter(method='filter_max_engagement')
    
    class Meta:
        model = Influencer
        fields = {
            'instagram_username': ['exact', 'icontains'],
            'site_web': ['exact', 'icontains'],
            'created_at': ['exact', 'gte', 'lte'],
            'updated_at': ['exact', 'gte', 'lte'],
        }
        
    ordering = OrderingFilter(
        fields=(
            ('pseudo', 'pseudo'),
            ('localisation', 'localisation'),
            ('user__name', 'user_name'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('total_followers', 'followers_totaux'),
            ('avg_engagement', 'engagement_moyen_global'),
        )
    )
    
    def filter_queryset(self, queryset):
        """Override to add annotations for ordering"""
        queryset = queryset.annotate(
            total_followers=Sum('reseaux_sociaux__nombre_abonnes'),
            avg_engagement=Avg('reseaux_sociaux__taux_engagement')
        )
        return super().filter_queryset(queryset)
    
    def filter_min_followers(self, queryset, name, value):
        """Filter influencers by minimum total followers"""
        filtered_ids = []
        for influencer in queryset:
            if influencer.followers_totaux >= value:
                filtered_ids.append(influencer.id)
        return queryset.filter(id__in=filtered_ids)
    
    def filter_max_followers(self, queryset, name, value):
        """Filter influencers by maximum total followers"""
        filtered_ids = []
        for influencer in queryset:
            if influencer.followers_totaux <= value:
                filtered_ids.append(influencer.id)
        return queryset.filter(id__in=filtered_ids)
    
    def filter_min_engagement(self, queryset, name, value):
        """Filter influencers by minimum engagement rate"""
        filtered_ids = []
        for influencer in queryset:
            if influencer.engagement_moyen_global >= value:
                filtered_ids.append(influencer.id)
        return queryset.filter(id__in=filtered_ids)
    
    def filter_max_engagement(self, queryset, name, value):
        """Filter influencers by maximum engagement rate"""
        filtered_ids = []
        for influencer in queryset:
            if influencer.engagement_moyen_global <= value:
                filtered_ids.append(influencer.id)
        return queryset.filter(id__in=filtered_ids)
