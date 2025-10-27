"""
Category patch mutation.
"""
import graphene
from graphene_django_cud.mutations import DjangoPatchMutation
from ..models import Category


class CategoryPatchMutation(DjangoPatchMutation):
    """
    Mutation to partially update an existing Category instance.
    
    This mutation allows updating specific fields of an existing category
    without requiring all fields to be provided.
    """
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Patch an existing Category"
        
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