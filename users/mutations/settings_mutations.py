import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError

from users.models import User, NotificationPreferences, PrivacySettings


class NotificationPreferencesType(graphene.ObjectType):
    """GraphQL type for NotificationPreferences"""
    email_notifications = graphene.Boolean()
    new_applications = graphene.Boolean()
    messages = graphene.Boolean()
    campaign_updates = graphene.Boolean()
    weekly_report = graphene.Boolean()
    push_notifications = graphene.Boolean()


class PrivacySettingsType(graphene.ObjectType):
    """GraphQL type for PrivacySettings"""
    profile_visibility = graphene.Boolean()
    show_email = graphene.Boolean()
    show_phone = graphene.Boolean()
    searchable = graphene.Boolean()
    allow_analytics = graphene.Boolean()


class UpdateNotificationPreferences(graphene.Mutation):
    """Update user notification preferences"""
    success = graphene.Boolean()
    message = graphene.String()
    preferences = graphene.Field(NotificationPreferencesType)
    
    class Arguments:
        email_notifications = graphene.Boolean()
        new_applications = graphene.Boolean()
        messages = graphene.Boolean()
        campaign_updates = graphene.Boolean()
        weekly_report = graphene.Boolean()
        push_notifications = graphene.Boolean()
    
    @login_required
    def mutate(
        self, info,
        email_notifications=None,
        new_applications=None,
        messages=None,
        campaign_updates=None,
        weekly_report=None,
        push_notifications=None
    ):
        user = info.context.user
        
        try:
            # Get or create preferences
            preferences, created = NotificationPreferences.objects.get_or_create(user=user)
            
            # Update fields if provided
            if email_notifications is not None:
                preferences.email_notifications = email_notifications
            if new_applications is not None:
                preferences.new_applications = new_applications
            if messages is not None:
                preferences.messages = messages
            if campaign_updates is not None:
                preferences.campaign_updates = campaign_updates
            if weekly_report is not None:
                preferences.weekly_report = weekly_report
            if push_notifications is not None:
                preferences.push_notifications = push_notifications
            
            preferences.save()
            
            # Create response object
            prefs_obj = NotificationPreferencesType(
                email_notifications=preferences.email_notifications,
                new_applications=preferences.new_applications,
                messages=preferences.messages,
                campaign_updates=preferences.campaign_updates,
                weekly_report=preferences.weekly_report,
                push_notifications=preferences.push_notifications
            )
            
            return UpdateNotificationPreferences(
                success=True,
                message='Notification preferences updated successfully',
                preferences=prefs_obj
            )
            
        except Exception as e:
            raise GraphQLError(f'Failed to update notification preferences: {str(e)}')


class UpdatePrivacySettings(graphene.Mutation):
    """Update user privacy settings"""
    success = graphene.Boolean()
    message = graphene.String()
    settings = graphene.Field(PrivacySettingsType)
    
    class Arguments:
        profile_visibility = graphene.Boolean()
        show_email = graphene.Boolean()
        show_phone = graphene.Boolean()
        searchable = graphene.Boolean()
        allow_analytics = graphene.Boolean()
    
    @login_required
    def mutate(
        self, info,
        profile_visibility=None,
        show_email=None,
        show_phone=None,
        searchable=None,
        allow_analytics=None
    ):
        user = info.context.user
        
        try:
            # Get or create settings
            settings, created = PrivacySettings.objects.get_or_create(user=user)
            
            # Update fields if provided
            if profile_visibility is not None:
                settings.profile_visibility = profile_visibility
            if show_email is not None:
                settings.show_email = show_email
            if show_phone is not None:
                settings.show_phone = show_phone
            if searchable is not None:
                settings.searchable = searchable
            if allow_analytics is not None:
                settings.allow_analytics = allow_analytics
            
            settings.save()
            
            # Create response object
            settings_obj = PrivacySettingsType(
                profile_visibility=settings.profile_visibility,
                show_email=settings.show_email,
                show_phone=settings.show_phone,
                searchable=settings.searchable,
                allow_analytics=settings.allow_analytics
            )
            
            return UpdatePrivacySettings(
                success=True,
                message='Privacy settings updated successfully',
                settings=settings_obj
            )
            
        except Exception as e:
            raise GraphQLError(f'Failed to update privacy settings: {str(e)}')


class GetNotificationPreferences(graphene.ObjectType):
    """Query to get user notification preferences"""
    notification_preferences = graphene.Field(NotificationPreferencesType)
    
    @login_required
    def resolve_notification_preferences(self, info):
        user = info.context.user
        
        try:
            preferences, created = NotificationPreferences.objects.get_or_create(user=user)
            
            return NotificationPreferencesType(
                email_notifications=preferences.email_notifications,
                new_applications=preferences.new_applications,
                messages=preferences.messages,
                campaign_updates=preferences.campaign_updates,
                weekly_report=preferences.weekly_report,
                push_notifications=preferences.push_notifications
            )
        except Exception as e:
            raise GraphQLError(f'Failed to get notification preferences: {str(e)}')


class GetPrivacySettings(graphene.ObjectType):
    """Query to get user privacy settings"""
    privacy_settings = graphene.Field(PrivacySettingsType)
    
    @login_required
    def resolve_privacy_settings(self, info):
        user = info.context.user
        
        try:
            settings, created = PrivacySettings.objects.get_or_create(user=user)
            
            return PrivacySettingsType(
                profile_visibility=settings.profile_visibility,
                show_email=settings.show_email,
                show_phone=settings.show_phone,
                searchable=settings.searchable,
                allow_analytics=settings.allow_analytics
            )
        except Exception as e:
            raise GraphQLError(f'Failed to get privacy settings: {str(e)}')
