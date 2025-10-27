import graphene
from .category_queries import CategoryQueries
from .category_mutations import CategoryMutations

class Query (CategoryQueries, graphene.ObjectType):
    pass

class Mutation (CategoryMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)