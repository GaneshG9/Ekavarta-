const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');

// All routes require authentication
router.use(authMiddleware);

// Campaign management
router.get('/', (req, res) => {
  res.json({ message: 'Get campaigns', campaigns: [] });
});

router.post('/', (req, res) => {
  res.json({ message: 'Create campaign' });
});

router.get('/:id', (req, res) => {
  res.json({ message: 'Get campaign by ID' });
});

router.put('/:id', (req, res) => {
  res.json({ message: 'Update campaign' });
});

router.delete('/:id', (req, res) => {
  res.json({ message: 'Delete campaign' });
});

module.exports = router;