import graphene
from .offer_mutations_all import (
    OfferCreateMutation,
    OfferUpdateMutation,
    OfferPatchMutation,
    OfferDeleteMutation,
    OfferBatchCreateMutation,
    OfferBatchDeleteMutation
)

class OfferMutations(graphene.ObjectType):
    """All offer mutations in one place"""
    create_offer = OfferCreateMutation.Field()
    update_offer = OfferUpdateMutation.Field()
    patch_offer = OfferPatchMutation.Field()
    delete_offer = OfferDeleteMutation.Field()
    batch_create_offers = OfferBatchCreateMutation.Field()
    batch_delete_offers = OfferBatchDeleteMutation.Field()
    
