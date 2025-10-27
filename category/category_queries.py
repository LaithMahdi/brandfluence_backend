"""
DEPRECATED: This file is kept for backward compatibility.
Use the organized queries from the queries/ folder instead.

Import the organized queries from queries/category_queries.py
"""

# Import from the new organized structure
from .queries.category_queries import CategoryQueries
from .queries.category_single import CategorySingleQuery
from .queries.category_list import CategoryListQuery

# Re-export for backward compatibility
__all__ = [
    'CategoryQueries',
    'CategorySingleQuery', 
    'CategoryListQuery',
]