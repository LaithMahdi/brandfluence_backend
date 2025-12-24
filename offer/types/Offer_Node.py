import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from ..models import Offer, OfferApplication


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


class OfferApplicationType(DjangoObjectType):
    """GraphQL type for OfferApplication"""
    class Meta:
        model = OfferApplication
        fields = ('id', 'offer', 'user', 'proposal', 'asking_price', 'status', 'submitted_at')


class OfferNode(DjangoObjectType):
    """GraphQL Node for Offer - defines what data can be queried"""
    
    applications = graphene.List(OfferApplicationType)

    class Meta:
        model = Offer
        interfaces = (relay.Node,)
        connection_class = OfferConnection
    
    def resolve_applications(self, info):
        """Resolve applications for this offer"""
        return self.applications.all()
    
    @classmethod
    def get_queryset(cls, queryset, info):
        """Optimize queryset to reduce database hits"""
        return queryset.select_related('created_by').prefetch_related('applications')

