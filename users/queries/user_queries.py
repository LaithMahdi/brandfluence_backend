import graphene
from .user_single import UserSingleQuery
from .user_list import UserListQuery


class UserQueries(UserSingleQuery, UserListQuery):
    """All user queries in one place"""
    pass