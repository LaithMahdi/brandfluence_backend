import graphene
from ..category_node import CategoryNode


class CategorySingleQuery(graphene.ObjectType):
    """Query to get a single category by ID"""
    
    category = graphene.relay.Node.Field(CategoryNode)