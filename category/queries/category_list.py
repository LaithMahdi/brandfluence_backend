import graphene
from graphene_django.filter import DjangoFilterConnectionField
from ..models import Category
from ..category_node import CategoryConnection, CategoryNode
from ..category_filter import CategoryFilter


class CategoryListQuery(graphene.ObjectType):
    """Query to get all categories with pagination and totalCount"""
    
    all_categories = DjangoFilterConnectionField(
        CategoryNode,
        filterset_class=CategoryFilter
    )
    
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all().order_by('-created')