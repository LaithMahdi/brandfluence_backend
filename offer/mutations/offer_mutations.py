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
    offerCreate = OfferCreateMutation.Field()
    offerUpdate = OfferUpdateMutation.Field()
    offerPatch = OfferPatchMutation.Field()
    offerDelete = OfferDeleteMutation.Field()
    offerBatchCreate = OfferBatchCreateMutation.Field()
    offerBatchDelete = OfferBatchDeleteMutation.Field()
