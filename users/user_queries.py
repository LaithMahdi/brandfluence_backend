# Backward compatibility - import from organized queries folder
from .queries.user_queries import UserQueries
from .queries.influencer_queries import InfluencerQueries
from .queries.company_queries import CompanyQueries

__all__ = [
    'UserQueries',
    'InfluencerQueries',
    'CompanyQueries',
]
