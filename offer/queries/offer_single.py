import graphene
from graphene_django.filter import DjangoFilterConnectionField

from offer.types.Offer_Node import OfferNode
from offer.models import Offer


class OfferSingleQuery(graphene.ObjectType):
    """Query to get a single offer by ID"""
    
    offer = graphene.relay.Node.Field(OfferNode)
    
    my_offers = graphene.List(OfferNode)
    
    def resolve_my_offers(self, info):
        """Get all offers created by the authenticated user"""
        user = info.context.user
        
        if not user.is_authenticated:
            raise Exception("Vous devez être connecté pour voir vos offres")
        
        return Offer.objects.filter(created_by=user).prefetch_related('applications').order_by('-created_at')

