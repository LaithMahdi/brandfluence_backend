import graphene
from ..types import CategoryNode
from graphene_django.filter import DjangoFilterConnectionField
from category.filters.category_filter import CategoryFilter



class CategoryListQuery(graphene.ObjectType):
    """Query to get all categories with pagination and totalCount"""

    all_categories = DjangoFilterConnectionField(CategoryNode,filterset_class=CategoryFilter)
    category = graphene.relay.Node.Field(CategoryNode)