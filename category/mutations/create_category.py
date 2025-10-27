"""
Category create mutation.
"""
import graphene
from graphene_django_cud.mutations import DjangoCreateMutation
from ..models import Category


class CategoryCreateMutation(DjangoCreateMutation):
    """
    Mutation to create a new Category instance.
    
    This mutation allows creating a new category with the provided data.
    The 'created' and 'modified' fields are automatically handled by the TimeStampedModel.
    """
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Create a new Category"
        
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