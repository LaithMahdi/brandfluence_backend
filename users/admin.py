from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User, UserRole, VerifyToken


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
