from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'leads', views.LeadViewSet)
# router.register(r'activities', views.LeadActivityViewSet)
# router.register(r'cold-calls', views.ColdCallLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('import/', views.ImportLeadsView.as_view(), name='import-leads'),
    # path('export/', views.ExportLeadsView.as_view(), name='export-leads'),
]