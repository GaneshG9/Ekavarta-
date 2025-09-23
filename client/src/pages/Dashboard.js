import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  Button,
  IconButton,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Campaign,
  AttachMoney,
  Phone,
  Email,
  WhatsApp,
  Refresh,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { crmService, leadService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [refreshKey, setRefreshKey] = useState(0);

  // Fetch dashboard data
  const { data: dashboardData, isLoading: dashboardLoading } = useQuery(
    ['dashboard', refreshKey],
    () => crmService.getDashboard(),
    {
      staleTime: 30000, // 30 seconds
    }
  );

  // Fetch lead stats
  const { data: leadStats, isLoading: statsLoading } = useQuery(
    ['leadStats', refreshKey],
    () => leadService.getLeadStats('30d'),
    {
      staleTime: 30000,
    }
  );

  // Fetch recent leads
  const { data: recentLeads, isLoading: leadsLoading } = useQuery(
    ['recentLeads', refreshKey],
    () => leadService.getLeads({ limit: 5, sortBy: 'createdAt' }),
    {
      staleTime: 30000,
    }
  );

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const statsCards = [
    {
      title: 'Total Leads',
      value: leadStats?.totalLeads || 0,
      icon: <People />,
      color: '#1976d2',
      trend: '+12%',
    },
    {
      title: 'Active Campaigns',
      value: dashboardData?.data?.activeCompaigns || 0,
      icon: <Campaign />,
      color: '#2e7d32',
      trend: '+8%',
    },
    {
      title: 'Conversion Rate',
      value: `${dashboardData?.data?.conversionRate || 0}%`,
      icon: <TrendingUp />,
      color: '#ed6c02',
      trend: '+2.5%',
    },
    {
      title: 'Revenue',
      value: `₹${dashboardData?.data?.revenue || 0}`,
      icon: <AttachMoney />,
      color: '#9c27b0',
      trend: '+15%',
    },
  ];

  const getStatusColor = (status) => {
    const colors = {
      new: 'primary',
      contacted: 'info',
      qualified: 'warning',
      proposal_sent: 'secondary',
      negotiation: 'success',
      closed_won: 'success',
      closed_lost: 'error',
      follow_up: 'default',
    };
    return colors[status] || 'default';
  };

  const getBusinessTypeIcon = (type) => {
    const icons = {
      real_estate: '🏠',
      solar: '☀️',
      digital_marketing: '📱',
      other: '💼',
    };
    return icons[type] || '💼';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          Welcome back, {user?.name}!
        </Typography>
        <IconButton onClick={handleRefresh} color="primary">
          <Refresh />
        </IconButton>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={3}>
        {statsCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="textSecondary" gutterBottom variant="body2">
                      {card.title}
                    </Typography>
                    <Typography variant="h4">
                      {card.value}
                    </Typography>
                    <Typography variant="body2" color="success.main">
                      {card.trend} this month
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: card.color }}>
                    {card.icon}
                  </Avatar>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Recent Leads */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Leads
            </Typography>
            {leadsLoading ? (
              <Typography>Loading...</Typography>
            ) : (
              <List>
                {recentLeads?.leads?.slice(0, 5).map((lead) => (
                  <ListItem key={lead._id} divider>
                    <ListItemAvatar>
                      <Avatar>
                        {getBusinessTypeIcon(lead.businessType)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={`${lead.firstName} ${lead.lastName}`}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            {lead.email} • {lead.phone}
                          </Typography>
                          <Box mt={1}>
                            <Chip
                              label={lead.status.replace('_', ' ').toUpperCase()}
                              size="small"
                              color={getStatusColor(lead.status)}
                              sx={{ mr: 1 }}
                            />
                            <Chip
                              label={lead.businessType.replace('_', ' ').toUpperCase()}
                              size="small"
                              variant="outlined"
                            />
                          </Box>
                        </Box>
                      }
                    />
                    <Box display="flex" flexDirection="column" gap={1}>
                      <IconButton size="small" color="primary">
                        <Phone />
                      </IconButton>
                      <IconButton size="small" color="primary">
                        <Email />
                      </IconButton>
                      <IconButton size="small" color="success">
                        <WhatsApp />
                      </IconButton>
                    </Box>
                  </ListItem>
                ))}
              </List>
            )}
            <Box mt={2} textAlign="center">
              <Button variant="outlined" href="/leads">
                View All Leads
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  fullWidth
                  href="/leads?action=create"
                  sx={{ mb: 1 }}
                >
                  Add New Lead
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="outlined"
                  fullWidth
                  href="/campaigns?action=create"
                  sx={{ mb: 1 }}
                >
                  Create Campaign
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="outlined"
                  fullWidth
                  href="/analytics"
                  sx={{ mb: 1 }}
                >
                  View Analytics
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {/* Lead Status Breakdown */}
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Lead Status Breakdown
            </Typography>
            {statsLoading ? (
              <Typography>Loading...</Typography>
            ) : (
              <Box>
                {leadStats?.breakdown?.status?.map((item) => (
                  <Box
                    key={item._id}
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                    py={1}
                  >
                    <Typography variant="body2">
                      {item._id?.replace('_', ' ').toUpperCase()}
                    </Typography>
                    <Chip
                      label={item.count}
                      size="small"
                      color={getStatusColor(item._id)}
                    />
                  </Box>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;