import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from offer.filters.Offer_Filter import OfferFilter
from offer.types.Offer_Node import OfferNode
from offer.models import Offer


class OfferListQuery(graphene.ObjectType):
    """Query to get all offers with pagination and totalCount"""

    all_offers = DjangoFilterConnectionField(
        OfferNode,
        filterset_class=OfferFilter,
        description="Get all offers with pagination and filtering"
    )
    
    # Get offers created by current user
    my_offers = DjangoFilterConnectionField(
        OfferNode,
        filterset_class=OfferFilter,
        description="Get offers created by the authenticated user"
    )

    offer = graphene.relay.Node.Field(OfferNode)
    
    @login_required
    def resolve_my_offers(self, info, **kwargs):
        """Get offers created by the current authenticated user"""
        user = info.context.user
        return Offer.objects.filter(created_by=user).prefetch_related('applications', 'applications__user')
