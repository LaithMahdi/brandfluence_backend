import graphene
from ..user_node import UserNode
from graphene_django.filter import DjangoFilterConnectionField
from ..filters import UserFilter
from ..models import User


class UserListQuery(graphene.ObjectType):
    """Query to get all users with pagination and totalCount"""

    all_users = DjangoFilterConnectionField(
        UserNode,
        filterset_class=UserFilter
    )
    
    def resolve_all_users(self, info, **kwargs):
        """Get all users with pagination (admin only)"""
        user = info.context.user
        if not user.is_authenticated or not user.is_staff:
            return User.objects.none()
        
        # Exclude staff users by default
        return User.objects.filter(is_staff=False)
