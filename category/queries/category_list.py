import graphene
from ..models import Category
from ..category_node import CategoryConnection


class CategoryListQuery(graphene.ObjectType):
    """Query to get all categories with pagination and totalCount"""
    
    all_categories = graphene.ConnectionField(CategoryConnection)
    
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all().order_by('-created')