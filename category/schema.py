"""
GraphQL schema for Category app.

This module defines the GraphQL schema by combining queries and mutations
from the organized folder structure.
"""
import graphene
from .queries import CategoryQueries
from .mutations import CategoryMutations


class Query(CategoryQueries, graphene.ObjectType):
    """
    Root Query class for Category app.
    
    Inherits all category-related queries from the organized queries module.
    """
    pass


class Mutation(CategoryMutations, graphene.ObjectType):
    """
    Root Mutation class for Category app.
    
    Inherits all category-related mutations from the organized mutations module.
    """
    pass


# Schema definition
schema = graphene.Schema(
    query=Query, 
    mutation=Mutation
)