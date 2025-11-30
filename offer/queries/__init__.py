# Backward compatibility - import from organized queries folder
from .offer_queries import OfferQueries
from .offer_single import OfferSingleQuery
from .offer_list import OfferListQuery

__all__ = [
    'OfferQueries',
    'OfferSingleQuery',
    'OfferListQuery',
]
