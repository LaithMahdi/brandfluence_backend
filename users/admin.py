from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from .models import User, UserRole, VerifyToken, NotificationPreferences, PrivacySettings
from .influencer_models import (
    Influencer, ReseauSocial, InfluencerWork, Image,
    InstagramReel, InstagramPost,
    PortfolioMedia, OffreCollaboration, StatistiquesGlobales
)
from .company_models import Company, Address


class UserCreationForm(forms.ModelForm):
    """A form for creating new users with password confirmation"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=UserRole.choices(),
        initial=UserRole.INFLUENCER.value,
        required=True,
        help_text="Select the user's role"
    )
    
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'phone_number')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_role(self):
        """Ensure role is stored as enum value"""
        role = self.cleaned_data.get('role')
        if role and not role.startswith('EnumMeta'):
            return role
        return role
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Explicitly set the role value
        user.role = self.cleaned_data.get('role')
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users"""
    password = ReadOnlyPasswordHashField()
    role = forms.ChoiceField(
        choices=UserRole.choices(),
        required=True,
        help_text="Select the user's role"
    )
    
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'phone_number', 'phone_number_verified',
                  'email_verified', 'verified_at', 'is_verify_by_admin', 'role',
                  'is_banned', 'is_active', 'is_staff', 'is_superuser')
    
    def __init__(self, *args, **kwargs):
        """Initialize form with current role value"""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.role:
            # Set the initial value to the current role
            current_role = self.instance.role
            # Handle incorrectly stored roles like 'EnumMeta.COMPANY'
            if 'EnumMeta.' in str(current_role):
                current_role = str(current_role).split('.')[-1]
            self.fields['role'].initial = current_role
    
    def clean_role(self):
        """Ensure role is stored as enum value"""
        role = self.cleaned_data.get('role')
        if role and not role.startswith('EnumMeta'):
            return role
        return role
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Explicitly set the role value to ensure it's saved correctly
        user.role = self.cleaned_data.get('role')
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email', 'name', 'get_role_display', 'email_verified', 'is_verify_by_admin', 
                    'is_banned', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'is_banned',
                   'email_verified', 'phone_number_verified', 'is_verify_by_admin')
    
    def get_role_display(self, obj):
        """Display role as clean enum value"""
        if obj.role:
            # Handle incorrectly stored roles like 'EnumMeta.COMPANY'
            if 'EnumMeta.' in str(obj.role):
                return str(obj.role).split('.')[-1]
            return obj.role
        return None
    get_role_display.short_description = 'Role'
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure role is saved correctly"""
        if 'role' in form.cleaned_data:
            obj.role = form.cleaned_data['role']
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone_number', 'phone_number_verified')}),
        ('Verification', {'fields': ('email_verified', 'verified_at', 'is_verify_by_admin')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_banned',
                                     'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('-created_at',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    actions = ['verify_by_admin', 'ban_users', 'unban_users', 'verify_emails']
    
    def verify_by_admin(self, request, queryset):
        updated = queryset.update(is_verify_by_admin=True)
        self.message_user(request, f'{updated} user(s) verified by admin.')
    verify_by_admin.short_description = 'Verify selected users by admin'
    
    def ban_users(self, request, queryset):
        for user in queryset:
            user.ban_user()
        self.message_user(request, f'{queryset.count()} user(s) banned.')
    ban_users.short_description = 'Ban selected users'
    
    def unban_users(self, request, queryset):
        for user in queryset:
            user.unban_user()
        self.message_user(request, f'{queryset.count()} user(s) unbanned.')
    unban_users.short_description = 'Unban selected users'
    
    def verify_emails(self, request, queryset):
        for user in queryset:
            user.verify_email()
        self.message_user(request, f'{queryset.count()} email(s) verified.')
    verify_emails.short_description = 'Verify emails for selected users'


@admin.register(VerifyToken)
class VerifyTokenAdmin(admin.ModelAdmin):
    """Admin for VerifyToken model"""
    list_display = ('user', 'code', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__name', 'code', 'token')
    readonly_fields = ('token', 'code', 'created_at', 'expires_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Token Details', {'fields': ('token', 'code')}),
        ('Status', {'fields': ('is_used',)}),
        ('Dates', {'fields': ('created_at', 'expires_at')}),
    )
    
    def has_add_permission(self, request):
        # Prevent manual creation of tokens through admin
        return False


admin.site.register(User, UserAdmin)


# Inline admins for influencer related models
class ReseauSocialInline(admin.TabularInline):
    model = ReseauSocial
    extra = 1
    fields = ('plateforme', 'url_profil', 'nombre_abonnes', 'taux_engagement', 
              'moyenne_vues', 'moyenne_likes', 'moyenne_commentaires', 'frequence_publication')


class InfluencerWorkInline(admin.TabularInline):
    model = InfluencerWork
    extra = 0
    fields = ('brand_name', 'campaign', 'period', 'results', 'publication_link')


class ImageInline(GenericTabularInline):
    model = Image
    extra = 1
    fields = ('url', 'is_default', 'is_public', 'created_at')
    readonly_fields = ('created_at',)


class InstagramReelInline(admin.TabularInline):
    model = InstagramReel
    extra = 0
    fields = ('instagram_id', 'post_name', 'likes', 'comments', 'views', 'taken_at')
    readonly_fields = ('instagram_id', 'taken_at')


class InstagramPostInline(admin.TabularInline):
    model = InstagramPost
    extra = 0
    fields = ('instagram_id', 'media_type', 'post_name', 'likes', 'comments', 'taken_at')
    readonly_fields = ('instagram_id', 'taken_at')


class PortfolioMediaInline(admin.TabularInline):
    model = PortfolioMedia
    extra = 0
    fields = ('titre', 'image_url', 'description', 'date_creation')


class OffreCollaborationInline(admin.TabularInline):
    model = OffreCollaboration
    extra = 1
    fields = ('type_collaboration', 'tarif_minimum', 'tarif_maximum', 'conditions')


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    """Admin for Influencer model"""
    list_display = ('user', 'pseudo', 'instagram_username', 'localisation', 
                    'disponibilite_collaboration', 'get_followers_total', 'created_at')
    list_filter = ('disponibilite_collaboration', 'localisation', 'created_at')
    search_fields = ('user__email', 'user__name', 'pseudo', 'instagram_username', 'biography')
    readonly_fields = ('created_at', 'updated_at', 'get_followers_total', 'get_engagement_moyen')
    filter_horizontal = ('selected_categories',)
    
    inlines = [ReseauSocialInline, InfluencerWorkInline, ImageInline, 
               InstagramReelInline, InstagramPostInline,
               PortfolioMediaInline, OffreCollaborationInline]
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Basic Information', {'fields': ('instagram_username', 'pseudo', 'biography', 
                                          'site_web', 'localisation')}),
        ('Instagram API Data', {'fields': ('instagram_data',)}),
        ('Categories & Interests', {'fields': ('selected_categories', 'langues', 
                                               'centres_interet', 'type_contenu')}),
        ('Collaboration', {'fields': ('disponibilite_collaboration',)}),
        ('Statistics', {'fields': ('get_followers_total', 'get_engagement_moyen')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_followers_total(self, obj):
        return f"{obj.followers_totaux:,}"
    get_followers_total.short_description = 'Total Followers'
    
    def get_engagement_moyen(self, obj):
        return f"{obj.engagement_moyen_global:.2f}%"
    get_engagement_moyen.short_description = 'Average Engagement'


@admin.register(ReseauSocial)
class ReseauSocialAdmin(admin.ModelAdmin):
    """Admin for ReseauSocial model"""
    list_display = ('influencer', 'plateforme', 'nombre_abonnes', 'taux_engagement', 
                    'frequence_publication', 'created_at')
    list_filter = ('plateforme', 'frequence_publication', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'url_profil')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Platform Details', {'fields': ('plateforme', 'url_profil', 'frequence_publication')}),
        ('Statistics', {'fields': ('nombre_abonnes', 'taux_engagement', 'moyenne_vues',
                                   'moyenne_likes', 'moyenne_commentaires')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(InfluencerWork)
class InfluencerWorkAdmin(admin.ModelAdmin):
    """Admin for InfluencerWork model"""
    list_display = ('influencer', 'brand_name', 'campaign', 'period', 'created_at')
    list_filter = ('period', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'brand_name', 'campaign')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Campaign Details', {'fields': ('brand_name', 'campaign', 'period')}),
        ('Results', {'fields': ('results', 'publication_link')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Admin for generic Image model"""
    list_display = ('id', 'get_related_object', 'url', 'is_default', 'is_public', 'created_at')
    list_filter = ('is_default', 'is_public', 'content_type', 'created_at')
    search_fields = ('url',)
    readonly_fields = ('created_at', 'content_type', 'object_id')
    
    fieldsets = (
        ('Related Object', {'fields': ('content_type', 'object_id')}),
        ('Image Details', {'fields': ('url', 'is_default', 'is_public')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_related_object(self, obj):
        return str(obj.content_object)
    get_related_object.short_description = 'Related To'


@admin.register(InstagramReel)
class InstagramReelAdmin(admin.ModelAdmin):
    """Admin for Instagram Reel"""
    list_display = ('influencer', 'post_name', 'username', 'likes', 'comments', 'views', 'taken_at')
    list_filter = ('taken_at', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'post_name', 'username', 'instagram_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Instagram Data', {'fields': ('instagram_id', 'code', 'video_url', 'thumbnail_url', 'username')}),
        ('Content', {'fields': ('post_name', 'duration', 'hashtags')}),
        ('Engagement', {'fields': ('likes', 'comments', 'views', 'taken_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    """Admin for Instagram Post"""
    list_display = ('influencer', 'post_name', 'media_type', 'username', 'likes', 'comments', 'taken_at')
    list_filter = ('media_type', 'taken_at', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'post_name', 'username', 'instagram_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Instagram Data', {'fields': ('instagram_id', 'code', 'media_type', 'image_url', 'thumbnail_url', 'username')}),
        ('Content', {'fields': ('post_name', 'carousel_media', 'hashtags')}),
        ('Engagement', {'fields': ('likes', 'comments', 'taken_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PortfolioMedia)
class PortfolioMediaAdmin(admin.ModelAdmin):
    """Admin for PortfolioMedia model"""
    list_display = ('influencer', 'titre', 'date_creation', 'created_at')
    list_filter = ('date_creation', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'titre', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Media Details', {'fields': ('titre', 'image_url', 'description', 'date_creation')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(OffreCollaboration)
class OffreCollaborationAdmin(admin.ModelAdmin):
    """Admin for OffreCollaboration model"""
    list_display = ('influencer', 'type_collaboration', 'tarif_minimum', 
                    'tarif_maximum', 'created_at')
    list_filter = ('type_collaboration', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo', 'type_collaboration')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Offer Details', {'fields': ('type_collaboration', 'tarif_minimum', 
                                      'tarif_maximum', 'conditions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(StatistiquesGlobales)
class StatistiquesGlobalesAdmin(admin.ModelAdmin):
    """Admin for StatistiquesGlobales model"""
    list_display = ('influencer', 'mois', 'followers_totaux', 
                    'engagement_moyen_global', 'croissance_mensuelle', 'created_at')
    list_filter = ('mois', 'created_at')
    search_fields = ('influencer__user__name', 'influencer__pseudo')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Influencer', {'fields': ('influencer',)}),
        ('Period', {'fields': ('mois',)}),
        ('Statistics', {'fields': ('followers_totaux', 'engagement_moyen_global', 
                                   'croissance_mensuelle')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )


# Company Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin for Address model"""
    list_display = ('id', 'address', 'city', 'state', 'country', 'postal_code', 'created_at')
    list_filter = ('country', 'state', 'created_at')
    search_fields = ('address', 'city', 'state', 'country', 'postal_code')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Address Information', {'fields': ('address', 'city', 'state', 'postal_code', 'country')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company model"""
    list_display = ('company_name', 'user', 'matricule', 'size', 'domain_activity', 
                    'disponibilite_collaboration', 'created_at')
    list_filter = ('size', 'domain_activity', 'entreprise_type', 
                   'disponibilite_collaboration', 'created_at')
    search_fields = ('company_name', 'matricule', 'user__email', 'user__name', 
                     'description', 'contact_email')
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [ImageInline]
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Company Information', {'fields': ('company_name', 'matricule', 'website', 
                                             'size', 'entreprise_type')}),
        ('Business Details', {'fields': ('domain_activity', 'description', 
                                         'contact_email', 'langues')}),
        ('Address', {'fields': ('address',)}),
        ('Collaboration', {'fields': ('disponibilite_collaboration',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make address field show related addresses
        if 'address' in form.base_fields:
            form.base_fields['address'].queryset = Address.objects.all()
        return form


@admin.register(NotificationPreferences)
class NotificationPreferencesAdmin(admin.ModelAdmin):
    """Admin for Notification Preferences"""
    list_display = (
        'user', 'email_notifications', 'new_applications', 
        'messages', 'campaign_updates', 'weekly_report', 'updated_at'
    )
    list_filter = ('email_notifications', 'new_applications', 'messages', 'updated_at')
    search_fields = ('user__email', 'user__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': ('email_notifications', 'new_applications', 'messages', 
                      'campaign_updates', 'weekly_report')
        }),
        ('App Notifications', {
            'fields': ('push_notifications',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PrivacySettings)
class PrivacySettingsAdmin(admin.ModelAdmin):
    """Admin for Privacy Settings"""
    list_display = (
        'user', 'profile_visibility', 'show_email', 
        'show_phone', 'searchable', 'updated_at'
    )
    list_filter = ('profile_visibility', 'show_email', 'show_phone', 'searchable')
    search_fields = ('user__email', 'user__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Visibility', {
            'fields': ('profile_visibility', 'show_email', 'show_phone')
        }),
        ('Search & Discovery', {
            'fields': ('searchable',)
        }),
        ('Data & Analytics', {
            'fields': ('allow_analytics',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

