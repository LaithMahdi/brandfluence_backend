# Category Mutations

This folder contains all GraphQL mutations for the Category model, organized by functionality.

## Structure

```
mutations/
├── __init__.py                 # Package initialization and imports
├── category_mutations.py       # Main mutations collection
├── create_category.py          # Category creation mutation
├── update_category.py          # Category update mutation
├── delete_category.py          # Category deletion mutations
├── patch_category.py           # Category patch mutation
└── batch_create_category.py    # Batch category creation mutation
```

## Available Mutations

### Single Item Operations

- **CategoryCreateMutation**: Create a new category
- **CategoryUpdateMutation**: Update an existing category
- **CategoryDeleteMutation**: Delete a single category
- **CategoryPatchMutation**: Partially update a category

### Batch Operations

- **CategoryBatchCreateMutation**: Create multiple categories at once
- **CategoryBatchDeleteMutation**: Delete multiple categories at once

## Usage

Import the mutations collection in your schema:

```python
from category.mutations import CategoryMutations

class Mutation(CategoryMutations, graphene.ObjectType):
    pass
```

## Extending Mutations

To add new mutations:

1. Create a new file in this folder
2. Define your mutation class
3. Add the import to `__init__.py`
4. Include it in `category_mutations.py`

## Security

Each mutation class includes permission hooks that can be overridden:

```python
@classmethod
def get_permissions(cls, root, info, input):
    # Add your permission logic here
    return []
```

## Validation

Use the `before_save` hook for custom validation:

```python
@classmethod
def before_save(cls, root, info, input, obj):
    # Add validation logic here
    pass
```
