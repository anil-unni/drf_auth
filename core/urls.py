
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # accounts-related endpoints
    path("accounts/", include("accounts.urls")),
    path("ai/", include("ai_module.urls")),
    
    # Schema and documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
