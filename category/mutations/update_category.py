from graphene_django_cud.mutations import DjangoUpdateMutation
from ..models import Category
from graphql import GraphQLError


class CategoryUpdateMutation(DjangoUpdateMutation):
    """Update an existing category"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
    
    @classmethod
    def check_permissions(cls, root, info, input):
        """Only allow admin users to update categories"""
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required")
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True