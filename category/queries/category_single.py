"""
Category single item query.
"""
import graphene
from ..category_node import CategoryNode


class CategorySingleQuery(graphene.ObjectType):
    """
    Query for retrieving a single Category instance.
    
    This query provides access to a single category by its ID.
    """
    
    category = graphene.relay.Node.Field(CategoryNode, description="Get a single category by ID")
    
    def resolve_category(self, info, **kwargs):
        """
        Resolver for single category query.
        
        Args:
            info: GraphQL resolve info
            **kwargs: Additional arguments
            
        Returns:
            Category instance or None if not found
        """
        # The Node.Field automatically handles the ID resolution
        # Additional custom logic can be added here if needed
        return None  # Node.Field handles the actual resolution