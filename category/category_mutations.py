import graphene
from graphene_django_cud.mutations import DjangoCreateMutation,DjangoUpdateMutation,DjangoDeleteMutation,DjangoBatchDeleteMutation,DjangoPatchMutation,DjangoBatchCreateMutation
from .models import Category

class CategoryCreateMutation(DjangoCreateMutation):
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Create a new Category"
    
class CategoryUpdateMutation(DjangoUpdateMutation):
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Update an existing Category"
        
class CategoryDeleteMutation(DjangoDeleteMutation):
    class Meta:
        model = Category
        description = "Delete an existing Category"
        
class CategoryBatchDeleteMutation(DjangoBatchDeleteMutation):
    class Meta:
        model = Category
        description = "Batch delete Categories"
        
class CategoryPatchMutation(DjangoPatchMutation):
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Patch an existing Category"
        
class CategoryBatchCreateMutation(DjangoBatchCreateMutation):
    class Meta:
        model = Category
        exclude = ['created', 'modified']
        description = "Batch create Categories"
        
class CategoryMutations(graphene.ObjectType):
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()
    batch_delete_categories = CategoryBatchDeleteMutation.Field()
    patch_category = CategoryPatchMutation.Field()
    batch_create_categories = CategoryBatchCreateMutation.Field()
        
