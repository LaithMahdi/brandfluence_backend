import graphene
from graphene_django import DjangoObjectType
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

        # un influencer only (si tu as un champ role dans User)
        # if user.role != "INFLUENCER":
        #     raise GraphQLError("Only influencers can apply to offers.")

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
