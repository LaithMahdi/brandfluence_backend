"""
Professional Offer Application Queries
Complete query operations with proper filtering and permissions
"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ..models import OfferApplication, ApplicationStatus
from ..types.OfferApplication_Node import OfferApplicationNode
from ..filters.OfferApplication_Filter import OfferApplicationFilter
from users.utils import check_user_role


class OfferApplicationQueries(graphene.ObjectType):
    """Queries for offer applications"""
    
    # Get single application by ID
    offer_application = graphene.relay.Node.Field(OfferApplicationNode)
    
    # Get all applications with filtering and pagination
    all_offer_applications = DjangoFilterConnectionField(
        OfferApplicationNode,
        filterset_class=OfferApplicationFilter,
        description="Get all offer applications with pagination and filtering"
    )
    
    # Get current user's applications (influencer view)
    my_applications = DjangoFilterConnectionField(
        OfferApplicationNode,
        filterset_class=OfferApplicationFilter,
        description="Get current user's applications"
    )
    
    # Get applications for a specific offer (offer creator view)
    applications_for_offer = DjangoFilterConnectionField(
        OfferApplicationNode,
        filterset_class=OfferApplicationFilter,
        offer_id_custom=graphene.ID(required=True),
        description="Get all applications for a specific offer"
    )
    
    # Get applications by status
    applications_by_status = DjangoFilterConnectionField(
        OfferApplicationNode,
        status_filter=graphene.String(required=True),
        filterset_class=OfferApplicationFilter,
        description="Get applications filtered by status"
    )
    
    # Statistics queries
    my_application_stats = graphene.Field(
        'offer.queries.offer_application_queries.ApplicationStatsType',
        description="Get statistics for current user's applications"
    )
    
    offer_application_stats = graphene.Field(
        'offer.queries.offer_application_queries.ApplicationStatsType',
        offer_id_stats=graphene.ID(required=True),
        description="Get statistics for applications on a specific offer"
    )
    
    @login_required
    def resolve_my_applications(self, info, **kwargs):
        """Get current user's applications"""
        user = info.context.user
        
        if not check_user_role(user, 'INFLUENCER'):
            raise GraphQLError('This query is only available for influencer accounts')
        
        return OfferApplication.objects.filter(user=user)
    
    @login_required
    def resolve_applications_for_offer(self, info, offer_id_custom, **kwargs):
        """Get all applications for a specific offer (offer creator or admin only)"""
        user = info.context.user
        
        from ..models import Offer
        try:
            offer = Offer.objects.get(id=offer_id_custom)
        except Offer.DoesNotExist:
            raise GraphQLError('Offer not found')
        
        # Check permissions
        is_offer_creator = offer.created_by_id == user.id
        is_admin = user.is_staff or user.is_superuser
        
        if not (is_offer_creator or is_admin):
            raise GraphQLError('You do not have permission to view applications for this offer')
        
        return OfferApplication.objects.filter(offer=offer)
    
    @login_required
    def resolve_applications_by_status(self, info, status_filter, **kwargs):
        """Get applications filtered by status"""
        user = info.context.user
        
        # Validate status
        valid_statuses = [choice[0] for choice in ApplicationStatus.choices]
        if status_filter not in valid_statuses:
            raise GraphQLError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        
        # Influencers see their own applications
        if check_user_role(user, 'INFLUENCER'):
            return OfferApplication.objects.filter(user=user, status=status_filter)
        
        # Companies/Admins see applications for their offers
        if user.is_staff or user.is_superuser:
            return OfferApplication.objects.filter(status=status_filter)
        
        # Company users see applications for their offers
        return OfferApplication.objects.filter(
            offer__created_by=user,
            status=status_filter
        )
    
    @login_required
    def resolve_my_application_stats(self, info, **kwargs):
        """Get statistics for current user's applications"""
        user = info.context.user
        
        if not check_user_role(user, 'INFLUENCER'):
            raise GraphQLError('This query is only available for influencer accounts')
        
        applications = OfferApplication.objects.filter(user=user)
        
        return ApplicationStatsType(
            total=applications.count(),
            pending=applications.filter(status=ApplicationStatus.PENDING).count(),
            approved=applications.filter(status=ApplicationStatus.APPROVED).count(),
            rejected=applications.filter(status=ApplicationStatus.REJECTED).count(),
            withdrawn=applications.filter(status=ApplicationStatus.WITHDRAW).count(),
        )
    
    @login_required
    def resolve_offer_application_stats(self, info, offer_id_stats, **kwargs):
        """Get statistics for applications on a specific offer"""
        user = info.context.user
        
        from ..models import Offer
        try:
            offer = Offer.objects.get(id=offer_id_stats)
        except Offer.DoesNotExist:
            raise GraphQLError('Offer not found')
        
        # Check permissions
        is_offer_creator = offer.created_by_id == user.id
        is_admin = user.is_staff or user.is_superuser
        
        if not (is_offer_creator or is_admin):
            raise GraphQLError('You do not have permission to view statistics for this offer')
        
        applications = OfferApplication.objects.filter(offer=offer)
        
        return ApplicationStatsType(
            total=applications.count(),
            pending=applications.filter(status=ApplicationStatus.PENDING).count(),
            approved=applications.filter(status=ApplicationStatus.APPROVED).count(),
            rejected=applications.filter(status=ApplicationStatus.REJECTED).count(),
            withdrawn=applications.filter(status=ApplicationStatus.WITHDRAW).count(),
        )


class ApplicationStatsType(graphene.ObjectType):
    """Statistics for applications"""
    total = graphene.Int()
    pending = graphene.Int()
    approved = graphene.Int()
    rejected = graphene.Int()
    withdrawn = graphene.Int()
