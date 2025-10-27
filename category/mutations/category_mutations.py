import graphene
from .create_category import CategoryCreateMutation
from .update_category import CategoryUpdateMutation
from .delete_category import CategoryDeleteMutation, CategoryBatchDeleteMutation
from .patch_category import CategoryPatchMutation
from .batch_create_category import CategoryBatchCreateMutation


class CategoryMutations(graphene.ObjectType):
    """All category mutations in one place"""
    
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()
    patch_category = CategoryPatchMutation.Field()
    batch_create_categories = CategoryBatchCreateMutation.Field()
    batch_delete_categories = CategoryBatchDeleteMutation.Field()