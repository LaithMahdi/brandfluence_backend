from graphene_django_cud.mutations import DjangoCreateMutation
from ..models import Category
from graphql import GraphQLError


class CategoryCreateMutation(DjangoCreateMutation):
    """Create a new category"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
    
    @classmethod
    def check_permissions(cls, root, info, input):
        """Only allow admin users to create categories"""
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required")
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True