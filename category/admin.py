"""
Django admin configuration for Category app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    
    Provides a comprehensive admin interface with search, filtering,
    and custom display options.
    """
    
    # List display configuration
    list_display = [
        'name',
        'description_truncated',
        'is_active_display',
        'created_display',
        'modified_display',
        'actions_column',
    ]
    
    # List filtering options
    list_filter = [
        'is_active',
        'created',
        'modified',
    ]
    
    # Search functionality
    search_fields = [
        'name',
        'description',
    ]
    
    # Ordering
    ordering = ['-created']
    
    # Fields configuration for add/edit forms
    fields = [
        'name',
        'description',
        'is_active',
    ]
    
    # Read-only fields in edit mode
    readonly_fields = [
        'created',
        'modified',
    ]
    
    # Pagination
    list_per_page = 25
    list_max_show_all = 100
    
    # Actions
    actions = [
        'make_active',
        'make_inactive',
    ]
    
    def get_readonly_fields(self, request, obj=None):
        """
        Return read-only fields based on whether we're adding or editing.
        """
        if obj:  # Editing an existing object
            return self.readonly_fields + ['created', 'modified']
        return []
    
    def get_fieldsets(self, request, obj=None):
        """
        Return fieldsets for the admin form.
        """
        fieldsets = [
            ('Basic Information', {
                'fields': ('name', 'description', 'is_active'),
                'description': 'Basic category information'
            }),
        ]
        
        if obj:  # Editing an existing object
            fieldsets.append(
                ('Timestamps', {
                    'fields': ('created', 'modified'),
                    'classes': ('collapse',),
                    'description': 'Automatically managed timestamps'
                })
            )
        
        return fieldsets
    
    # Custom display methods
    def description_truncated(self, obj):
        """Display truncated description."""
        if obj.description:
            return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description
        return '-'
    description_truncated.short_description = 'Description'
    
    def is_active_display(self, obj):
        """Display active status with color coding."""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Active</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Inactive</span>'
        )
    is_active_display.short_description = 'Status'
    is_active_display.admin_order_field = 'is_active'
    
    def created_display(self, obj):
        """Display formatted creation date."""
        return obj.created.strftime('%Y-%m-%d %H:%M')
    created_display.short_description = 'Created'
    created_display.admin_order_field = 'created'
    
    def modified_display(self, obj):
        """Display formatted modification date."""
        return obj.modified.strftime('%Y-%m-%d %H:%M')
    modified_display.short_description = 'Modified'
    modified_display.admin_order_field = 'modified'
    
    def actions_column(self, obj):
        """Display action buttons."""
        edit_url = reverse('admin:category_category_change', args=[obj.pk])
        delete_url = reverse('admin:category_category_delete', args=[obj.pk])
        
        return format_html(
            '<a href="{}" class="button" style="margin-right: 5px;">Edit</a>'
            '<a href="{}" class="button" style="background-color: #dc3545; color: white;">Delete</a>',
            edit_url,
            delete_url
        )
    actions_column.short_description = 'Actions'
    
    # Custom actions
    def make_active(self, request, queryset):
        """Mark selected categories as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} categories were successfully marked as active.'
        )
    make_active.short_description = "Mark selected categories as active"
    
    def make_inactive(self, request, queryset):
        """Mark selected categories as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} categories were successfully marked as inactive.'
        )
    make_inactive.short_description = "Mark selected categories as inactive"
    
    def get_queryset(self, request):
        """
        Optimize queryset for admin list view.
        """
        qs = super().get_queryset(request)
        # Add any additional optimizations here
        return qs
    
    class Media:
        """
        Additional CSS and JavaScript for the admin interface.
        """
        css = {
            'all': ['admin/css/custom_category_admin.css']  # Add custom CSS if needed
        }
        js = ['admin/js/custom_category_admin.js']  # Add custom JS if needed


# Optional: Register additional admin configurations
admin.site.site_header = "Brandfluence Administration"
admin.site.site_title = "Brandfluence Admin Portal"
admin.site.index_title = "Welcome to Brandfluence Administration"