import graphene
from .offer_single import OfferSingleQuery
from .offer_list import OfferListQuery
from .dashboard_stats import DashboardStatsQuery

class OfferQueries(OfferSingleQuery, OfferListQuery, DashboardStatsQuery):
    """All offer queries in one place"""
    pass
