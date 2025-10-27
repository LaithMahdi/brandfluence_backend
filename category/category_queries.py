# Backward compatibility - import from organized queries folder
from .queries.category_queries import CategoryQueries
from .queries.category_single import CategorySingleQuery
from .queries.category_list import CategoryListQuery

__all__ = [
    'CategoryQueries',
    'CategorySingleQuery', 
    'CategoryListQuery',
]