"""
Category delete mutations.
"""
import graphene
from graphene_django_cud.mutations import DjangoDeleteMutation, DjangoBatchDeleteMutation
from ..models import Category


class CategoryDeleteMutation(DjangoDeleteMutation):
    """
    Mutation to delete an existing Category instance.
    
    This mutation allows deleting a single category by ID.
    """
    
    class Meta:
        model = Category
        description = "Delete an existing Category"
        
    @classmethod
    def get_permissions(cls, root, info, input):
        """
        Define permissions for this mutation.
        Override this method to implement custom permission logic.
        """
        return []


class CategoryBatchDeleteMutation(DjangoBatchDeleteMutation):
    """
    Mutation to delete multiple Category instances.
    
    This mutation allows deleting multiple categories in a single operation.
    """
    
    class Meta:
        model = Category
        description = "Batch delete Categories"
        
    @classmethod
    def get_permissions(cls, root, info, input):
        """
        Define permissions for this mutation.
        Override this method to implement custom permission logic.
        """
        return []