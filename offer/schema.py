import graphene

from .queries.offer_queries import OfferQueries
from .mutations.offer_mutations import OfferMutations


class Query(OfferQueries, graphene.ObjectType):  
    pass


class Mutation(OfferMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
