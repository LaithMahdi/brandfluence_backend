import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from ..models import Category
from ..category_node import CategoryNode, CategoryConnection
from ..category_filter import CategoryFilter
from common.pagination_utils import OffsetConnectionField


class CategoryListQuery(graphene.ObjectType):
    """Query to get all categories with pagination and totalCount"""
    
    # Use OffsetConnectionField for automatic offset pagination support
    all_categories = OffsetConnectionField(
        CategoryConnection,
        # Add filter arguments
        name_Icontains=graphene.String(),
        name_Istartswith=graphene.String(),
        description_Icontains=graphene.String(),
        is_active=graphene.Boolean(),
        order_by=graphene.String(),
    )
    
    def resolve_all_categories(self, info, **kwargs):
        qs = Category.objects.all()
        
        # Apply filters manually
        if 'name_Icontains' in kwargs:
            qs = qs.filter(name__icontains=kwargs['name_Icontains'])
        if 'name_Istartswith' in kwargs:
            qs = qs.filter(name__istartswith=kwargs['name_Istartswith'])
        if 'description_Icontains' in kwargs:
            qs = qs.filter(description__icontains=kwargs['description_Icontains'])
        if 'is_active' in kwargs:
            qs = qs.filter(is_active=kwargs['is_active'])
        
        # Apply ordering
        order_by = kwargs.get('order_by', '-created')
        qs = qs.order_by(order_by)
        
        # Return the full queryset - OffsetConnectionField handles pagination
        return qs