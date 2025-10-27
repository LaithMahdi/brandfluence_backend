from django_filters import FilterSet,OrderingFilter
from .models import Category

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'is_active': ['exact'],
        }
        
    ordering = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('created', 'created'),
            ('modified', 'modified'),
        )
    )