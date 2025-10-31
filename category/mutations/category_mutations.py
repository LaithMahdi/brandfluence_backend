import graphene
from .category_mutations_all import (
    CategoryCreateMutation,
    CategoryUpdateMutation,
    CategoryPatchMutation,
    CategoryDeleteMutation,
    CategoryBatchCreateMutation,
    CategoryBatchDeleteMutation
)


class CategoryMutations(graphene.ObjectType):
    """All category mutations in one place"""
    
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    patch_category = CategoryPatchMutation.Field()
    delete_category = CategoryDeleteMutation.Field()
    batch_create_categories = CategoryBatchCreateMutation.Field()
    batch_delete_categories = CategoryBatchDeleteMutation.Field()