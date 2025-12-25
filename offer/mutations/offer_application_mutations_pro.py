"""
Professional Offer Application Mutations
Complete CRUD operations with proper permissions and validations
"""

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from django.utils import timezone
from django.db import transaction

from ..models import Offer, OfferApplication, ApplicationStatus
from ..types.OfferApplication_Node import OfferApplicationNode
from users.utils import check_user_role


class CreateOfferApplicationInput(graphene.InputObjectType):
    """Input for creating an offer application"""
    offer_id = graphene.ID(required=True)
    proposal = graphene.String(required=True)
    asking_price = graphene.Decimal(required=True)
    cover_letter = graphene.String()
    estimated_reach = graphene.Int()
    delivery_days = graphene.Int()
    portfolio_links = graphene.List(graphene.String)


class UpdateOfferApplicationInput(graphene.InputObjectType):
    """Input for updating an offer application"""
    application_id = graphene.ID(required=True)
    proposal = graphene.String()
    asking_price = graphene.Decimal()
    cover_letter = graphene.String()
    estimated_reach = graphene.Int()
    delivery_days = graphene.Int()
    portfolio_links = graphene.List(graphene.String)


class ReviewApplicationInput(graphene.InputObjectType):
    """Input for reviewing an application (admin only)"""
    application_id = graphene.ID(required=True)
    status = graphene.String(required=True)
    rejection_reason = graphene.String()
    admin_notes = graphene.String()


class CreateOfferApplication(graphene.Mutation):
    """Create a new offer application (influencer only)"""
    
    class Arguments:
        input = CreateOfferApplicationInput(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    application = graphene.Field(OfferApplicationNode)
    errors = graphene.List(graphene.String)
    
    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, input):
        user = info.context.user
        errors = []
        
        # Check if user is an influencer
        if not check_user_role(user, 'INFLUENCER'):
            return cls(
                success=False,
                message="Only influencers can apply to offers",
                application=None,
                errors=["PERMISSION_DENIED"]
            )
        
        # Validate offer exists
        # Decode Relay global ID if needed
        offer_id = input.offer_id
        print("----------------------- offer_id: ---------------- ", offer_id)
        try:
            node_type, pk = from_global_id(offer_id)
            if node_type == 'OfferNode':
                offer_id = int(pk)
            else:
                # If it decoded but wrong type, try to use as regular ID
                offer_id = int(offer_id)
        except Exception:
            # If decoding fails, try to use as regular integer ID
            try:
                offer_id = int(offer_id)
            except (ValueError, TypeError):
                return cls(
                    success=False,
                    message="Invalid offer ID format",
                    application=None,
                    errors=["INVALID_OFFER_ID"]
                )
        
        try:
            offer = Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            return cls(
                success=False,
                message="Offer not found",
                application=None,
                errors=["OFFER_NOT_FOUND"]
            )
        
        # Check if offer is still active
        if offer.end_date < timezone.now().date():
            return cls(
                success=False,
                message="This offer has expired",
                application=None,
                errors=["OFFER_EXPIRED"]
            )
        
        # Check if user already applied
        if OfferApplication.objects.filter(offer=offer, user=user).exists():
            return cls(
                success=False,
                message="You have already applied to this offer",
                application=None,
                errors=["DUPLICATE_APPLICATION"]
            )
        
        # Validate asking price is within budget
        if input.asking_price < offer.min_budget or input.asking_price > offer.max_budget:
            errors.append("PRICE_OUT_OF_RANGE")
        
        # Validate delivery days if provided
        if input.get('delivery_days') and input.delivery_days < 1:
            errors.append("INVALID_DELIVERY_DAYS")
        
        if errors:
            return cls(
                success=False,
                message="Validation errors occurred",
                application=None,
                errors=errors
            )
        
        # Create application
        application = OfferApplication.objects.create(
            offer=offer,
            user=user,
            proposal=input.proposal,
            asking_price=input.asking_price,
            cover_letter=input.get('cover_letter', ''),
            estimated_reach=input.get('estimated_reach'),
            delivery_days=input.get('delivery_days'),
            portfolio_links=input.get('portfolio_links', [])
        )
        
        return cls(
            success=True,
            message="Application submitted successfully",
            application=application,
            errors=[]
        )


class UpdateOfferApplication(graphene.Mutation):
    """Update an existing offer application (applicant only, pending status only)"""
    
    class Arguments:
        input = UpdateOfferApplicationInput(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    application = graphene.Field(OfferApplicationNode)
    errors = graphene.List(graphene.String)
    
    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, input):
        user = info.context.user
        errors = []
        
        # Decode Relay global ID if needed
        application_id = input.application_id
        try:
            node_type, pk = from_global_id(application_id)
            if node_type == 'OfferApplicationNode':
                application_id = int(pk)
        except Exception:
            pass  # If it's not a global ID, use it as is
        
        # Get application
        try:
            application = OfferApplication.objects.select_related('offer').get(
                id=application_id
            )
        except OfferApplication.DoesNotExist:
            return cls(
                success=False,
                message="Application not found",
                application=None,
                errors=["APPLICATION_NOT_FOUND"]
            )
        
        # Check permissions
        if application.user_id != user.id:
            return cls(
                success=False,
                message="You can only update your own applications",
                application=None,
                errors=["PERMISSION_DENIED"]
            )
        
        # Check if application is still pending
        if application.status != ApplicationStatus.PENDING:
            return cls(
                success=False,
                message="You can only update pending applications",
                application=None,
                errors=["INVALID_STATUS"]
            )
        
        # Update fields
        if input.get('proposal'):
            application.proposal = input.proposal
        
        if input.get('asking_price'):
            # Validate price is within budget
            if input.asking_price < application.offer.min_budget or input.asking_price > application.offer.max_budget:
                errors.append("PRICE_OUT_OF_RANGE")
            else:
                application.asking_price = input.asking_price
        
        if input.get('cover_letter') is not None:
            application.cover_letter = input.cover_letter
        
        if input.get('estimated_reach') is not None:
            application.estimated_reach = input.estimated_reach
        
        if input.get('delivery_days') is not None:
            if input.delivery_days < 1:
                errors.append("INVALID_DELIVERY_DAYS")
            else:
                application.delivery_days = input.delivery_days
        
        if input.get('portfolio_links') is not None:
            application.portfolio_links = input.portfolio_links
        
        if errors:
            return cls(
                success=False,
                message="Validation errors occurred",
                application=None,
                errors=errors
            )
        
        application.save()
        
        return cls(
            success=True,
            message="Application updated successfully",
            application=application,
            errors=[]
        )


class WithdrawOfferApplication(graphene.Mutation):
    """Withdraw an application (set status to WITHDRAW)"""
    
    class Arguments:
        application_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    application = graphene.Field(OfferApplicationNode)
    
    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, application_id):
        user = info.context.user
        
        # Decode Relay global ID if needed
        try:
            node_type, pk = from_global_id(application_id)
            if node_type == 'OfferApplicationNode':
                application_id = int(pk)
        except Exception:
            pass  # If it's not a global ID, use it as is
        
        try:
            application = OfferApplication.objects.get(id=application_id)
        except OfferApplication.DoesNotExist:
            return cls(
                success=False,
                message="Application not found",
                application=None
            )
        
        # Check permissions
        if application.user_id != user.id:
            return cls(
                success=False,
                message="You can only withdraw your own applications",
                application=None
            )
        
        # Check if can be withdrawn
        if application.status not in [ApplicationStatus.PENDING, ApplicationStatus.APPROVED]:
            return cls(
                success=False,
                message="You can only withdraw pending or approved applications",
                application=None
            )
        
        application.status = ApplicationStatus.WITHDRAW
        application.save()
        
        return cls(
            success=True,
            message="Application withdrawn successfully",
            application=application
        )


class ReviewOfferApplication(graphene.Mutation):
    """Review an application - approve or reject (offer creator or admin only)"""
    
    class Arguments:
        input = ReviewApplicationInput(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    application = graphene.Field(OfferApplicationNode)
    errors = graphene.List(graphene.String)
    
    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, input):
        user = info.context.user
        
        # Validate status
        if input.status not in [ApplicationStatus.APPROVED, ApplicationStatus.REJECTED]:
            return cls(
                success=False,
                message="Status must be APPROVED or REJECTED",
                application=None,
                errors=["INVALID_STATUS"]
            )
        
        # Decode Relay global ID if needed
        application_id = input.application_id
        try:
            node_type, pk = from_global_id(application_id)
            if node_type == 'OfferApplicationNode':
                application_id = int(pk)
        except Exception:
            pass  # If it's not a global ID, use it as is
        
        # Get application
        try:
            application = OfferApplication.objects.select_related('offer').get(
                id=application_id
            )
        except OfferApplication.DoesNotExist:
            return cls(
                success=False,
                message="Application not found",
                application=None,
                errors=["APPLICATION_NOT_FOUND"]
            )
        
        # Check permissions (must be offer creator or admin)
        is_offer_creator = application.offer.created_by_id == user.id
        is_admin = user.is_staff or user.is_superuser
        
        if not (is_offer_creator or is_admin):
            return cls(
                success=False,
                message="You don't have permission to review this application",
                application=None,
                errors=["PERMISSION_DENIED"]
            )
        
        # Check if application is pending
        if application.status != ApplicationStatus.PENDING:
            return cls(
                success=False,
                message="You can only review pending applications",
                application=None,
                errors=["INVALID_STATUS"]
            )
        
        # Update application
        application.status = input.status
        application.reviewed_by = user
        application.reviewed_at = timezone.now()
        
        if input.get('rejection_reason'):
            application.rejection_reason = input.rejection_reason
        
        if input.get('admin_notes'):
            application.admin_notes = input.admin_notes
        
        application.save()
        
        status_text = "approved" if input.status == ApplicationStatus.APPROVED else "rejected"
        
        return cls(
            success=True,
            message=f"Application {status_text} successfully",
            application=application,
            errors=[]
        )


class DeleteOfferApplication(graphene.Mutation):
    """Delete an application (admin only or applicant if pending)"""
    
    class Arguments:
        application_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, application_id):
        user = info.context.user
        
        # Decode Relay global ID if needed
        try:
            node_type, pk = from_global_id(application_id)
            if node_type == 'OfferApplicationNode':
                application_id = int(pk)
        except Exception:
            pass  # If it's not a global ID, use it as is
        
        try:
            application = OfferApplication.objects.get(id=application_id)
        except OfferApplication.DoesNotExist:
            return cls(
                success=False,
                message="Application not found"
            )
        
        # Check permissions
        is_owner = application.user_id == user.id
        is_admin = user.is_staff or user.is_superuser
        can_delete = is_admin or (is_owner and application.status == ApplicationStatus.PENDING)
        
        if not can_delete:
            return cls(
                success=False,
                message="You don't have permission to delete this application"
            )
        
        application.delete()
        
        return cls(
            success=True,
            message="Application deleted successfully"
        )


class OfferApplicationMutations(graphene.ObjectType):
    """All offer application mutations"""
    create_offer_application = CreateOfferApplication.Field()
    update_offer_application = UpdateOfferApplication.Field()
    withdraw_offer_application = WithdrawOfferApplication.Field()
    review_offer_application = ReviewOfferApplication.Field()
    delete_offer_application = DeleteOfferApplication.Field()
