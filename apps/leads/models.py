from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LeadSource(models.Model):
    """
    Sources from where leads are generated
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    source_type = models.CharField(max_length=50)  # 'website', 'social', 'referral', 'cold_call', etc.
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'lead_sources'


class Lead(models.Model):
    """
    Main lead model for tracking potential customers
    """
    LEAD_STATUS = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('on_hold', 'On Hold'),
    )
    
    LEAD_QUALITY = (
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('cold', 'Cold'),
    )
    
    LEAD_TYPES = (
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    )
    
    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Lead details
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPES, default='individual')
    lead_quality = models.CharField(max_length=10, choices=LEAD_QUALITY, default='warm')
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, related_name='leads')
    
    # Interest and requirements
    interested_services = models.JSONField(default=list)
    budget_range = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    
    # Assignment and tracking
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_leads')
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    
    # AI Analysis
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ai_insights = models.JSONField(default=dict)
    predicted_conversion_probability = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Tracking fields
    last_contacted = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.full_name} ({self.company_name or 'Individual'})"
    
    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']


class LeadActivity(models.Model):
    """
    Track all activities related to leads
    """
    ACTIVITY_TYPES = (
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('proposal', 'Proposal Sent'),
        ('follow_up', 'Follow Up'),
        ('status_change', 'Status Change'),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    
    # Communication details
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)  # For calls
    outcome = models.CharField(max_length=100, blank=True)
    next_action = models.CharField(max_length=200, blank=True)
    
    # AI generated content
    ai_generated = models.BooleanField(default=False)
    ai_sentiment = models.CharField(max_length=20, blank=True)  # positive, negative, neutral
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.activity_type} - {self.lead.full_name}"
    
    class Meta:
        db_table = 'lead_activities'
        ordering = ['-created_at']


class LeadCommunication(models.Model):
    """
    Store communication templates and logs
    """
    COMMUNICATION_TYPES = (
        ('cold_call_script', 'Cold Call Script'),
        ('email_template', 'Email Template'),
        ('whatsapp_template', 'WhatsApp Template'),
        ('follow_up_template', 'Follow Up Template'),
    )
    
    LANGUAGES = (
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('both', 'Both'),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='communications')
    communication_type = models.CharField(max_length=30, choices=COMMUNICATION_TYPES)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='en')
    
    # Content
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    personalized_content = models.TextField(blank=True)  # AI personalized version
    
    # Delivery tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    response_received = models.BooleanField(default=False)
    
    # AI generation
    ai_generated = models.BooleanField(default=False)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.communication_type} for {self.lead.full_name}"
    
    class Meta:
        db_table = 'lead_communications'
        ordering = ['-created_at']


class ColdCallLog(models.Model):
    """
    Detailed logs for AI-powered cold calls
    """
    CALL_STATUS = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('no_answer', 'No Answer'),
        ('busy', 'Busy'),
        ('voicemail', 'Voicemail'),
    )
    
    CALL_OUTCOMES = (
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('callback_requested', 'Callback Requested'),
        ('information_requested', 'Information Requested'),
        ('meeting_scheduled', 'Meeting Scheduled'),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='cold_calls')
    
    # Call details
    phone_number = models.CharField(max_length=15)
    language = models.CharField(max_length=10, default='en')
    script_used = models.TextField()
    
    # Call tracking
    scheduled_at = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Call status and outcome
    status = models.CharField(max_length=20, choices=CALL_STATUS, default='scheduled')
    outcome = models.CharField(max_length=30, choices=CALL_OUTCOMES, blank=True)
    
    # AI analysis
    conversation_transcript = models.TextField(blank=True)
    ai_sentiment_analysis = models.JSONField(default=dict)
    ai_next_action = models.CharField(max_length=200, blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cold call to {self.lead.full_name} at {self.scheduled_at}"
    
    class Meta:
        db_table = 'cold_call_logs'
        ordering = ['-scheduled_at']
