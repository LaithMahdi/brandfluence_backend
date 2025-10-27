import graphene
from graphene_django.filter import DjangoFilterConnectionField
from ..user_node import UserNode
from ..models import User


class UserQueries(graphene.ObjectType):
    """GraphQL queries for User"""
    user = graphene.relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    me = graphene.Field(UserNode)
    
    def resolve_all_users(self, info, **kwargs):
        """Get all users (admin only)"""
        user = info.context.user
        if user.is_authenticated and user.is_staff:
            return User.objects.all()
        return User.objects.none()
    
    def resolve_me(self, info):
        """Get current authenticated user"""
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
