const mongoose = require('mongoose');

const campaignSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  type: {
    type: String,
    enum: ['email', 'sms', 'whatsapp', 'cold_call', 'social_media', 'google_ads', 'facebook_ads'],
    required: true
  },
  businessType: {
    type: String,
    enum: ['real_estate', 'solar', 'digital_marketing', 'all'],
    required: true
  },
  
  // Campaign Configuration
  status: {
    type: String,
    enum: ['draft', 'scheduled', 'active', 'paused', 'completed', 'cancelled'],
    default: 'draft'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high'],
    default: 'medium'
  },
  
  // Scheduling
  startDate: {
    type: Date,
    required: true
  },
  endDate: {
    type: Date
  },
  schedule: {
    frequency: {
      type: String,
      enum: ['once', 'daily', 'weekly', 'monthly']
    },
    daysOfWeek: [Number], // 0-6, Sunday-Saturday
    timeOfDay: String, // HH:MM format
    timezone: { type: String, default: 'Asia/Kolkata' }
  },
  
  // Content
  content: {
    subject: String, // For email/sms
    message: String,
    template: String,
    variables: [String], // Dynamic variables like {firstName}, {company}
    attachments: [String], // File URLs
    callScript: String, // For cold calls
    language: {
      type: String,
      enum: ['english', 'hindi', 'both'],
      default: 'english'
    }
  },
  
  // Targeting
  targetAudience: {
    leadStatus: [String],
    businessTypes: [String],
    tags: [String],
    locations: [String],
    customFilters: mongoose.Schema.Types.Mixed
  },
  
  // AI Configuration
  aiSettings: {
    autoPersonalize: { type: Boolean, default: false },
    optimizeDeliveryTime: { type: Boolean, default: false },
    abTestContent: { type: Boolean, default: false },
    autoFollowUp: { type: Boolean, default: false },
    sentimentAnalysis: { type: Boolean, default: false }
  },
  
  // Analytics
  metrics: {
    sent: { type: Number, default: 0 },
    delivered: { type: Number, default: 0 },
    opened: { type: Number, default: 0 },
    clicked: { type: Number, default: 0 },
    replied: { type: Number, default: 0 },
    converted: { type: Number, default: 0 },
    unsubscribed: { type: Number, default: 0 },
    bounced: { type: Number, default: 0 }
  },
  
  // Budget and Cost
  budget: {
    total: Number,
    spent: { type: Number, default: 0 },
    currency: { type: String, default: 'INR' }
  },
  
  // Team
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  assignedTo: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  
  // Social Media Specific
  socialMediaConfig: {
    platforms: [String], // ['facebook', 'instagram', 'linkedin', 'twitter']
    adSets: [{
      platform: String,
      adSetId: String,
      budget: Number,
      targeting: mongoose.Schema.Types.Mixed
    }]
  },
  
  // Integration Settings
  integrations: {
    zapier: {
      webhookUrl: String,
      enabled: { type: Boolean, default: false }
    },
    hubspot: {
      listId: String,
      enabled: { type: Boolean, default: false }
    },
    salesforce: {
      campaignId: String,
      enabled: { type: Boolean, default: false }
    }
  },
  
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Indexes
campaignSchema.index({ type: 1, status: 1 });
campaignSchema.index({ businessType: 1, status: 1 });
campaignSchema.index({ createdBy: 1 });
campaignSchema.index({ startDate: 1, endDate: 1 });

module.exports = mongoose.model('Campaign', campaignSchema);