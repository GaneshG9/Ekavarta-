from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'categories', views.ServiceCategoryViewSet)
# router.register(r'services', views.ServiceViewSet)
# router.register(r'inquiries', views.ServiceInquiryViewSet)
# router.register(r'quotes', views.ServiceQuoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]