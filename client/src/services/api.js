import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// Auth service
export const authService = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (profileData) => api.put('/auth/profile', profileData),
  changePassword: (passwordData) => api.put('/auth/change-password', passwordData),
};

// Lead service
export const leadService = {
  getLeads: (params) => api.get('/leads', { params }),
  getLeadById: (id) => api.get(`/leads/${id}`),
  createLead: (leadData) => api.post('/leads', leadData),
  updateLead: (id, leadData) => api.put(`/leads/${id}`, leadData),
  addInteraction: (id, interactionData) => api.post(`/leads/${id}/interactions`, interactionData),
  assignLead: (id, assignedTo) => api.put(`/leads/${id}/assign`, { assignedTo }),
  getLeadStats: (timeframe) => api.get('/leads/stats', { params: { timeframe } }),
};

// Campaign service
export const campaignService = {
  getCampaigns: (params) => api.get('/campaigns', { params }),
  getCampaignById: (id) => api.get(`/campaigns/${id}`),
  createCampaign: (campaignData) => api.post('/campaigns', campaignData),
  updateCampaign: (id, campaignData) => api.put(`/campaigns/${id}`, campaignData),
  deleteCampaign: (id) => api.delete(`/campaigns/${id}`),
};

// CRM service
export const crmService = {
  getDashboard: () => api.get('/crm/dashboard'),
  getQuickStats: () => api.get('/crm/quick-stats'),
};

// Communication service
export const communicationService = {
  sendWhatsApp: (data) => api.post('/communication/whatsapp/send', data),
  sendTelegram: (data) => api.post('/communication/telegram/send', data),
  initiateCall: (data) => api.post('/communication/call/initiate', data),
  sendEmail: (data) => api.post('/communication/email/send', data),
  sendSMS: (data) => api.post('/communication/sms/send', data),
};

// Analytics service
export const analyticsService = {
  getOverview: () => api.get('/analytics/overview'),
  getLeadAnalytics: () => api.get('/analytics/leads'),
  getCampaignAnalytics: () => api.get('/analytics/campaigns'),
  getRevenueAnalytics: () => api.get('/analytics/revenue'),
};

// Integration service
export const integrationService = {
  getStatus: () => api.get('/integrations/status'),
  connectZapier: (config) => api.post('/integrations/zapier/connect', config),
  connectHubSpot: (config) => api.post('/integrations/hubspot/connect', config),
  connectSalesforce: (config) => api.post('/integrations/salesforce/connect', config),
};

export default api;