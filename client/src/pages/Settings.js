import React from 'react';
import { Typography, Box } from '@mui/material';

const Settings = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings & Configuration
      </Typography>
      <Typography variant="body1">
        Settings interface coming soon. This will include:
      </Typography>
      <ul>
        <li>User profile management</li>
        <li>Team and permission settings</li>
        <li>Integration configurations</li>
        <li>AI model settings</li>
        <li>Communication preferences</li>
      </ul>
    </Box>
  );
};

export default Settings;