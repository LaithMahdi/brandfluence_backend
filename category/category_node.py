import graphene
from graphene_django_optimizer import OptimizedDjangoObjectType
from django.utils import timezone
from .models import Category
from common.pagination_utils import PaginatedConnection


class CategoryNode(OptimizedDjangoObjectType):
    """GraphQL Node for Category - defines what data can be queried"""

    
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'is_active': ['exact'],
            'created': ['exact', 'gte', 'lte'],
            'modified': ['exact', 'gte', 'lte'],
        }

    
    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related().prefetch_related()


class CategoryConnection(PaginatedConnection):
    """Connection for Category with totalCount and offset pagination support"""
    
    class Meta:
        node = CategoryNode