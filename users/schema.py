import graphene
from .queries.user_queries import UserQueries
from .queries.influencer_queries import InfluencerQueries
from .queries.company_queries import CompanyQueries
from .mutations.user_mutations import UserMutations
from .mutations.auth_mutations import AuthMutations
from .mutations.influencer_mutations import InfluencerMutations
from .mutations.company_mutations import CompanyMutations


class Query(UserQueries, InfluencerQueries, CompanyQueries, graphene.ObjectType):
    """Users app queries"""
    pass


class Mutation(UserMutations, AuthMutations, InfluencerMutations, CompanyMutations, graphene.ObjectType):
    """Users app mutations"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
