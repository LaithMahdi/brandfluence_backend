from graphene_django_cud.mutations import DjangoCreateMutation
from ..models import Category
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class CategoryCreateMutation(DjangoCreateMutation):
    """Create a new category"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to create categories"""
        user = info.context.user
        
        # Print token for debugging
        auth_header = info.context.META.get('HTTP_AUTHORIZATION', '')
        print(f"[CREATE CATEGORY] Authorization Header: {auth_header}")
        print(f"[CREATE CATEGORY] User: {user}")
        print(f"[CREATE CATEGORY] User authenticated: {user.is_authenticated}")
        print(f"[CREATE CATEGORY] User is_staff: {user.is_staff}")
        
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True