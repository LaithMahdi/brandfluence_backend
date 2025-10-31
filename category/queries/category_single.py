import graphene
from ..types import CategoryNode


class CategorySingleQuery(graphene.ObjectType):
    """Query to get a single category by ID"""
    
    category = graphene.relay.Node.Field(CategoryNode)