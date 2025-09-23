const mongoose = require('mongoose');

const leadSchema = new mongoose.Schema({
  // Basic Information
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    lowercase: true,
    trim: true
  },
  phone: {
    type: String,
    required: true,
    trim: true
  },
  alternatePhone: {
    type: String,
    trim: true
  },
  
  // Contact Information
  address: {
    street: String,
    city: String,
    state: String,
    pincode: String,
    country: { type: String, default: 'India' }
  },
  
  // Business Information
  businessType: {
    type: String,
    enum: ['real_estate', 'solar', 'digital_marketing', 'other'],
    required: true
  },
  company: {
    type: String,
    trim: true
  },
  designation: {
    type: String,
    trim: true
  },
  
  // Lead Management
  source: {
    type: String,
    enum: ['website', 'social_media', 'referral', 'cold_call', 'whatsapp', 'telegram', 'email', 'advertisement'],
    required: true
  },
  status: {
    type: String,
    enum: ['new', 'contacted', 'qualified', 'proposal_sent', 'negotiation', 'closed_won', 'closed_lost', 'follow_up'],
    default: 'new'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high', 'urgent'],
    default: 'medium'
  },
  
  // Assignment
  assignedTo: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  assignedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  assignedAt: {
    type: Date
  },
  
  // Requirements
  requirements: {
    budget: {
      min: Number,
      max: Number,
      currency: { type: String, default: 'INR' }
    },
    timeline: String,
    specificNeeds: String,
    propertyType: {
      type: String,
      enum: ['residential', 'commercial', 'industrial', 'agricultural']
    },
    solarCapacity: String,
    marketingGoals: [String]
  },
  
  // Interaction History
  interactions: [{
    type: {
      type: String,
      enum: ['call', 'email', 'whatsapp', 'telegram', 'meeting', 'proposal', 'follow_up']
    },
    date: { type: Date, default: Date.now },
    agent: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    notes: String,
    outcome: String,
    nextAction: String,
    nextActionDate: Date
  }],
  
  // AI Insights
  aiScore: {
    type: Number,
    min: 0,
    max: 100,
    default: 50
  },
  aiInsights: {
    buyingProbability: Number,
    bestContactTime: String,
    preferredChannel: String,
    keyMotivators: [String],
    objections: [String]
  },
  
  // Tags and Notes
  tags: [String],
  notes: String,
  
  // Tracking
  lastContactDate: Date,
  nextFollowUp: Date,
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Indexes for better performance
leadSchema.index({ email: 1 });
leadSchema.index({ phone: 1 });
leadSchema.index({ businessType: 1, status: 1 });
leadSchema.index({ assignedTo: 1, status: 1 });
leadSchema.index({ aiScore: -1 });
leadSchema.index({ nextFollowUp: 1 });

module.exports = mongoose.model('Lead', leadSchema);