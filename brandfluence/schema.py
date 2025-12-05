import graphene

from category import schema as category_schema
from users import schema as users_schema
from offer import schema as offer_schema

# IMPORT CORRIGÉ
from offer.mutations.offer_application_mutations import (
    CreateOfferApplication,
    UpdateOfferApplicationStatus,
)

class Query(
    users_schema.Query,
    category_schema.Query,
    offer_schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    users_schema.Mutation,
    category_schema.Mutation,
    offer_schema.Mutation,
    graphene.ObjectType
):
    create_offer_application = CreateOfferApplication.Field()
    update_offer_application_status = UpdateOfferApplicationStatus.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
