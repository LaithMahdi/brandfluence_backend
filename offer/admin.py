from django.contrib import admin
from .models import Offer, OfferApplication, ApplicationStatus



@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_budget', 'max_budget', 'influencer_number', 'start_date', 'end_date', 'created_by')
    search_fields = ('title', 'objectif', 'requirement', 'created_by__username')
    list_filter = ('start_date', 'end_date', 'created_by')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    list_per_page = 20



@admin.register(OfferApplication)
class OfferApplicationAdmin(admin.ModelAdmin):
    list_display = ('offer', 'user', 'asking_price', 'status', 'submitted_at')
    search_fields = ('offer__title', 'user__username', 'proposal')
    list_filter = ('status', 'submitted_at')
    ordering = ('-submitted_at',)
    list_editable = ('status',) 
    list_per_page = 20
