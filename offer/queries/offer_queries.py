import graphene
from .offer_single import OfferSingleQuery
from .offer_list import OfferListQuery

class OfferQueries(OfferSingleQuery, OfferListQuery):
    """All offer queries in one place"""
    pass
