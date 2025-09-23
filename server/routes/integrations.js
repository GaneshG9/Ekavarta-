const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');

// All routes require authentication
router.use(authMiddleware);

// Third-party integrations
router.get('/status', (req, res) => {
  res.json({ 
    message: 'Integration status',
    integrations: {
      zapier: { connected: false },
      hubspot: { connected: false },
      salesforce: { connected: false },
      whatsapp: { connected: false },
      telegram: { connected: false }
    }
  });
});

router.post('/zapier/connect', (req, res) => {
  res.json({ message: 'Zapier integration configured' });
});

router.post('/hubspot/connect', (req, res) => {
  res.json({ message: 'HubSpot integration configured' });
});

router.post('/salesforce/connect', (req, res) => {
  res.json({ message: 'Salesforce integration configured' });
});

module.exports = router;