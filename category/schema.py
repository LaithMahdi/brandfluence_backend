import graphene

from .queries import CategoryQueries
from .mutations import CategoryMutations


class Query(CategoryQueries, graphene.ObjectType):  
    pass


class Mutation(CategoryMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)