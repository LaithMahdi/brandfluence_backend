from graphene_django_cud.mutations import DjangoBatchCreateMutation
from ..models import Category


class CategoryBatchCreateMutation(DjangoBatchCreateMutation):
    """Create multiple categories at once"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']