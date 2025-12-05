import graphene

from .queries.offer_queries import OfferQueries
from .mutations.offer_mutations import OfferMutations


from offer.mutations.offer_application_mutations import (
    CreateOfferApplication,
    UpdateOfferApplicationStatus,
)



class Query(OfferQueries, graphene.ObjectType):
    """All GraphQL queries"""
    pass



class Mutation(OfferMutations, graphene.ObjectType):
    """All GraphQL mutations"""

   
    create_offer_application = CreateOfferApplication.Field()
    update_offer_application_status = UpdateOfferApplicationStatus.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
