import graphene

from offer.mutations.offer_mutations import OfferMutations
from offer.queries.offer_queries import OfferQueries
from .queries.user_queries import UserQueries
from .queries.influencer_queries import InfluencerQueries
from .queries.company_queries import CompanyQueries
from .mutations.user_mutations import UserMutations
from .mutations.auth_mutations import AuthMutations
from .mutations.influencer_mutations import InfluencerMutations
from .mutations.company_mutations import CompanyMutations
from .mutations.settings_mutations import (
    UpdateNotificationPreferences,
    UpdatePrivacySettings,
    GetNotificationPreferences,
    GetPrivacySettings
)


class Query(UserQueries, InfluencerQueries, CompanyQueries, OfferQueries, GetNotificationPreferences, GetPrivacySettings, graphene.ObjectType):
    """Users app queries"""
    pass


class Mutation(UserMutations, AuthMutations, InfluencerMutations, CompanyMutations, OfferMutations, graphene.ObjectType):
    """Users app mutations"""
    update_notification_preferences = UpdateNotificationPreferences.Field()
    update_privacy_settings = UpdatePrivacySettings.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
