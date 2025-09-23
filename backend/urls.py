"""
URL configuration for Ekavarta AI Business Automation Platform.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/', views.api_overview, name='api-overview'),
    path('api/categories/', views.service_categories_api, name='service-categories'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/services/', include('apps.services.urls')),
    path('api/leads/', include('apps.leads.urls')),
    path('api/ai/', include('apps.ai_automation.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
