import graphene
from .queries import UserQueries, InfluencerQueries
from .mutations import UserMutations, AuthMutations, InfluencerMutations


class Query(UserQueries, InfluencerQueries, graphene.ObjectType):
    """Users app queries"""
    pass


class Mutation(UserMutations, AuthMutations, InfluencerMutations, graphene.ObjectType):
    """Users app mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
