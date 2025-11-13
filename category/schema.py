import graphene

from offer.mutations.offer_mutations import OfferMutations
from offer.queries.offer_queries import OfferQueries
from .queries import CategoryQueries
from .mutations import CategoryMutations


class Query(CategoryQueries, graphene.ObjectType,OfferQueries):  
    pass


class Mutation(CategoryMutations, graphene.ObjectType,OfferMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)