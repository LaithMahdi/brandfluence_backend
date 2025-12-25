import graphene

from .queries.offer_queries import OfferQueries
from .queries.offer_application_queries import OfferApplicationQueries
from .mutations.offer_mutations import OfferMutations
from .mutations.offer_application_mutations_pro import OfferApplicationMutations


class Query(OfferQueries, OfferApplicationQueries, graphene.ObjectType):
    """All GraphQL queries"""
    pass


class Mutation(OfferMutations, OfferApplicationMutations, graphene.ObjectType):
    """All GraphQL mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
