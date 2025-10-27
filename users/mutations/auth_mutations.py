import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from ..user_node import UserNode

User = get_user_model()


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    """Custom JWT token obtain mutation with user details"""
    user = graphene.Field(UserNode)
    
    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class VerifyToken(graphql_jwt.Verify):
    """Verify JWT token"""
    pass


class RefreshToken(graphql_jwt.Refresh):
    """Refresh JWT token"""
    pass


class RevokeToken(graphql_jwt.Revoke):
    """Revoke JWT token"""
    pass


class ChangePassword(graphene.Mutation):
    """Change user password"""
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
    
    @login_required
    def mutate(self, info, old_password, new_password):
        user = info.context.user
        
        # Check if old password is correct
        if not user.check_password(old_password):
            raise GraphQLError('Old password is incorrect')
        
        # Validate new password
        if len(new_password) < 8:
            raise GraphQLError('New password must be at least 8 characters long')
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return ChangePassword(
            success=True,
            message='Password changed successfully'
        )


class ResetPasswordRequest(graphene.Mutation):
    """Request password reset (placeholder for email sending)"""
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        email = graphene.String(required=True)
    
    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
            # TODO: Implement email sending logic with reset token
            # For now, just return success
            return ResetPasswordRequest(
                success=True,
                message='Password reset instructions sent to your email'
            )
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return ResetPasswordRequest(
                success=True,
                message='If the email exists, password reset instructions have been sent'
            )


class AuthMutations(graphene.ObjectType):
    """Authentication mutations"""
    # JWT token operations
    token_auth = ObtainJSONWebToken.Field()
    verify_token = VerifyToken.Field()
    refresh_token = RefreshToken.Field()
    revoke_token = RevokeToken.Field()
    
    # Password management
    change_password = ChangePassword.Field()
    reset_password_request = ResetPasswordRequest.Field()
