const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');

// All routes require authentication
router.use(authMiddleware);

// Analytics and reporting
router.get('/overview', (req, res) => {
  res.json({ message: 'Analytics overview' });
});

router.get('/leads', (req, res) => {
  res.json({ message: 'Lead analytics' });
});

router.get('/campaigns', (req, res) => {
  res.json({ message: 'Campaign analytics' });
});

router.get('/revenue', (req, res) => {
  res.json({ message: 'Revenue analytics' });
});

module.exports = router;