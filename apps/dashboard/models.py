from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class BusinessMetric(models.Model):
    """
    Track key business metrics and KPIs
    """
    METRIC_TYPES = (
        ('leads', 'Leads'),
        ('conversions', 'Conversions'),
        ('revenue', 'Revenue'),
        ('social_engagement', 'Social Engagement'),
        ('website_traffic', 'Website Traffic'),
        ('ad_performance', 'Ad Performance'),
        ('customer_satisfaction', 'Customer Satisfaction'),
    )
    
    MEASUREMENT_PERIODS = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    )
    
    # Metric details
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    metric_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Value and tracking
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Time period
    measurement_period = models.CharField(max_length=20, choices=MEASUREMENT_PERIODS)
    measurement_date = models.DateField()
    
    # Calculation details
    calculation_method = models.TextField(blank=True)
    data_sources = models.JSONField(default=list)
    
    # Performance indicators
    percentage_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_improving = models.BooleanField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.metric_name} - {self.measurement_date}"
    
    class Meta:
        db_table = 'business_metrics'
        unique_together = ['metric_type', 'metric_name', 'measurement_date']
        ordering = ['-measurement_date']


class DashboardWidget(models.Model):
    """
    Configurable dashboard widgets
    """
    WIDGET_TYPES = (
        ('metric_card', 'Metric Card'),
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('graph', 'Graph'),
        ('map', 'Map'),
        ('list', 'List'),
        ('calendar', 'Calendar'),
    )
    
    CHART_TYPES = (
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
    )
    
    # Widget configuration
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, blank=True)
    
    # Data configuration
    data_source = models.CharField(max_length=100)  # Model or API endpoint
    data_filters = models.JSONField(default=dict)
    refresh_interval_minutes = models.PositiveIntegerField(default=30)
    
    # Layout and positioning
    position_x = models.PositiveIntegerField(default=0)
    position_y = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=4)
    height = models.PositiveIntegerField(default=3)
    
    # Styling
    color_scheme = models.CharField(max_length=50, default='default')
    custom_styling = models.JSONField(default=dict)
    
    # Visibility and permissions
    is_visible = models.BooleanField(default=True)
    is_shared = models.BooleanField(default=False)
    
    # Performance
    last_updated = models.DateTimeField(null=True, blank=True)
    update_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.widget_type})"
    
    class Meta:
        db_table = 'dashboard_widgets'
        ordering = ['position_y', 'position_x']


class Report(models.Model):
    """
    AI-generated reports and analytics
    """
    REPORT_TYPES = (
        ('daily_summary', 'Daily Summary'),
        ('weekly_performance', 'Weekly Performance'),
        ('monthly_analysis', 'Monthly Analysis'),
        ('lead_analysis', 'Lead Analysis'),
        ('social_media_report', 'Social Media Report'),
        ('ad_performance', 'Ad Performance'),
        ('business_insights', 'Business Insights'),
        ('custom', 'Custom Report'),
    )
    
    REPORT_STATUS = (
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('scheduled', 'Scheduled'),
    )
    
    # Report details
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Content
    executive_summary = models.TextField(blank=True)
    key_findings = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    detailed_analysis = models.TextField(blank=True)
    
    # Data and charts
    data_analyzed = models.JSONField(default=dict)
    charts_data = models.JSONField(default=list)
    attachments = models.JSONField(default=list)  # File URLs
    
    # Time period
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    
    # AI generation
    ai_generated = models.BooleanField(default=True)
    ai_model_used = models.CharField(max_length=100, blank=True)
    generation_prompt = models.TextField(blank=True)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Status and sharing
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='generating')
    is_automated = models.BooleanField(default=False)  # Auto-generated vs manual
    is_shared = models.BooleanField(default=False)
    shared_with = models.JSONField(default=list)  # User IDs or email addresses
    
    # Performance tracking
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.report_type} - {self.title}"
    
    class Meta:
        db_table = 'reports'
        ordering = ['-generated_at']


class TrafficAnalytics(models.Model):
    """
    Website and platform traffic analytics
    """
    TRAFFIC_SOURCES = (
        ('direct', 'Direct'),
        ('organic', 'Organic Search'),
        ('paid', 'Paid Search'),
        ('social', 'Social Media'),
        ('referral', 'Referral'),
        ('email', 'Email'),
        ('display', 'Display Ads'),
    )
    
    DEVICE_TYPES = (
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
    )
    
    # Traffic data
    date = models.DateField()
    source = models.CharField(max_length=20, choices=TRAFFIC_SOURCES)
    medium = models.CharField(max_length=50, blank=True)
    campaign = models.CharField(max_length=100, blank=True)
    
    # Metrics
    sessions = models.PositiveIntegerField(default=0)
    users = models.PositiveIntegerField(default=0)
    page_views = models.PositiveIntegerField(default=0)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    avg_session_duration = models.PositiveIntegerField(default=0)  # in seconds
    
    # Device and location
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Conversions
    conversions = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Page performance
    top_pages = models.JSONField(default=list)
    entry_pages = models.JSONField(default=list)
    exit_pages = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} - {self.source}"
    
    class Meta:
        db_table = 'traffic_analytics'
        unique_together = ['date', 'source', 'medium', 'campaign', 'device_type']
        ordering = ['-date']


class PerformanceAlert(models.Model):
    """
    System alerts for performance monitoring
    """
    ALERT_TYPES = (
        ('metric_threshold', 'Metric Threshold'),
        ('system_error', 'System Error'),
        ('api_failure', 'API Failure'),
        ('low_performance', 'Low Performance'),
        ('anomaly_detection', 'Anomaly Detection'),
    )
    
    SEVERITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    ALERT_STATUS = (
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )
    
    # Alert details
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    # Related data
    related_metric = models.CharField(max_length=100, blank=True)
    threshold_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=ALERT_STATUS, default='active')
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Actions taken
    actions_taken = models.JSONField(default=list)
    resolution_notes = models.TextField(blank=True)
    
    # AI analysis
    ai_detected = models.BooleanField(default=False)
    ai_recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.severity} - {self.title}"
    
    class Meta:
        db_table = 'performance_alerts'
        ordering = ['-created_at', '-severity']


class UserActivity(models.Model):
    """
    Track user activities within the dashboard
    """
    ACTIVITY_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('page_view', 'Page View'),
        ('widget_interaction', 'Widget Interaction'),
        ('report_generation', 'Report Generation'),
        ('data_export', 'Data Export'),
        ('settings_change', 'Settings Change'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    
    # Activity details
    page_url = models.URLField(blank=True)
    action_details = models.JSONField(default=dict)
    
    # Session tracking
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Performance
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
