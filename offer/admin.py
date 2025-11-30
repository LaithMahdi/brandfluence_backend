from django.contrib import admin
from django.utils.html import format_html
from .models import Offer, OfferApplication, ApplicationStatus


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin interface for Offer model"""
    
    list_display = ['title', 'budget_range', 'influencer_number', 'date_range', 'created_by', 'applications_count', 'created_at']
    list_filter = ['start_date', 'end_date', 'created_at', 'created_by']
    search_fields = ['title', 'objectif', 'requirement', 'created_by__username']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25
    readonly_fields = ['created_at', 'applications_count']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ('title', 'created_by')
        }),
        ('Budget & Requirements', {
            'fields': ('min_budget', 'max_budget', 'influencer_number')
        }),
        ('Details', {
            'fields': ('objectif', 'requirement')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    ]
    
    def budget_range(self, obj):
        """Display budget range in formatted way"""
        return format_html(
            '<span style="color: #0066cc;">${} - ${}</span>',
            f'{obj.min_budget:,.2f}',
            f'{obj.max_budget:,.2f}'
        )
    budget_range.short_description = 'Budget Range'
    budget_range.admin_order_field = 'min_budget'
    
    def date_range(self, obj):
        """Display date range"""
        return format_html(
            '{} → {}',
            obj.start_date.strftime('%Y-%m-%d'),
            obj.end_date.strftime('%Y-%m-%d')
        )
    date_range.short_description = 'Campaign Period'
    date_range.admin_order_field = 'start_date'
    
    def applications_count(self, obj):
        """Show number of applications"""
        count = obj.applications.count()
        color = 'green' if count > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} applications</span>',
            color,
            count
        )
    applications_count.short_description = 'Applications'


@admin.register(OfferApplication)
class OfferApplicationAdmin(admin.ModelAdmin):
    """Admin interface for OfferApplication model"""
    
    list_display = ['offer', 'user', 'asking_price_formatted', 'status_badge', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'offer']
    search_fields = ['offer__title', 'user__username', 'proposal']
    ordering = ['-submitted_at']
    list_editable = ['status']
    list_per_page = 25
    readonly_fields = ['submitted_at']
    
    fieldsets = [
        ('Application Details', {
            'fields': ('offer', 'user', 'asking_price')
        }),
        ('Proposal', {
            'fields': ('proposal',)
        }),
        ('Status', {
            'fields': ('status', 'submitted_at')
        }),
    ]
    
    actions = ['approve_applications', 'reject_applications', 'set_pending']
    
    def asking_price_formatted(self, obj):
        """Display asking price formatted"""
        return format_html(
            '<span style="color: #0066cc; font-weight: bold;">${}</span>',
            f'{obj.asking_price:,.2f}'
        )
    asking_price_formatted.short_description = 'Asking Price'
    asking_price_formatted.admin_order_field = 'asking_price'
    
    def status_badge(self, obj):
        """Show colored status badge"""
        colors = {
            ApplicationStatus.PENDING: '#ff9800',
            ApplicationStatus.APPROVED: '#4caf50',
            ApplicationStatus.REJECTED: '#f44336',
            ApplicationStatus.WITHDRAW: '#9e9e9e',
        }
        icons = {
            ApplicationStatus.PENDING: '⏳',
            ApplicationStatus.APPROVED: '✓',
            ApplicationStatus.REJECTED: '✗',
            ApplicationStatus.WITHDRAW: '↩',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            colors.get(obj.status, '#000'),
            icons.get(obj.status, ''),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def approve_applications(self, request, queryset):
        """Approve selected applications"""
        updated = queryset.update(status=ApplicationStatus.APPROVED)
        self.message_user(request, f'{updated} applications approved.')
    approve_applications.short_description = "✓ Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """Reject selected applications"""
        updated = queryset.update(status=ApplicationStatus.REJECTED)
        self.message_user(request, f'{updated} applications rejected.')
    reject_applications.short_description = "✗ Reject selected applications"
    
    def set_pending(self, request, queryset):
        """Set selected applications to pending"""
        updated = queryset.update(status=ApplicationStatus.PENDING)
        self.message_user(request, f'{updated} applications set to pending.')
    set_pending.short_description = "⏳ Set to pending"
