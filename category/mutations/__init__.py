"""
Category mutations package.
Contains all GraphQL mutations for Category model.
"""

from .category_mutations import CategoryMutations
from .create_category import CategoryCreateMutation
from .update_category import CategoryUpdateMutation
from .delete_category import CategoryDeleteMutation, CategoryBatchDeleteMutation
from .patch_category import CategoryPatchMutation
from .batch_create_category import CategoryBatchCreateMutation

__all__ = [
    'CategoryMutations',
    'CategoryCreateMutation',
    'CategoryUpdateMutation',
    'CategoryDeleteMutation',
    'CategoryBatchDeleteMutation',
    'CategoryPatchMutation',
    'CategoryBatchCreateMutation',
]