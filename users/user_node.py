import graphene
from graphene_django import DjangoObjectType
from .models import User, UserRole


class UserRoleEnum(graphene.Enum):
    """GraphQL Enum for User Roles"""
    ADMIN = 'ADMIN'
    COMPANY = 'COMPANY'
    INFLUENCER = 'INFLUENCER'


class UserNode(DjangoObjectType):
    """GraphQL Node for User model"""
    role = graphene.Field(UserRoleEnum)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'phone_number', 'phone_number_verified',
            'email_verified', 'verified_at', 'is_verify_by_admin', 'role',
            'is_banned', 'is_active', 'is_staff', 'is_superuser',
            'created_at', 'updated_at', 'last_login'
        )
        filter_fields = {
            'email': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'role': ['exact'],
            'email_verified': ['exact'],
            'phone_number_verified': ['exact'],
            'is_verify_by_admin': ['exact'],
            'is_banned': ['exact'],
            'is_active': ['exact'],
            'is_staff': ['exact'],
        }
        interfaces = (graphene.relay.Node,)
    
    def resolve_role(self, info):
        """Convert Django TextChoices role to GraphQL enum"""
        if self.role:
            return self.role
        return None
