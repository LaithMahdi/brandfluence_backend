"""
User queries package.
Contains all GraphQL queries for User model.
"""

from .user_queries import UserQueries
from .user_single import UserSingleQuery
from .user_list import UserListQuery
from .influencer_queries import InfluencerQueries
from .company_queries import CompanyQueries

__all__ = [
    'UserQueries',
    'UserSingleQuery',
    'UserListQuery',
    'InfluencerQueries',
    'CompanyQueries',
]
