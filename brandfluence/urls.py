from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from schema_graph.views import Schema
from django.http import JsonResponse
from .schema import schema

admin.site.site_header = "BrandFluence Admin"
admin.site.site_title = "BrandFluence Admin Portal"
admin.site.index_title = "Welcome to BrandFluence Admin Portal"

def health_check(request):
    """Simple health check endpoint"""
    import django
    return JsonResponse({
        'status': 'ok',
        'django_version': django.get_version(),
        'message': 'BrandFluence API is running'
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]