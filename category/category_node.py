import graphene
from graphene_django_optimizer import OptimizedDjangoObjectType
from django.utils import timezone
from .models import Category


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


class CategoryConnection(graphene.relay.Connection):
    """Connection that adds totalCount to category queries"""
    
    total_count = graphene.Int()
    
    class Meta:
        node = CategoryNode
    
    def resolve_total_count(self, info, **kwargs):
        # Use the length of iterable if it's a queryset
        if hasattr(self, 'iterable'):
            if hasattr(self.iterable, 'count'):
                return self.iterable.count()
            return len(self.iterable)
        return 0