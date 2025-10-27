from graphene_django_cud.mutations import DjangoDeleteMutation, DjangoBatchDeleteMutation
from ..models import Category


class CategoryDeleteMutation(DjangoDeleteMutation):
    """Delete a single category"""
    
    class Meta:
        model = Category


class CategoryBatchDeleteMutation(DjangoBatchDeleteMutation):
    """Delete multiple categories at once"""
    
    class Meta:
        model = Category