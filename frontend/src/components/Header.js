import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Box, Chip, Tooltip, IconButton } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import PeopleIcon from '@mui/icons-material/People';
import { motion, AnimatePresence } from 'framer-motion';

const agentStatuses = [
  { name: "Sarah", emoji: "👱‍♀️", status: "Team Lead", color: "#FF69B4" },
  { name: "Mike", emoji: "🏠", status: "Property Expert", color: "#4CAF50" },
  { name: "Emma", emoji: "🌟", status: "Amenities Pro", color: "#9C27B0" },
  { name: "Jessica", emoji: "💰", status: "Negotiator", color: "#FFA500" },
  { name: "Robert", emoji: "📝", status: "Closing Whiz", color: "#795548" }
];

function Header() {
  const [showTeam, setShowTeam] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getGreeting = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return "Good Morning! ☀️";
    if (hour < 18) return "Good Afternoon! 🌤️";
    return "Good Evening! 🌙";
  };

  return (
    <AppBar 
      position="static" 
      sx={{ 
        mb: 2, 
        borderRadius: 1,
        background: 'linear-gradient(90deg, #1976d2, #1565c0)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
      }}
    >
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <motion.div
            whileHover={{ rotate: 360, scale: 1.2 }}
            transition={{ duration: 0.5 }}
          >
            <HomeIcon sx={{ mr: 2, fontSize: '2rem' }} />
          </motion.div>
          <Box>
            <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
              AI Real Estate Team
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.9 }}>
              {getGreeting()} • {currentTime.toLocaleTimeString()}
            </Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <motion.div whileHover={{ scale: 1.05 }}>
            <Tooltip title="Meet the Team">
              <IconButton 
                color="inherit" 
                onClick={() => setShowTeam(!showTeam)}
                sx={{ 
                  bgcolor: 'rgba(255, 255, 255, 0.1)',
                  '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.2)' }
                }}
              >
                <PeopleIcon />
              </IconButton>
            </Tooltip>
          </motion.div>
          
          <AnimatePresence>
            {showTeam && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                style={{ display: 'flex', gap: '8px' }}
              >
                {agentStatuses.map((agent) => (
                  <motion.div
                    key={agent.name}
                    whileHover={{ y: -4 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Tooltip title={`${agent.status}`}>
                      <Chip
                        label={`${agent.emoji} ${agent.name}`}
                        sx={{
                          bgcolor: 'rgba(255, 255, 255, 0.9)',
                          color: agent.color,
                          fontWeight: 'bold',
                          '&:hover': {
                            bgcolor: 'rgba(255, 255, 255, 1)',
                          }
                        }}
                      />
                    </Tooltip>
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
