import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from graphene_django.filter import DjangoFilterConnectionField

from ..influencer_models import Influencer
from ..influencer_node import InfluencerNode
from ..utils import check_user_role, normalize_role

User = get_user_model()


class InfluencerQueries(graphene.ObjectType):
    """Queries for influencer profiles"""
    
    # Get current user's influencer profile
    my_influencer_profile = graphene.Field(InfluencerNode)
    
    # Get influencer by user ID
    influencer_by_user = graphene.Field(
        InfluencerNode,
        user_id=graphene.ID(required=True)
    )
    
    # Get influencer by ID
    influencer = graphene.Field(
        InfluencerNode,
        id=graphene.ID(required=True)
    )
    
    # List all influencers (with filtering)
    all_influencers = graphene.List(
        InfluencerNode,
        localisation=graphene.String(),
        disponibilite=graphene.String(),
        min_followers=graphene.Int(),
        category_ids=graphene.List(graphene.ID)
    )
    
    # Search influencers
    search_influencers = graphene.List(
        InfluencerNode,
        query=graphene.String(required=True),
        localisation=graphene.String(),
        min_followers=graphene.Int(),
        max_followers=graphene.Int(),
        min_engagement=graphene.Float(),
        category_ids=graphene.List(graphene.ID)
    )
    
    def resolve_my_influencer_profile(self, info):
        """Get current authenticated user's influencer profile"""
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        # Get user from database to ensure we have the latest role
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            # Refresh user from database
            user = User.objects.get(pk=user.pk)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        print(f'User role: {user.role} (type: {type(user.role)})')
        
        
        if not check_user_role(user, 'INFLUENCER'):
            raise GraphQLError(f'This query is only available for influencer accounts (current role: {user.role}, type: {type(user.role)})')
        
        try:
            return Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            return None
    
    def resolve_influencer_by_user(self, info, user_id):
        """Get influencer profile by user ID"""
        try:
            user = User.objects.get(pk=user_id)
            if not check_user_role(user, 'INFLUENCER'):
                raise GraphQLError('User is not an influencer')
            
            return Influencer.objects.get(user=user)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found')
    
    def resolve_influencer(self, info, id):
        """Get influencer profile by influencer ID"""
        try:
            return Influencer.objects.get(pk=id)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer not found')
    
    def resolve_all_influencers(self, info, localisation=None, disponibilite=None, 
                               min_followers=None, category_ids=None):
        """List all influencers with optional filters"""
        queryset = Influencer.objects.all()
        
        # Filter by localisation
        if localisation:
            queryset = queryset.filter(localisation__icontains=localisation)
        
        # Filter by availability
        if disponibilite:
            queryset = queryset.filter(disponibilite_collaboration=disponibilite)
        
        # Filter by categories
        if category_ids:
            queryset = queryset.filter(selected_categories__id__in=category_ids).distinct()
        
        # Filter by minimum followers (calculated from social networks)
        if min_followers:
            # This requires annotation to calculate total followers
            influencers = []
            for influencer in queryset:
                if influencer.followers_totaux >= min_followers:
                    influencers.append(influencer)
            return influencers
        
        return queryset
    
    def resolve_search_influencers(self, info, query, localisation=None, 
                                  min_followers=None, max_followers=None,
                                  min_engagement=None, category_ids=None):
        """Search influencers with advanced filters"""
        from django.db.models import Q
        
        # Search in multiple fields
        queryset = Influencer.objects.filter(
            Q(pseudo__icontains=query) |
            Q(biography__icontains=query) |
            Q(user__name__icontains=query) |
            Q(centres_interet__icontains=query)
        )
        
        # Apply additional filters
        if localisation:
            queryset = queryset.filter(localisation__icontains=localisation)
        
        if category_ids:
            queryset = queryset.filter(selected_categories__id__in=category_ids).distinct()
        
        # Filter by followers and engagement (requires calculation)
        results = []
        for influencer in queryset:
            followers = influencer.followers_totaux
            engagement = influencer.engagement_moyen_global
            
            if min_followers and followers < min_followers:
                continue
            if max_followers and followers > max_followers:
                continue
            if min_engagement and engagement < min_engagement:
                continue
            
            results.append(influencer)
        
        return results
