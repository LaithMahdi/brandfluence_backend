import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from ..user_node import UserNode, UserRoleEnum

User = get_user_model()


class RegisterUser(graphene.Mutation):
    """Register a new user"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)
        phone_number = graphene.String()
        role = graphene.Argument(UserRoleEnum, required=True)
    
    def mutate(self, info, email, password, name, role, phone_number=None):
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise GraphQLError('User with this email already exists')
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role,
            phone_number=phone_number
        )
        
        return RegisterUser(
            user=user,
            success=True,
            message='User registered successfully'
        )


class UpdateUser(graphene.Mutation):
    """Update user information"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
        name = graphene.String()
        phone_number = graphene.String()
        email_verified = graphene.Boolean()
        phone_number_verified = graphene.Boolean()
        is_verify_by_admin = graphene.Boolean()
        is_banned = graphene.Boolean()
        role = graphene.Argument(UserRoleEnum)
    
    def mutate(self, info, user_id, **kwargs):
        current_user = info.context.user
        
        if not current_user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        # Only allow users to update their own profile or admins to update any
        if user.id != current_user.id and not current_user.is_staff:
            raise GraphQLError('Permission denied')
        
        # Update fields
        if 'name' in kwargs:
            user.name = kwargs['name']
        if 'phone_number' in kwargs:
            user.phone_number = kwargs['phone_number']
        
        # Admin-only fields
        if current_user.is_staff:
            if 'email_verified' in kwargs:
                user.email_verified = kwargs['email_verified']
            if 'phone_number_verified' in kwargs:
                user.phone_number_verified = kwargs['phone_number_verified']
            if 'is_verify_by_admin' in kwargs:
                user.is_verify_by_admin = kwargs['is_verify_by_admin']
            if 'is_banned' in kwargs:
                if kwargs['is_banned']:
                    user.ban_user()
                else:
                    user.unban_user()
            if 'role' in kwargs:
                user.role = kwargs['role']
        
        user.save()
        
        return UpdateUser(
            user=user,
            success=True,
            message='User updated successfully'
        )


class VerifyEmail(graphene.Mutation):
    """Verify user email"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        # Only allow users to verify their own email or admins
        if user.id != current_user.id and not current_user.is_staff:
            raise GraphQLError('Permission denied')
        
        user.verify_email()
        
        return VerifyEmail(
            user=user,
            success=True,
            message='Email verified successfully'
        )


class VerifyPhone(graphene.Mutation):
    """Verify user phone number"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        # Only allow users to verify their own phone or admins
        if user.id != current_user.id and not current_user.is_staff:
            raise GraphQLError('Permission denied')
        
        user.verify_phone()
        
        return VerifyPhone(
            user=user,
            success=True,
            message='Phone number verified successfully'
        )


class AdminVerifyUser(graphene.Mutation):
    """Admin verify a user"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated or not current_user.is_staff:
            raise GraphQLError('Admin permission required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        user.admin_verify()
        
        return AdminVerifyUser(
            user=user,
            success=True,
            message='User verified by admin successfully'
        )


class BanUser(graphene.Mutation):
    """Ban a user"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated or not current_user.is_staff:
            raise GraphQLError('Admin permission required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        user.ban_user()
        
        return BanUser(
            user=user,
            success=True,
            message='User banned successfully'
        )


class UnbanUser(graphene.Mutation):
    """Unban a user"""
    user = graphene.Field(UserNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated or not current_user.is_staff:
            raise GraphQLError('Admin permission required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        user.unban_user()
        
        return UnbanUser(
            user=user,
            success=True,
            message='User unbanned successfully'
        )


class DeleteUser(graphene.Mutation):
    """Delete a user"""
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.ID(required=True)
    
    def mutate(self, info, user_id):
        current_user = info.context.user
        
        if not current_user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        # Only allow users to delete their own account or admins to delete any
        if user.id != current_user.id and not current_user.is_staff:
            raise GraphQLError('Permission denied')
        
        user.delete()
        
        return DeleteUser(
            success=True,
            message='User deleted successfully'
        )


class UserMutations(graphene.ObjectType):
    """All user mutations"""
    register_user = RegisterUser.Field()
    update_user = UpdateUser.Field()
    verify_email = VerifyEmail.Field()
    verify_phone = VerifyPhone.Field()
    admin_verify_user = AdminVerifyUser.Field()
    ban_user = BanUser.Field()
    unban_user = UnbanUser.Field()
    delete_user = DeleteUser.Field()
