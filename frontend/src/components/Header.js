import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';

function Header() {
  return (
    <AppBar position="static" sx={{ mb: 2, borderRadius: 1 }}>
      <Toolbar>
        <HomeIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div">
          AI Real Estate Agent
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <Typography variant="subtitle2">
          Your Smart Property Assistant
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
