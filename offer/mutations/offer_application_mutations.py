import graphene
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id
from decimal import Decimal, InvalidOperation
from offer.models import Offer, OfferApplication, ApplicationStatus
from graphql import GraphQLError


class OfferApplicationType(DjangoObjectType):
    class Meta:
        model = OfferApplication
        fields = "__all__"


class CreateOfferApplication(graphene.Mutation):
    class Arguments:
        offer_id = graphene.ID(required=True)
        proposal = graphene.String(required=True)
        asking_price = graphene.Float(required=True)

    ok = graphene.Boolean()
    application = graphene.Field(OfferApplicationType)

    def mutate(self, info, offer_id, proposal, asking_price):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError("You must be logged in.")
        try:
            asking_price = Decimal(str(asking_price))
        except (InvalidOperation, ValueError, TypeError):
            raise GraphQLError("Invalid asking price format.")

        # Decode Relay global ID if needed
        try:
            node_type, pk = from_global_id(offer_id)
            if node_type == 'OfferNode':
                offer_id = int(pk)
            else:
                offer_id = int(offer_id)
        except Exception:
            try:
                offer_id = int(offer_id)
            except (ValueError, TypeError):
                raise GraphQLError("Invalid offer ID format.")

        try:
            offer = Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            raise GraphQLError("Offer not found.")

        # empêcher double postulation
        if OfferApplication.objects.filter(offer=offer, user=user).exists():
            raise GraphQLError("You already applied to this offer.")

        application = OfferApplication.objects.create(
            offer=offer,
            user=user,
            proposal=proposal,
            asking_price=asking_price
        )

        return CreateOfferApplication(ok=True, application=application)
    
class UpdateOfferApplicationStatus(graphene.Mutation):
    class Arguments:
        application_id = graphene.ID(required=True)
        status = graphene.String(required=True)  

    ok = graphene.Boolean()
    application = graphene.Field(OfferApplicationType)

    def mutate(self, info, application_id, status):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError("You must be logged in.")

        if status not in [ApplicationStatus.APPROVED, ApplicationStatus.REJECTED]:
            raise GraphQLError("Invalid status.")

        # Decode Relay global ID if needed
        try:
            node_type, pk = from_global_id(application_id)
            if node_type == 'OfferApplicationNode':
                application_id = int(pk)
            else:
                application_id = int(application_id)
        except Exception:
            try:
                application_id = int(application_id)
            except (ValueError, TypeError):
                raise GraphQLError("Invalid application ID format.")

        try:
            application = OfferApplication.objects.select_related("offer").get(id=application_id)
        except OfferApplication.DoesNotExist:
            raise GraphQLError("Application not found.")

        # Vérifier que l'utilisateur est bien le créateur de l'offre
        if application.offer.created_by != user:
            raise GraphQLError("You are not allowed to accept/reject this application.")

        application.status = status
        application.save()

        return UpdateOfferApplicationStatus(ok=True, application=application)
