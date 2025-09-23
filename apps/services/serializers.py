from rest_framework import serializers
from .models import ServiceCategory, Service, ServiceInquiry, ServiceQuote


class ServiceCategorySerializer(serializers.ModelSerializer):
    services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'services_count', 'display_order']
    
    def get_services_count(self, obj):
        return obj.services.filter(is_active=True).count()


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'category_name', 'short_description', 
                 'detailed_description', 'service_type', 'pricing_model', 'base_price', 
                 'currency', 'features', 'requirements', 'deliverables', 'thumbnail', 
                 'is_featured']


class ServiceInquirySerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = ServiceInquiry
        fields = ['id', 'service', 'service_name', 'customer_name', 'subject', 'message', 
                 'budget_range', 'timeline', 'contact_name', 'contact_email', 'contact_phone', 
                 'preferred_contact_method', 'status', 'priority', 'ai_score', 'created_at']
        read_only_fields = ['customer_name', 'ai_score', 'created_at']


class ServiceQuoteSerializer(serializers.ModelSerializer):
    inquiry_subject = serializers.CharField(source='inquiry.subject', read_only=True)
    customer_name = serializers.CharField(source='inquiry.customer.get_full_name', read_only=True)
    
    class Meta:
        model = ServiceQuote
        fields = ['id', 'quote_number', 'inquiry', 'inquiry_subject', 'customer_name',
                 'line_items', 'subtotal', 'tax_amount', 'discount_amount', 'total_amount',
                 'currency', 'terms_and_conditions', 'valid_until', 'payment_terms',
                 'status', 'ai_generated', 'created_at', 'sent_at']
        read_only_fields = ['quote_number', 'ai_generated', 'created_at']