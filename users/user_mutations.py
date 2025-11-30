# Backward compatibility - import from organized mutations folder
from .mutations.user_mutations import UserMutations
from .mutations.auth_mutations import AuthMutations
from .mutations.influencer_mutations import InfluencerMutations
from .mutations.company_mutations import CompanyMutations

__all__ = [
    'UserMutations',
    'AuthMutations',
    'InfluencerMutations',
    'CompanyMutations',
]
