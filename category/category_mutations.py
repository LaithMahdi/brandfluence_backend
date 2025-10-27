"""
DEPRECATED: This file is kept for backward compatibility.
Use the organized mutations from the mutations/ folder instead.

Import the organized mutations from mutations/category_mutations.py
"""

# Import from the new organized structure
from .mutations.category_mutations import CategoryMutations
from .mutations.create_category import CategoryCreateMutation
from .mutations.update_category import CategoryUpdateMutation
from .mutations.delete_category import CategoryDeleteMutation, CategoryBatchDeleteMutation
from .mutations.patch_category import CategoryPatchMutation
from .mutations.batch_create_category import CategoryBatchCreateMutation

# Re-export for backward compatibility
__all__ = [
    'CategoryMutations',
    'CategoryCreateMutation',
    'CategoryUpdateMutation',
    'CategoryDeleteMutation',
    'CategoryBatchDeleteMutation',
    'CategoryPatchMutation',
    'CategoryBatchCreateMutation',
]
        
