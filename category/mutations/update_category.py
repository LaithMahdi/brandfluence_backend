from graphene_django_cud.mutations import DjangoUpdateMutation
from ..models import Category


class CategoryUpdateMutation(DjangoUpdateMutation):
    """Update an existing category"""
    
    class Meta:
        model = Category
        exclude = ['created', 'modified']