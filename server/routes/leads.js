const express = require('express');
const router = express.Router();
const leadController = require('../controllers/leadController');
const { authMiddleware, requireRole, requirePermission } = require('../middleware/auth');

// All routes require authentication
router.use(authMiddleware);

// Lead management routes
router.post('/', leadController.createLead);
router.get('/', leadController.getLeads);
router.get('/stats', leadController.getLeadStats);
router.get('/:id', leadController.getLeadById);
router.put('/:id', leadController.updateLead);
router.post('/:id/interactions', leadController.addInteraction);

// Assignment route (managers and admins only)
router.put('/:id/assign', requireRole(['manager', 'admin']), leadController.assignLead);

module.exports = router;