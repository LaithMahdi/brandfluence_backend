"""
Consolidated Offer Mutations
All CRUD operations for Offer model with admin permission requirements
"""

from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoUpdateMutation,
    DjangoPatchMutation,
    DjangoDeleteMutation,
    DjangoBatchCreateMutation,
    DjangoBatchDeleteMutation
)
from ..models import Offer
from ..types.Offer_Node import OfferNode
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class OfferCreateMutation(DjangoCreateMutation):
    """Create a new offer"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
        exclude = ['created_at']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to create offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class OfferUpdateMutation(DjangoUpdateMutation):
    """Update an existing offer"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
        exclude = ['created_at']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input, id, obj):
        """Only allow admin users to update offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class OfferPatchMutation(DjangoPatchMutation):
    """Partially update an offer (only specific fields)"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
        exclude = ['created_at']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input, id, obj):
        """Only allow admin users to patch offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class OfferDeleteMutation(DjangoDeleteMutation):
    """Delete a single offer"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input, id):
        """Only allow admin users to delete offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class OfferBatchCreateMutation(DjangoBatchCreateMutation):
    """Create multiple offers at once"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
        exclude = ['created_at']
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to batch create offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True


class OfferBatchDeleteMutation(DjangoBatchDeleteMutation):
    """Delete multiple offers at once"""
    
    class Meta:
        model = Offer
        model_type = OfferNode
    
    @classmethod
    @login_required
    def check_permissions(cls, root, info, input):
        """Only allow admin users to batch delete offers"""
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("Admin privileges required")
        return True
