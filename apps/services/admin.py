from django.contrib import admin
from .models import ServiceCategory, Service, ServiceInquiry, ServiceQuote


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'service_type', 'pricing_model', 'base_price', 'is_active', 'is_featured')
    list_filter = ('category', 'service_type', 'pricing_model', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ()


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer', 'contact_name', 'contact_email', 'status', 'priority', 'ai_score', 'created_at')
    list_filter = ('status', 'priority', 'service__category', 'ai_analyzed', 'created_at')
    search_fields = ('contact_name', 'contact_email', 'contact_phone', 'subject')
    readonly_fields = ('ai_score', 'ai_insights')


@admin.register(ServiceQuote)
class ServiceQuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_number', 'inquiry', 'total_amount', 'currency', 'status', 'ai_generated', 'created_at')
    list_filter = ('status', 'ai_generated', 'currency', 'created_at')
    search_fields = ('quote_number', 'inquiry__contact_name', 'inquiry__contact_email')
    readonly_fields = ('ai_generated', 'ai_confidence')
