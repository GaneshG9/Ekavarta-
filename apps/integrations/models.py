from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class WhatsAppIntegration(models.Model):
    """
    WhatsApp Business API integration
    """
    MESSAGE_STATUS = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    )
    
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('template', 'Template'),
        ('interactive', 'Interactive'),
    )
    
    # User/Lead information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='whatsapp_messages')
    phone_number = models.CharField(max_length=15)
    contact_name = models.CharField(max_length=100, blank=True)
    
    # Message details
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    message_content = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    template_name = models.CharField(max_length=100, blank=True)
    template_parameters = models.JSONField(default=list)
    
    # WhatsApp API details
    whatsapp_message_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS, default='sent')
    
    # AI generation
    ai_generated = models.BooleanField(default=False)
    ai_prompt = models.TextField(blank=True)
    
    # Tracking
    is_inbound = models.BooleanField(default=False)  # True if received from user
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Response tracking
    requires_response = models.BooleanField(default=False)
    response_received = models.BooleanField(default=False)
    response_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"WhatsApp to {self.phone_number} - {self.message_type}"
    
    class Meta:
        db_table = 'whatsapp_integration'
        ordering = ['-sent_at']


class TelegramIntegration(models.Model):
    """
    Telegram Bot integration
    """
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('document', 'Document'),
        ('voice', 'Voice'),
        ('video', 'Video'),
        ('sticker', 'Sticker'),
    )
    
    # User information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='telegram_messages')
    telegram_user_id = models.CharField(max_length=50)
    telegram_username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    
    # Message details
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    message_content = models.TextField()
    media_file_id = models.CharField(max_length=200, blank=True)
    
    # Telegram API details
    telegram_message_id = models.CharField(max_length=50)
    chat_id = models.CharField(max_length=50)
    
    # AI processing
    ai_generated = models.BooleanField(default=False)
    ai_response = models.TextField(blank=True)
    
    # Tracking
    is_inbound = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Bot commands
    is_command = models.BooleanField(default=False)
    command_name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Telegram from {self.telegram_username or self.telegram_user_id}"
    
    class Meta:
        db_table = 'telegram_integration'
        ordering = ['-created_at']


class SocialMediaAccount(models.Model):
    """
    Social media accounts for posting automation
    """
    PLATFORMS = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
    )
    
    ACCOUNT_STATUS = (
        ('active', 'Active'),
        ('expired', 'Token Expired'),
        ('error', 'Error'),
        ('disabled', 'Disabled'),
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    account_name = models.CharField(max_length=100)
    account_id = models.CharField(max_length=100)
    
    # Authentication
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Account details
    profile_picture_url = models.URLField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    
    # Configuration
    auto_posting_enabled = models.BooleanField(default=True)
    posting_schedule = models.JSONField(default=dict)  # Times and days for posting
    
    # Status
    status = models.CharField(max_length=20, choices=ACCOUNT_STATUS, default='active')
    last_posted = models.DateTimeField(null=True, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
    # Performance tracking
    total_posts = models.PositiveIntegerField(default=0)
    total_engagement = models.PositiveIntegerField(default=0)
    average_engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.platform} - {self.account_name}"
    
    class Meta:
        db_table = 'social_media_accounts'
        unique_together = ['platform', 'account_id']


class ThirdPartyIntegration(models.Model):
    """
    Third-party integrations and API connections
    """
    INTEGRATION_TYPES = (
        ('n8n', 'n8n Workflow'),
        ('zapier', 'Zapier'),
        ('crm', 'CRM System'),
        ('email_marketing', 'Email Marketing'),
        ('analytics', 'Analytics'),
        ('payment', 'Payment Gateway'),
        ('storage', 'Cloud Storage'),
    )
    
    INTEGRATION_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('expired', 'Expired'),
    )
    
    # Integration details
    integration_type = models.CharField(max_length=30, choices=INTEGRATION_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # API configuration
    api_endpoint = models.URLField()
    api_key = models.TextField()
    webhook_url = models.URLField(blank=True, null=True)
    
    # Configuration
    configuration = models.JSONField(default=dict)
    mapping_rules = models.JSONField(default=dict)  # Data mapping rules
    
    # Status and monitoring
    status = models.CharField(max_length=20, choices=INTEGRATION_STATUS, default='active')
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_frequency_minutes = models.PositiveIntegerField(default=60)
    
    # Performance tracking
    total_requests = models.PositiveIntegerField(default=0)
    successful_requests = models.PositiveIntegerField(default=0)
    failed_requests = models.PositiveIntegerField(default=0)
    last_error_message = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.integration_type} - {self.name}"
    
    class Meta:
        db_table = 'third_party_integrations'


class APILog(models.Model):
    """
    Log all API requests and responses for monitoring
    """
    REQUEST_METHODS = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    )
    
    # Request details
    integration = models.ForeignKey(ThirdPartyIntegration, on_delete=models.CASCADE, related_name='api_logs')
    request_method = models.CharField(max_length=10, choices=REQUEST_METHODS)
    endpoint = models.URLField()
    
    # Request/Response data
    request_headers = models.JSONField(default=dict)
    request_body = models.TextField(blank=True)
    response_status_code = models.PositiveIntegerField()
    response_headers = models.JSONField(default=dict)
    response_body = models.TextField(blank=True)
    
    # Performance
    response_time_ms = models.PositiveIntegerField()
    
    # Error tracking
    is_error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    # User tracking
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.request_method} {self.endpoint} - {self.response_status_code}"
    
    class Meta:
        db_table = 'api_logs'
        ordering = ['-created_at']


class NotificationChannel(models.Model):
    """
    Configure notification channels for different events
    """
    CHANNEL_TYPES = (
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('sms', 'SMS'),
        ('webhook', 'Webhook'),
    )
    
    EVENT_TYPES = (
        ('new_lead', 'New Lead'),
        ('lead_status_change', 'Lead Status Change'),
        ('task_completion', 'Task Completion'),
        ('system_error', 'System Error'),
        ('daily_report', 'Daily Report'),
        ('weekly_report', 'Weekly Report'),
    )
    
    # Channel configuration
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    
    # Recipients
    recipients = models.JSONField(default=list)  # List of emails, phone numbers, etc.
    
    # Message template
    message_template = models.TextField()
    subject_template = models.CharField(max_length=200, blank=True)
    
    # Scheduling
    is_active = models.BooleanField(default=True)
    send_immediately = models.BooleanField(default=True)
    scheduled_time = models.TimeField(null=True, blank=True)  # For daily reports
    
    # AI enhancement
    ai_personalization = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.channel_type} - {self.event_type}"
    
    class Meta:
        db_table = 'notification_channels'
        unique_together = ['channel_type', 'event_type']
