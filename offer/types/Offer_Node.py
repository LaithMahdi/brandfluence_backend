import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from ..models import Offer


class OfferConnection(relay.Connection):
    """Connection for Offer with totalCount and offset pagination support"""
    
    total_count = graphene.Int()
    
    class Meta:
        abstract = True
    
    def resolve_total_count(root, info, **kwargs):
        """Resolve total count from stored length or iterable"""
        return root.length if hasattr(root, 'length') else (
            root.iterable.count() if hasattr(root, 'iterable') and hasattr(root.iterable, 'count') else len(root.edges)
        )


class OfferNode(DjangoObjectType):
    """GraphQL Node for Offer - defines what data can be queried"""

    class Meta:
        model = Offer
        interfaces = (relay.Node,)
        connection_class = OfferConnection
    
    @classmethod
    def get_queryset(cls, queryset, info):
        """Optimize queryset to reduce database hits"""
        return queryset.select_related('created_by').prefetch_related('applications')
