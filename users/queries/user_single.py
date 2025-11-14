import graphene
from ..user_node import UserNode


class UserSingleQuery(graphene.ObjectType):
    """Query to get a single user by ID"""
    
    user = graphene.relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)
    
    def resolve_me(self, info):
        """Get current authenticated user"""
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
