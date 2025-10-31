from graphene_django_cud.mutations import DjangoBatchCreateMutation
from ..models import Category
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class CategoryBatchCreateMutation(DjangoBatchCreateMutation):
    """Create multiple categories at once"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to batch create categories"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True