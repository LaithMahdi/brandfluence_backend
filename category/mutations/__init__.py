"""
Category mutations package.
Contains all GraphQL mutations for Category model.
"""

# Import from consolidated mutations file
from .category_mutations_all import (
    CategoryCreateMutation,
    CategoryUpdateMutation,
    CategoryPatchMutation,
    CategoryDeleteMutation,
    CategoryBatchCreateMutation,
    CategoryBatchDeleteMutation
)

# Import the mutations class for schema
from .category_mutations import CategoryMutations

__all__ = [
    'CategoryMutations',
    'CategoryCreateMutation',
    'CategoryUpdateMutation',
    'CategoryDeleteMutation',
    'CategoryBatchDeleteMutation',
    'CategoryPatchMutation',
    'CategoryBatchCreateMutation',
]