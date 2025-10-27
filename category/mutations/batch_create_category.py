"""
Category batch create mutation.
"""
import graphene
from graphene_django_cud.mutations import DjangoBatchCreateMutation
from ..models import Category


class CategoryBatchCreateMutation(DjangoBatchCreateMutation):
    """
    Mutation to create multiple Category instances.
    
    This mutation allows creating multiple categories in a single operation.
    """
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Batch create Categories"
        
    @classmethod
    def get_permissions(cls, root, info, input):
        """
        Define permissions for this mutation.
        Override this method to implement custom permission logic.
        """
        return []
        
    @classmethod
    def before_save(cls, root, info, input, obj):
        """
        Hook called before saving the object.
        Override this method to implement custom validation or data processing.
        """
        # Add any custom validation or data processing here
        pass