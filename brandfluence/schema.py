import graphene

from category import schema as category_schema
from users import schema as users_schema
from offer import schema as offer_schema

class Query(
    users_schema.Query,
    category_schema.Query,
    offer_schema.Query,    
    graphene.ObjectType
):
    pass

class Mutation(
    users_schema.Mutation,
    category_schema.Mutation,
    offer_schema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)