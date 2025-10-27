"""
Category update mutation.
"""
import graphene
from graphene_django_cud.mutations import DjangoUpdateMutation
from ..models import Category


class CategoryUpdateMutation(DjangoUpdateMutation):
    """
    Mutation to update an existing Category instance.
    
    This mutation allows updating an existing category with the provided data.
    The 'modified' field is automatically updated by the TimeStampedModel.
    """
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Update an existing Category"
        
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