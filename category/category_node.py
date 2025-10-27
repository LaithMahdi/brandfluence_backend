import graphene
from graphene_django_optimizer import OptimizedDjangoObjectType
from .models import Category
from .category_filter import CategoryFilter


class CategoryNode(OptimizedDjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'name': ['icontains', 'exact'],
            'is_active': ['exact'],
        }
        category_count = graphene.Int(description="Total number of categories")
        
        @classmethod
        def get_queryset(cls, queryset, info):
            return CategoryFilter(info.context.GET, queryset=queryset).qs