"""
GraphQL Node definition for Category model.

This module defines the GraphQL node representation of the Category model
with optimizations and custom field resolvers.
"""
import graphene
from graphene_django_optimizer import OptimizedDjangoObjectType
from django.utils import timezone
from .models import Category


class CategoryNode(OptimizedDjangoObjectType):
    """
    GraphQL Node for Category model.
    
    Provides an optimized GraphQL representation with relay-style
    node interfaces and custom field resolvers.
    """
    
    # Custom fields
    age_in_days = graphene.Int(
        description="Number of days since the category was created"
    )
    
    is_recently_created = graphene.Boolean(
        description="Whether the category was created in the last 7 days"
    )
    
    is_recently_modified = graphene.Boolean(
        description="Whether the category was modified in the last 7 days"
    )
    
    formatted_created = graphene.String(
        description="Formatted creation date"
    )
    
    formatted_modified = graphene.String(
        description="Formatted modification date"
    )
    
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'is_active': ['exact'],
            'created': ['exact', 'gte', 'lte'],
            'modified': ['exact', 'gte', 'lte'],
        }
        description = "Category node with relay-style interface"
    
    def resolve_age_in_days(self, info):
        """
        Resolve the age of the category in days.
        
        Returns:
            Number of days since creation
        """
        return (timezone.now() - self.created).days
    
    def resolve_is_recently_created(self, info):
        """
        Resolve whether the category was recently created.
        
        Returns:
            True if created within the last 7 days
        """
        return (timezone.now() - self.created).days <= 7
    
    def resolve_is_recently_modified(self, info):
        """
        Resolve whether the category was recently modified.
        
        Returns:
            True if modified within the last 7 days
        """
        return (timezone.now() - self.modified).days <= 7
    
    def resolve_formatted_created(self, info):
        """
        Resolve formatted creation date.
        
        Returns:
            Formatted creation date string
        """
        return self.created.strftime('%Y-%m-%d %H:%M:%S')
    
    def resolve_formatted_modified(self, info):
        """
        Resolve formatted modification date.
        
        Returns:
            Formatted modification date string
        """
        return self.modified.strftime('%Y-%m-%d %H:%M:%S')
    
    @classmethod
    def get_queryset(cls, queryset, info):
        """
        Optimize the queryset for this node.
        
        Args:
            queryset: Base queryset
            info: GraphQL resolve info
            
        Returns:
            Optimized queryset
        """
        # Apply any custom queryset optimizations here
        return queryset.select_related().prefetch_related()


# Custom Connection with totalCount
class CategoryConnection(graphene.relay.Connection):
    """
    Custom connection that adds totalCount field.
    """
    total_count = graphene.Int(description="Total count of all categories")
    
    class Meta:
        node = CategoryNode
    
    def resolve_total_count(self, info, **kwargs):
        """
        Resolve the total count of categories.
        """
        return Category.objects.count()