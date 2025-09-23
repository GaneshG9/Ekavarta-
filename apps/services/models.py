from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ServiceCategory(models.Model):
    """
    Categories for different services (Real Estate, Solar, Digital Marketing)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='service_icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'service_categories'
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['display_order', 'name']


class Service(models.Model):
    """
    Individual services offered by Ekavarta
    """
    SERVICE_TYPES = (
        ('consultation', 'Consultation'),
        ('implementation', 'Implementation'),
        ('maintenance', 'Maintenance'),
        ('training', 'Training'),
    )
    
    PRICING_MODELS = (
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly Rate'),
        ('monthly', 'Monthly Subscription'),
        ('custom', 'Custom Quote'),
    )
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300)
    detailed_description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    
    # Pricing
    pricing_model = models.CharField(max_length=20, choices=PRICING_MODELS)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='INR')
    
    # Features and requirements
    features = models.JSONField(default=list)
    requirements = models.JSONField(default=list)
    deliverables = models.JSONField(default=list)
    
    # Media
    thumbnail = models.ImageField(upload_to='service_thumbnails/', blank=True, null=True)
    gallery = models.JSONField(default=list)  # Store image URLs
    
    # SEO and metadata
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        db_table = 'services'
        ordering = ['category', 'display_order', 'name']


class ServiceInquiry(models.Model):
    """
    Customer inquiries for services
    """
    INQUIRY_STATUS = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('quoted', 'Quoted'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    )
    
    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='inquiries')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_inquiries')
    
    # Inquiry details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget_range = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    
    # Contact information
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    preferred_contact_method = models.CharField(max_length=20, default='email')
    
    # Status tracking
    status = models.CharField(max_length=20, choices=INQUIRY_STATUS, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_inquiries')
    
    # AI processing
    ai_analyzed = models.BooleanField(default=False)
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ai_insights = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service.name} inquiry from {self.contact_name}"
    
    class Meta:
        db_table = 'service_inquiries'
        verbose_name = 'Service Inquiry'
        verbose_name_plural = 'Service Inquiries'
        ordering = ['-created_at']


class ServiceQuote(models.Model):
    """
    Quotes generated for service inquiries
    """
    QUOTE_STATUS = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )
    
    inquiry = models.ForeignKey(ServiceInquiry, on_delete=models.CASCADE, related_name='quotes')
    quote_number = models.CharField(max_length=50, unique=True)
    
    # Quote details
    line_items = models.JSONField(default=list)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    
    # Terms and conditions
    terms_and_conditions = models.TextField()
    valid_until = models.DateTimeField()
    payment_terms = models.CharField(max_length=200)
    
    # Status
    status = models.CharField(max_length=20, choices=QUOTE_STATUS, default='draft')
    
    # AI generated
    ai_generated = models.BooleanField(default=False)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Quote {self.quote_number} for {self.inquiry}"
    
    class Meta:
        db_table = 'service_quotes'
        ordering = ['-created_at']
