import graphene

from offer.types.Offer_Node import OfferNode


class OfferSingleQuery(graphene.ObjectType):
    """Query to get a single offer by ID"""
    
    offer = graphene.relay.Node.Field(OfferNode)
