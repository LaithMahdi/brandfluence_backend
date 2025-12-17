import graphene
from graphene_django import DjangoObjectType
from .models import User, UserRole
from common.pagination_utils import PaginatedConnection


class UserRoleEnum(graphene.Enum):
    """GraphQL Enum for User Roles"""
    ADMIN = UserRole.ADMIN.value
    COMPANY = UserRole.COMPANY.value
    INFLUENCER = UserRole.INFLUENCER.value


class UserConnection(PaginatedConnection):
    """Connection for User with totalCount and offset pagination support"""
    
    class Meta:
        abstract = True


class UserNode(DjangoObjectType):
    """GraphQL Node for User model"""
    role = graphene.Field(UserRoleEnum)
    influencer_profile = graphene.Field('users.influencer_node.InfluencerNode')
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'phone_number', 'phone_number_verified',
            'email_verified', 'verified_at', 'is_verify_by_admin', 'role',
            'is_banned', 'is_active', 'is_staff', 'is_superuser',
            'is_completed_profile', 'created_at', 'updated_at', 'last_login'
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
        connection_class = UserConnection
    
    def resolve_role(self, info):
        """Convert Django role to GraphQL enum"""
        if self.role:
            # Handle incorrectly stored roles like 'EnumMeta.COMPANY'
            if 'EnumMeta.' in str(self.role):
                role_value = str(self.role).split('.')[-1]  # Extract 'COMPANY' from 'EnumMeta.COMPANY'
                return role_value
            return self.role
        return None
    
    def resolve_influencer_profile(self, info):
        """Get influencer profile if user is an influencer"""
        from .utils import check_user_role
        if check_user_role(self, 'INFLUENCER'):
            try:
                return self.influencer_profile
            except:
                return None
        return None
