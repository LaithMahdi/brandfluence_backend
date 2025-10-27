"""
Category list query.
"""
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from ..models import Category
from ..category_node import CategoryNode, CategoryConnection
from ..category_filter import CategoryFilter


class CategoryListQuery(graphene.ObjectType):
    """
    Query for retrieving multiple Category instances.
    
    This query provides filtered and paginated access to categories.
    """
    
    all_categories = graphene.ConnectionField(
        CategoryConnection,
        description="Get all categories with optional filtering and pagination"
    )
    
    def resolve_all_categories(self, info, **kwargs):
        """
        Resolver for all categories query.
        
        Args:
            info: GraphQL resolve info
            **kwargs: Filter and pagination arguments
            
        Returns:
            QuerySet of all Category instances
        """
        return Category.objects.all().order_by('-created')