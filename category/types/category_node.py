import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from django.utils import timezone
from ..models import Category


class CategoryConnection(relay.Connection):
    """Connection for Category with totalCount and offset pagination support"""
    
    total_count = graphene.Int()
    
    class Meta:
        abstract = True
    
    def resolve_total_count(root, info, **kwargs):
        """Resolve total count from stored length or iterable"""
        return root.length if hasattr(root, 'length') else (
            root.iterable.count() if hasattr(root, 'iterable') and hasattr(root.iterable, 'count') else len(root.edges)
        )


class CategoryNode(DjangoObjectType):
    """GraphQL Node for Category - defines what data can be queried"""

    class Meta:
        model = Category
        interfaces = (relay.Node,)
        connection_class = CategoryConnection
    
    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related().prefetch_related()
