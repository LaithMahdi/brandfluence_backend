import graphene
from graphene_django.filter import DjangoFilterConnectionField
from ..user_node import UserNode, UserConnection
from ..models import User
from common.pagination_utils import OffsetConnectionField


class UserQueries(graphene.ObjectType):
    """GraphQL queries for User"""
    user = graphene.relay.Node.Field(UserNode)
    
    # Updated to use OffsetConnectionField with totalCount support
    all_users = OffsetConnectionField(
        UserConnection,
        # Add filter arguments
        email_Icontains=graphene.String(),
        name_Icontains=graphene.String(),
        role=graphene.String(),
        email_verified=graphene.Boolean(),
        is_active=graphene.Boolean(),
        is_staff=graphene.Boolean(),
        is_banned=graphene.Boolean(),
        order_by=graphene.String(),
    )
    
    me = graphene.Field(UserNode)
    
    def resolve_all_users(self, info, **kwargs):
        """Get all users with pagination (admin only)"""
        user = info.context.user
        if not user.is_authenticated or not user.is_staff:
            return User.objects.none()
        
        qs = User.objects.all()
        
        # Apply filters
        if 'email_Icontains' in kwargs:
            qs = qs.filter(email__icontains=kwargs['email_Icontains'])
        if 'name_Icontains' in kwargs:
            qs = qs.filter(name__icontains=kwargs['name_Icontains'])
        if 'role' in kwargs:
            qs = qs.filter(role=kwargs['role'])
        if 'email_verified' in kwargs:
            qs = qs.filter(email_verified=kwargs['email_verified'])
        if 'is_active' in kwargs:
            qs = qs.filter(is_active=kwargs['is_active'])
        if 'is_staff' in kwargs:
            qs = qs.filter(is_staff=kwargs['is_staff'])
        if 'is_banned' in kwargs:
            qs = qs.filter(is_banned=kwargs['is_banned'])
        
        # Apply ordering
        order_by = kwargs.get('order_by', '-created_at')
        qs = qs.order_by(order_by)
        
        return qs
    
    def resolve_me(self, info):
        """Get current authenticated user"""
        user = info.context.user
        if user.is_authenticated:
            return user
        return None