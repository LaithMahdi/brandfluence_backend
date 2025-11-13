import graphene
from graphene_django.filter import DjangoFilterConnectionField

from offer.filters.Offer_Filter import OfferFilter
from offer.types.Offer_Node import OfferNode


class OfferListQuery(graphene.ObjectType):
    """Query to get all offers with pagination and totalCount"""

    all_offers = DjangoFilterConnectionField(
        OfferNode,
        filterset_class=OfferFilter
    )

    offer = graphene.relay.Node.Field(OfferNode)
