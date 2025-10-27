import graphene 
from graphene_django.filter import DjangoFilterConnectionField
from .models import Category
from .category_node import CategoryNode
from .category_filter import CategoryFilter

class Query(graphene.ObjectType):
    category = graphene.relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode, filterset_class=CategoryFilter)
    
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()