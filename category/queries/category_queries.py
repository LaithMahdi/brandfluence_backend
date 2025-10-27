import graphene
from .category_single import CategorySingleQuery
from .category_list import CategoryListQuery


class CategoryQueries(CategorySingleQuery, CategoryListQuery):
    """All category queries in one place"""
    pass