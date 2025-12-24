import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q, Count
from datetime import datetime, timedelta

from offer.models import Offer, OfferApplication, ApplicationStatus
from offer.types.Offer_Node import OfferNode


class OfferApplicationType(DjangoObjectType):
    """GraphQL type for OfferApplication"""
    
    class Meta:
        model = OfferApplication
        fields = ('id', 'offer', 'user', 'proposal', 'asking_price', 'status', 'submitted_at')


class RecentOfferType(graphene.ObjectType):
    """Simplified offer type for dashboard"""
    id = graphene.ID()
    title = graphene.String()
    min_budget = graphene.Decimal()
    max_budget = graphene.Decimal()
    start_date = graphene.Date()
    end_date = graphene.Date()
    influencer_number = graphene.Int()
    created_at = graphene.DateTime()


class RecentApplicationType(graphene.ObjectType):
    """Application type for dashboard"""
    id = graphene.ID()
    offer = graphene.Field(lambda: SimpleOfferType)
    user = graphene.Field(lambda: SimpleUserType)
    status = graphene.String()
    asking_price = graphene.Decimal()
    submitted_at = graphene.DateTime()


class SimpleOfferType(graphene.ObjectType):
    """Simplified offer for nested use"""
    id = graphene.ID()
    title = graphene.String()


class SimpleUserType(graphene.ObjectType):
    """Simplified user for nested use"""
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()


class CompanyDashboardStatsType(graphene.ObjectType):
    """Dashboard statistics for companies"""
    total_offers = graphene.Int()
    active_offers = graphene.Int()
    total_applications = graphene.Int()
    pending_applications = graphene.Int()
    approved_applications = graphene.Int()
    rejected_applications = graphene.Int()
    recent_offers = graphene.List(RecentOfferType)
    recent_applications = graphene.List(RecentApplicationType)


class DashboardStatsQuery(graphene.ObjectType):
    """Query for company dashboard statistics"""
    
    company_dashboard_stats = graphene.Field(CompanyDashboardStatsType)

    def resolve_company_dashboard_stats(self, info):
        """Resolve company dashboard statistics"""
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Vous devez être connecté pour accéder au tableau de bord")

        # Get all offers created by this user (company)
        user_offers = Offer.objects.filter(created_by=user)
        
        # Calculate active offers (ongoing campaigns)
        today = datetime.now().date()
        active_offers = user_offers.filter(
            start_date__lte=today,
            end_date__gte=today
        )

        # Get all applications for user's offers
        all_applications = OfferApplication.objects.filter(offer__created_by=user)

        # Count applications by status
        pending_count = all_applications.filter(status=ApplicationStatus.PENDING).count()
        approved_count = all_applications.filter(status=ApplicationStatus.APPROVED).count()
        rejected_count = all_applications.filter(status=ApplicationStatus.REJECTED).count()

        # Get recent offers (last 10)
        recent_offers = user_offers.order_by('-created_at')[:10]
        recent_offers_data = [
            RecentOfferType(
                id=offer.id,
                title=offer.title,
                min_budget=offer.min_budget,
                max_budget=offer.max_budget,
                start_date=offer.start_date,
                end_date=offer.end_date,
                influencer_number=offer.influencer_number,
                created_at=offer.created_at
            )
            for offer in recent_offers
        ]

        # Get recent applications (last 10)
        recent_applications = all_applications.select_related('offer', 'user').order_by('-submitted_at')[:10]
        recent_applications_data = [
            RecentApplicationType(
                id=app.id,
                offer=SimpleOfferType(id=app.offer.id, title=app.offer.title),
                user=SimpleUserType(id=app.user.id, name=app.user.name, email=app.user.email),
                status=app.status,
                asking_price=app.asking_price,
                submitted_at=app.submitted_at
            )
            for app in recent_applications
        ]

        return CompanyDashboardStatsType(
            total_offers=user_offers.count(),
            active_offers=active_offers.count(),
            total_applications=all_applications.count(),
            pending_applications=pending_count,
            approved_applications=approved_count,
            rejected_applications=rejected_count,
            recent_offers=recent_offers_data,
            recent_applications=recent_applications_data
        )
