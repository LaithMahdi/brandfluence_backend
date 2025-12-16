from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from schema_graph.views import Schema
from django.shortcuts import render
from .schema import schema
from django.urls import path, include 
admin.site.site_header = "BrandFluence Admin"
admin.site.site_title = "BrandFluence Admin Portal"
admin.site.index_title = "Welcome to BrandFluence Admin Portal"

def home(request):
    """Home page with API information"""
    import django
    return render(request, 'home.html', {
        'django_version': django.get_version(),
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('api/', include('api.urls')), 
  
]