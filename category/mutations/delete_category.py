from graphene_django_cud.mutations import DjangoDeleteMutation, DjangoBatchDeleteMutation
from ..models import Category
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class CategoryDeleteMutation(DjangoDeleteMutation):
    """Delete a single category"""
    
    class Meta:
        model = Category
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input, id):
        """Only allow admin users to delete categories"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class CategoryBatchDeleteMutation(DjangoBatchDeleteMutation):
    """Delete multiple categories at once"""
    
    class Meta:
        model = Category
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to batch delete categories"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True