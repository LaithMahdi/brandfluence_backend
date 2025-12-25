import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from ..models import OfferApplication


class OfferApplicationConnection(relay.Connection):
    """Connection for OfferApplication with totalCount support"""
    
    total_count = graphene.Int()
    pending_count = graphene.Int()
    approved_count = graphene.Int()
    rejected_count = graphene.Int()
    
    class Meta:
        abstract = True
    
    def resolve_total_count(root, info, **kwargs):
        """Resolve total count"""
        return root.length if hasattr(root, 'length') else (
            root.iterable.count() if hasattr(root, 'iterable') and hasattr(root.iterable, 'count') else len(root.edges)
        )
    
    def resolve_pending_count(root, info, **kwargs):
        """Count of pending applications"""
        if hasattr(root, 'iterable') and hasattr(root.iterable, 'filter'):
            return root.iterable.filter(status='Pending').count()
        return 0
    
    def resolve_approved_count(root, info, **kwargs):
        """Count of approved applications"""
        if hasattr(root, 'iterable') and hasattr(root.iterable, 'filter'):
            return root.iterable.filter(status='Approved').count()
        return 0
    
    def resolve_rejected_count(root, info, **kwargs):
        """Count of rejected applications"""
        if hasattr(root, 'iterable') and hasattr(root.iterable, 'filter'):
            return root.iterable.filter(status='Rejected').count()
        return 0


class OfferApplicationNode(DjangoObjectType):
    """GraphQL Node for OfferApplication"""
    
    is_pending = graphene.Boolean()
    is_approved = graphene.Boolean()
    is_rejected = graphene.Boolean()
    can_edit = graphene.Boolean()
    can_withdraw = graphene.Boolean()

    class Meta:
        model = OfferApplication
        interfaces = (relay.Node,)
        connection_class = OfferApplicationConnection
        fields = '__all__'
    
    @classmethod
    def get_queryset(cls, queryset, info):
        """Optimize queryset to reduce database hits"""
        return queryset.select_related(
            'offer',
            'user',
            'reviewed_by'
        ).prefetch_related(
            'offer__created_by'
        )
    
    def resolve_is_pending(self, info):
        return self.is_pending
    
    def resolve_is_approved(self, info):
        return self.is_approved
    
    def resolve_is_rejected(self, info):
        return self.is_rejected
    
    def resolve_can_edit(self, info):
        """Check if current user can edit this application"""
        user = info.context.user
        if not user.is_authenticated:
            return False
        # Only the applicant can edit, and only if pending
        return self.user_id == user.id and self.is_pending
    
    def resolve_can_withdraw(self, info):
        """Check if current user can withdraw this application"""
        user = info.context.user
        if not user.is_authenticated:
            return False
        # Only the applicant can withdraw, and only if pending or approved
        return self.user_id == user.id and self.status in ['Pending', 'Approved']
