"""
Reusable pagination utilities for offset-based GraphQL pagination with totalCount.
Can be used across different models (Category, User, etc.)
"""

import graphene
from graphene import relay


class PaginatedConnection(relay.Connection):
    """
    Base Connection class that adds totalCount field.
    Inherit from this for any model that needs pagination with total count.
    
    Example:
        class UserConnection(PaginatedConnection):
            class Meta:
                node = UserNode
    """
    
    total_count = graphene.Int()
    
    class Meta:
        abstract = True
    
    def resolve_total_count(root, info, **kwargs):
        """Resolve total count from stored length or iterable"""
        return root.length if hasattr(root, 'length') else (
            root.iterable.count() if hasattr(root, 'iterable') and hasattr(root.iterable, 'count') else len(root.edges)
        )


class OffsetConnectionField(relay.ConnectionField):
    """
    Custom ConnectionField that handles offset-based pagination properly.
    Automatically adds offset parameter and calculates correct pageInfo.
    
    Features:
    - Adds 'offset' argument automatically
    - Calculates totalCount independently of pagination
    - Correctly determines hasNextPage and hasPreviousPage
    
    Example:
        class Query(graphene.ObjectType):
            all_users = OffsetConnectionField(
                UserConnection,
                name_icontains=graphene.String(),
                email_icontains=graphene.String(),
            )
            
            def resolve_all_users(self, info, **kwargs):
                qs = User.objects.all()
                # Apply filters
                if 'name_icontains' in kwargs:
                    qs = qs.filter(name__icontains=kwargs['name_icontains'])
                return qs
    """
    
    def __init__(self, *args, **kwargs):
        # Automatically add offset parameter
        kwargs.setdefault('offset', graphene.Int())
        super().__init__(*args, **kwargs)
    
    @classmethod
    def resolve_connection(cls, connection_type, args, resolved):
        """
        Override to properly handle offset-based pagination with correct pageInfo.
        
        Args:
            connection_type: The connection class
            args: GraphQL arguments (first, offset, etc.)
            resolved: The queryset or iterable to paginate
            
        Returns:
            Connection instance with proper pagination info
        """
        
        # Get the total count from the queryset before slicing
        if hasattr(resolved, 'count'):
            total_count = resolved.count()
        elif hasattr(resolved, '__len__'):
            total_count = len(resolved)
        else:
            total_count = 0
        
        # Get pagination parameters from args
        offset = args.get('offset', 0)
        first = args.get('first')
        
        # Calculate pagination info
        if first is not None:
            # Check if there are more items after this page
            has_next_page = (offset + first) < total_count
            # Check if we're not at the beginning
            has_previous_page = offset > 0
            
            # Slice the queryset for this page
            sliced_iterable = resolved[offset:offset + first]
        else:
            # No limit specified, return all from offset
            has_next_page = False
            has_previous_page = offset > 0
            sliced_iterable = resolved[offset:]
        
        # Call parent's resolve_connection with sliced iterable
        connection = super(OffsetConnectionField, cls).resolve_connection(
            connection_type, args, sliced_iterable
        )
        
        # Store total count on the connection for resolve_total_count
        connection.length = total_count
        connection.iterable = resolved
        
        # Override pageInfo with our calculated values
        connection.page_info.has_next_page = has_next_page
        connection.page_info.has_previous_page = has_previous_page
        
        return connection


def create_offset_connection_field(connection_class, **extra_args):
    """
    Helper function to create an OffsetConnectionField with custom arguments.
    
    Args:
        connection_class: The connection class (e.g., UserConnection)
        **extra_args: Additional GraphQL arguments (filters, sorting, etc.)
        
    Returns:
        OffsetConnectionField instance
        
    Example:
        all_users = create_offset_connection_field(
            UserConnection,
            name_icontains=graphene.String(),
            email_icontains=graphene.String(),
            is_active=graphene.Boolean(),
            order_by=graphene.String(),
        )
    """
    return OffsetConnectionField(connection_class, **extra_args)
