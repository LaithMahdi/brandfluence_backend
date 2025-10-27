import graphene

from category import schema as category_schema

class Query(category_schema.Query, graphene.ObjectType):
    pass

class Mutation(category_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)