const Lead = require('../models/Lead');
const User = require('../models/User');

const leadController = {
  // Create new lead
  createLead: async (req, res) => {
    try {
      const leadData = {
        ...req.body,
        assignedBy: req.user.userId
      };

      const lead = new Lead(leadData);
      await lead.save();

      // Populate assigned user details
      await lead.populate('assignedTo assignedBy', 'name email');

      // Emit real-time update
      const io = req.app.get('io');
      if (lead.assignedTo) {
        io.to(`dashboard-${lead.assignedTo._id}`).emit('new-lead', lead);
      }

      res.status(201).json({
        message: 'Lead created successfully',
        lead
      });
    } catch (error) {
      console.error('Create lead error:', error);
      res.status(500).json({ message: 'Error creating lead', error: error.message });
    }
  },

  // Get all leads with filters and pagination
  getLeads: async (req, res) => {
    try {
      const {
        page = 1,
        limit = 10,
        status,
        businessType,
        source,
        priority,
        assignedTo,
        search,
        sortBy = 'createdAt',
        sortOrder = 'desc'
      } = req.query;

      // Build filter object
      const filter = { isActive: true };

      // Role-based filtering
      if (req.user.role === 'agent') {
        filter.assignedTo = req.user.userId;
      } else if (req.user.role === 'manager') {
        // Manager can see leads in their department
        const departmentAgents = await User.find({ 
          department: req.user.department,
          role: 'agent' 
        }).select('_id');
        filter.assignedTo = { $in: departmentAgents.map(agent => agent._id) };
      }

      if (status) filter.status = status;
      if (businessType) filter.businessType = businessType;
      if (source) filter.source = source;
      if (priority) filter.priority = priority;
      if (assignedTo) filter.assignedTo = assignedTo;

      // Search functionality
      if (search) {
        filter.$or = [
          { firstName: { $regex: search, $options: 'i' } },
          { lastName: { $regex: search, $options: 'i' } },
          { email: { $regex: search, $options: 'i' } },
          { phone: { $regex: search, $options: 'i' } },
          { company: { $regex: search, $options: 'i' } }
        ];
      }

      // Pagination
      const skip = (page - 1) * limit;
      const sortOptions = { [sortBy]: sortOrder === 'desc' ? -1 : 1 };

      const leads = await Lead.find(filter)
        .populate('assignedTo assignedBy', 'name email department')
        .sort(sortOptions)
        .skip(skip)
        .limit(parseInt(limit));

      const total = await Lead.countDocuments(filter);

      res.json({
        leads,
        pagination: {
          current: parseInt(page),
          pages: Math.ceil(total / limit),
          total,
          limit: parseInt(limit)
        }
      });
    } catch (error) {
      console.error('Get leads error:', error);
      res.status(500).json({ message: 'Error fetching leads', error: error.message });
    }
  },

  // Get single lead by ID
  getLeadById: async (req, res) => {
    try {
      const { id } = req.params;

      const lead = await Lead.findById(id)
        .populate('assignedTo assignedBy', 'name email department')
        .populate('interactions.agent', 'name email');

      if (!lead) {
        return res.status(404).json({ message: 'Lead not found' });
      }

      // Check permissions
      if (req.user.role === 'agent' && lead.assignedTo?.toString() !== req.user.userId) {
        return res.status(403).json({ message: 'Access denied' });
      }

      res.json({ lead });
    } catch (error) {
      console.error('Get lead error:', error);
      res.status(500).json({ message: 'Error fetching lead', error: error.message });
    }
  },

  // Update lead
  updateLead: async (req, res) => {
    try {
      const { id } = req.params;
      const updates = req.body;

      const lead = await Lead.findById(id);
      if (!lead) {
        return res.status(404).json({ message: 'Lead not found' });
      }

      // Check permissions
      if (req.user.role === 'agent' && lead.assignedTo?.toString() !== req.user.userId) {
        return res.status(403).json({ message: 'Access denied' });
      }

      // Update lead
      Object.keys(updates).forEach(key => {
        if (key !== '_id' && key !== 'createdAt') {
          lead[key] = updates[key];
        }
      });

      await lead.save();
      await lead.populate('assignedTo assignedBy', 'name email department');

      // Emit real-time update
      const io = req.app.get('io');
      if (lead.assignedTo) {
        io.to(`dashboard-${lead.assignedTo._id}`).emit('lead-updated', lead);
      }

      res.json({
        message: 'Lead updated successfully',
        lead
      });
    } catch (error) {
      console.error('Update lead error:', error);
      res.status(500).json({ message: 'Error updating lead', error: error.message });
    }
  },

  // Add interaction to lead
  addInteraction: async (req, res) => {
    try {
      const { id } = req.params;
      const interactionData = {
        ...req.body,
        agent: req.user.userId,
        date: new Date()
      };

      const lead = await Lead.findById(id);
      if (!lead) {
        return res.status(404).json({ message: 'Lead not found' });
      }

      // Check permissions
      if (req.user.role === 'agent' && lead.assignedTo?.toString() !== req.user.userId) {
        return res.status(403).json({ message: 'Access denied' });
      }

      lead.interactions.push(interactionData);
      lead.lastContactDate = new Date();

      // Update next follow-up if provided
      if (interactionData.nextActionDate) {
        lead.nextFollowUp = interactionData.nextActionDate;
      }

      await lead.save();
      await lead.populate('interactions.agent', 'name email');

      // Emit real-time update
      const io = req.app.get('io');
      if (lead.assignedTo) {
        io.to(`dashboard-${lead.assignedTo._id}`).emit('interaction-added', {
          leadId: lead._id,
          interaction: interactionData
        });
      }

      res.json({
        message: 'Interaction added successfully',
        interaction: lead.interactions[lead.interactions.length - 1]
      });
    } catch (error) {
      console.error('Add interaction error:', error);
      res.status(500).json({ message: 'Error adding interaction', error: error.message });
    }
  },

  // Assign lead to agent
  assignLead: async (req, res) => {
    try {
      const { id } = req.params;
      const { assignedTo } = req.body;

      // Check if target user exists and is an agent
      const targetUser = await User.findById(assignedTo);
      if (!targetUser || !['agent', 'manager'].includes(targetUser.role)) {
        return res.status(400).json({ message: 'Invalid user for assignment' });
      }

      const lead = await Lead.findById(id);
      if (!lead) {
        return res.status(404).json({ message: 'Lead not found' });
      }

      lead.assignedTo = assignedTo;
      lead.assignedBy = req.user.userId;
      lead.assignedAt = new Date();

      await lead.save();
      await lead.populate('assignedTo assignedBy', 'name email department');

      // Emit real-time update to new assignee
      const io = req.app.get('io');
      io.to(`dashboard-${assignedTo}`).emit('lead-assigned', lead);

      res.json({
        message: 'Lead assigned successfully',
        lead
      });
    } catch (error) {
      console.error('Assign lead error:', error);
      res.status(500).json({ message: 'Error assigning lead', error: error.message });
    }
  },

  // Get lead statistics
  getLeadStats: async (req, res) => {
    try {
      const { timeframe = '30d' } = req.query;
      
      // Calculate date range
      const endDate = new Date();
      const startDate = new Date();
      
      switch (timeframe) {
        case '7d':
          startDate.setDate(startDate.getDate() - 7);
          break;
        case '30d':
          startDate.setDate(startDate.getDate() - 30);
          break;
        case '90d':
          startDate.setDate(startDate.getDate() - 90);
          break;
        case '1y':
          startDate.setFullYear(startDate.getFullYear() - 1);
          break;
        default:
          startDate.setDate(startDate.getDate() - 30);
      }

      // Build filter based on user role
      const filter = { 
        isActive: true,
        createdAt: { $gte: startDate, $lte: endDate }
      };

      if (req.user.role === 'agent') {
        filter.assignedTo = req.user.userId;
      }

      // Get statistics
      const [
        totalLeads,
        statusStats,
        sourceStats,
        businessTypeStats,
        priorityStats
      ] = await Promise.all([
        Lead.countDocuments(filter),
        Lead.aggregate([
          { $match: filter },
          { $group: { _id: '$status', count: { $sum: 1 } } }
        ]),
        Lead.aggregate([
          { $match: filter },
          { $group: { _id: '$source', count: { $sum: 1 } } }
        ]),
        Lead.aggregate([
          { $match: filter },
          { $group: { _id: '$businessType', count: { $sum: 1 } } }
        ]),
        Lead.aggregate([
          { $match: filter },
          { $group: { _id: '$priority', count: { $sum: 1 } } }
        ])
      ]);

      res.json({
        timeframe,
        totalLeads,
        breakdown: {
          status: statusStats,
          source: sourceStats,
          businessType: businessTypeStats,
          priority: priorityStats
        }
      });
    } catch (error) {
      console.error('Get lead stats error:', error);
      res.status(500).json({ message: 'Error fetching lead statistics', error: error.message });
    }
  }
};

module.exports = leadController;