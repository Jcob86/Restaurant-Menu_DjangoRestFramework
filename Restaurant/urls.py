from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = 'Restaurant Admin'
admin.site.index_title = 'Admin'

schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="Documentation of Restaurant App",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/schema', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]
