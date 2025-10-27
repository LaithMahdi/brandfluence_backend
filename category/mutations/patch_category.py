from graphene_django_cud.mutations import DjangoPatchMutation
from ..models import Category


class CategoryPatchMutation(DjangoPatchMutation):
    """Partially update a category (only specific fields)"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']