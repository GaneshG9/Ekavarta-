from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import ServiceCategory, Service, ServiceInquiry, ServiceQuote
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer, 
    ServiceInquirySerializer, ServiceQuoteSerializer
)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Service categories (Real Estate, Solar, Digital Marketing)
    """
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [AllowAny]


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Services offered by Ekavarta
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured services"""
        featured_services = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_services, many=True)
        return Response(serializer.data)


class ServiceInquiryViewSet(viewsets.ModelViewSet):
    """
    Service inquiries from customers
    """
    serializer_class = ServiceInquirySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type in ['admin', 'manager']:
            return ServiceInquiry.objects.all()
        return ServiceInquiry.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class ServiceQuoteViewSet(viewsets.ModelViewSet):
    """
    Service quotes for inquiries
    """
    serializer_class = ServiceQuoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type in ['admin', 'manager']:
            return ServiceQuote.objects.all()
        return ServiceQuote.objects.filter(inquiry__customer=self.request.user)
