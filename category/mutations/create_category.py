from graphene_django_cud.mutations import DjangoCreateMutation
from ..models import Category


class CategoryCreateMutation(DjangoCreateMutation):
    """Create a new category"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']