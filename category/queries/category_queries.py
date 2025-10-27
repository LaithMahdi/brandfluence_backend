"""
Category queries collection.
"""
import graphene
from .category_single import CategorySingleQuery
from .category_list import CategoryListQuery


class CategoryQueries(CategorySingleQuery, CategoryListQuery):
    """
    Collection of all Category-related queries.
    
    This class inherits from individual query classes to provide
    a unified interface for all category queries.
    """
    pass