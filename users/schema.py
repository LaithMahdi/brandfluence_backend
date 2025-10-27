import graphene
from .queries import UserQueries
from .mutations import UserMutations, AuthMutations


class Query(UserQueries, graphene.ObjectType):
    """Users app queries"""
    pass


class Mutation(UserMutations, AuthMutations, graphene.ObjectType):
    """Users app mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
