from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AITask(models.Model):
    """
    Track AI-powered tasks and automations
    """
    TASK_TYPES = (
        ('content_generation', 'Content Generation'),
        ('lead_analysis', 'Lead Analysis'),
        ('cold_calling', 'Cold Calling'),
        ('social_posting', 'Social Media Posting'),
        ('ad_creation', 'Ad Creation'),
        ('report_generation', 'Report Generation'),
        ('customer_response', 'Customer Response'),
    )
    
    TASK_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    task_type = models.CharField(max_length=30, choices=TASK_TYPES)
    task_name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Task configuration
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict)
    ai_model_used = models.CharField(max_length=100, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='pending')
    progress_percentage = models.PositiveIntegerField(default=0)
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.task_type} - {self.task_name}"
    
    class Meta:
        db_table = 'ai_tasks'
        ordering = ['-created_at']


class SocialMediaContent(models.Model):
    """
    AI-generated social media content
    """
    CONTENT_TYPES = (
        ('post', 'Post'),
        ('story', 'Story'),
        ('reel', 'Reel'),
        ('video', 'Video'),
        ('carousel', 'Carousel'),
    )
    
    PLATFORMS = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
    )
    
    CONTENT_STATUS = (
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    )
    
    # Content details
    title = models.CharField(max_length=200)
    content = models.TextField()
    hashtags = models.TextField(blank=True)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    
    # Media files
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    media_files = models.JSONField(default=list)
    
    # AI generation details
    ai_prompt = models.TextField()
    ai_model_used = models.CharField(max_length=100)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Posting details
    status = models.CharField(max_length=20, choices=CONTENT_STATUS, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    post_id = models.CharField(max_length=100, blank=True)  # Platform post ID
    
    # Performance metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.platform} {self.content_type} - {self.title}"
    
    class Meta:
        db_table = 'social_media_content'
        ordering = ['-created_at']


class AIGeneratedAd(models.Model):
    """
    AI-generated advertisements for different platforms
    """
    AD_PLATFORMS = (
        ('google_ads', 'Google Ads'),
        ('facebook_ads', 'Facebook Ads'),
        ('instagram_ads', 'Instagram Ads'),
        ('linkedin_ads', 'LinkedIn Ads'),
        ('youtube_ads', 'YouTube Ads'),
    )
    
    AD_TYPES = (
        ('search', 'Search Ad'),
        ('display', 'Display Ad'),
        ('video', 'Video Ad'),
        ('shopping', 'Shopping Ad'),
        ('lead_gen', 'Lead Generation Ad'),
    )
    
    AD_STATUS = (
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('rejected', 'Rejected'),
    )
    
    # Ad details
    campaign_name = models.CharField(max_length=200)
    ad_name = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=AD_PLATFORMS)
    ad_type = models.CharField(max_length=20, choices=AD_TYPES)
    
    # Ad content
    headline = models.CharField(max_length=100)
    description = models.TextField()
    call_to_action = models.CharField(max_length=50)
    landing_page_url = models.URLField()
    
    # Creative assets
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    creative_assets = models.JSONField(default=list)
    
    # Targeting
    target_audience = models.JSONField(default=dict)
    keywords = models.JSONField(default=list)
    budget_daily = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # AI generation
    ai_prompt = models.TextField()
    ai_model_used = models.CharField(max_length=100)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Status and performance
    status = models.CharField(max_length=20, choices=AD_STATUS, default='draft')
    platform_ad_id = models.CharField(max_length=100, blank=True)
    
    # Performance metrics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ctr = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Click-through rate
    cpc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cost per click
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.platform} - {self.ad_name}"
    
    class Meta:
        db_table = 'ai_generated_ads'
        ordering = ['-created_at']


class AIInsight(models.Model):
    """
    AI-generated insights and recommendations
    """
    INSIGHT_TYPES = (
        ('lead_scoring', 'Lead Scoring'),
        ('performance_analysis', 'Performance Analysis'),
        ('trend_prediction', 'Trend Prediction'),
        ('optimization_recommendation', 'Optimization Recommendation'),
        ('market_analysis', 'Market Analysis'),
    )
    
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Data and analysis
    data_analyzed = models.JSONField(default=dict)
    insights = models.JSONField(default=dict)
    recommendations = models.JSONField(default=list)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    # AI model details
    ai_model_used = models.CharField(max_length=100)
    analysis_date = models.DateTimeField(auto_now_add=True)
    
    # Action items
    action_items = models.JSONField(default=list)
    priority_level = models.CharField(max_length=10, default='medium')
    
    # Implementation tracking
    implemented = models.BooleanField(default=False)
    implementation_date = models.DateTimeField(null=True, blank=True)
    implementation_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.insight_type} - {self.title}"
    
    class Meta:
        db_table = 'ai_insights'
        ordering = ['-created_at']


class AutomationWorkflow(models.Model):
    """
    Automation workflows and n8n integrations
    """
    WORKFLOW_STATUS = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('error', 'Error'),
        ('disabled', 'Disabled'),
    )
    
    TRIGGER_TYPES = (
        ('schedule', 'Schedule'),
        ('webhook', 'Webhook'),
        ('event', 'Event'),
        ('manual', 'Manual'),
    )
    
    # Workflow details
    name = models.CharField(max_length=200)
    description = models.TextField()
    workflow_type = models.CharField(max_length=50)
    
    # Configuration
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    trigger_config = models.JSONField(default=dict)
    workflow_config = models.JSONField(default=dict)
    
    # n8n integration
    n8n_workflow_id = models.CharField(max_length=100, blank=True)
    n8n_webhook_url = models.URLField(blank=True, null=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=WORKFLOW_STATUS, default='active')
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Performance
    execution_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'automation_workflows'
        ordering = ['-created_at']
