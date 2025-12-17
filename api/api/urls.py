
from django.urls import path
from . import views

urlpatterns = [
   
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('countries/', views.CountriesView.as_view(), name='countries'),
    
    
    path('recommend/', views.RecommendView.as_view(), name='recommend'),
    
    
    path('search/', views.SearchView.as_view(), name='search'),
    
    
    path('influencer/<int:influencer_id>/', views.InfluencerDetailView.as_view(), name='influencer-detail'),
]