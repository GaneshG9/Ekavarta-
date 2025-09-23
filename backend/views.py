from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from apps.services.models import ServiceCategory, Service


def home(request):
    """
    Main landing page
    """
    return render(request, 'index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """
    API overview endpoint
    """
    return JsonResponse({
        'message': 'Welcome to Ekavarta AI Business Automation Platform',
        'version': '1.0.0',
        'endpoints': {
            'authentication': '/api/auth/',
            'services': '/api/services/',
            'leads': '/api/leads/',
            'ai_automation': '/api/ai/',
            'dashboard': '/api/dashboard/',
            'integrations': '/api/integrations/',
        },
        'features': [
            'AI-Powered Lead Management',
            'Cold Calling Automation in Hindi & English',
            'Social Media Content Generation',
            'WhatsApp & Telegram Integration',
            'Automated Reporting & Analytics',
            'Multi-Service Platform (Real Estate, Solar, Digital Marketing)'
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def service_categories_api(request):
    """
    Get service categories for the frontend
    """
    categories = ServiceCategory.objects.filter(is_active=True).order_by('display_order')
    data = []
    for category in categories:
        services_count = category.services.filter(is_active=True).count()
        data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'services_count': services_count,
            'display_order': category.display_order
        })
    
    return JsonResponse({
        'categories': data,
        'total_count': len(data)
    })