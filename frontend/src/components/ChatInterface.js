import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  IconButton, 
  Paper, 
  Typography,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  // Divider, // Removed unused import
  Accordion,
  AccordionSummary,
  AccordionDetails,
  // Badge // Removed unused import
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HomeIcon from '@mui/icons-material/Home';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import GavelIcon from '@mui/icons-material/Gavel';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import DirectionsBusIcon from '@mui/icons-material/DirectionsBus';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ReactTypingEffect from 'react-typing-effect';
import { motion, AnimatePresence } from 'framer-motion';

function ChatInterface({ messages: rawMessages, onSendMessage, loading }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Parse the JSON conversation data
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (rawMessages && rawMessages.length > 0) {
      const lastMessage = rawMessages[rawMessages.length - 1];
      
      if (lastMessage.type === 'agent' && lastMessage.content) {
        try {
          const parsed = JSON.parse(lastMessage.content);
          if (parsed.conversation) {
            const timestamp = Date.now();
            const formattedMessages = parsed.conversation.map((msg, index) => ({
              id: `${timestamp}-${index}-${msg.name || 'user'}-${msg.type || 'message'}`,
              type: 'agent',
              agent: msg.name,
              role: msg.role,
              emoji: msg.emoji,
              content: msg.message,
              messageType: msg.type,
              output: msg.output,
              timestamp: timestamp
            }));
            setMessages([...rawMessages.slice(0, -1), ...formattedMessages]);
          } else {
            setMessages(rawMessages);
          }
        } catch (e) {
          setMessages(rawMessages);
        }
      } else {
        setMessages(rawMessages);
      }
    }
  }, [rawMessages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const getAgentColor = (agent) => {
    const colors = {
      'Sarah': '#FF69B4',    // Hot pink for the team lead
      'Mike': '#4CAF50',     // Green for properties
      'Jessica': '#FFA500',  // Orange for negotiations
      'Emma': '#9C27B0',     // Purple for lifestyle
      'Jack': '#2196F3',     // Blue for location
      'Robert': '#795548'    // Brown for legal
    };
    return colors[agent] || '#666666';
  };

  const messageTransition = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
    transition: { duration: 0.3 }
  };

  const renderPropertyCard = (property, uniqueKey) => (
    <Grid item xs={12} md={6} key={uniqueKey}>
      <motion.div whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
        <Card elevation={3} sx={{ height: '100%' }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
              <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
                {property.name}
              </Typography>
              <Chip 
                label={property.price} 
                color="primary" 
                variant="filled"
                sx={{ fontWeight: 'bold' }}
              />
            </Box>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {property.highlight}
            </Typography>

            <Typography variant="body2" color="success.main" sx={{ mb: 2, fontWeight: 'medium' }}>
              {property.availability}
            </Typography>

            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {property.features?.map((feature, idx) => (
                <Chip 
                  key={`feature-${feature}-${idx}`} 
                  label={feature} 
                  size="small" 
                  variant="outlined"
                  sx={{ fontSize: '0.75rem' }}
                />
              ))}
            </Box>
          </CardContent>
        </Card>
      </motion.div>
    </Grid>
  );

  const renderNegotiationDetails = (output) => {
    if (!output) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          <AttachMoneyIcon sx={{ mr: 1 }} /> Negotiation Strategy
        </Typography>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12}>
            <Card sx={{ bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Market Analysis</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>{output.market_analysis?.summary}</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Recent Sales</Typography>
                    <Typography variant="body2">{output.market_analysis?.recent_sales}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Market Trend</Typography>
                    <Typography variant="body2">{output.market_analysis?.trend}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Days on Market</Typography>
                    <Typography variant="body2">{output.market_analysis?.days_on_market}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={4}>
            <Card sx={{ bgcolor: 'success.light', color: 'success.contrastText', height: '100%' }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Best Case</Typography>
                <Typography variant="h6" sx={{ mb: 1 }}>{output.expected_outcome?.best_case?.price}</Typography>
                <Typography variant="body2">{output.expected_outcome?.best_case?.strategy}</Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption">Probability:</Typography>
                  <Typography variant="body2">{output.expected_outcome?.best_case?.probability}</Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card sx={{ bgcolor: 'info.light', color: 'info.contrastText', height: '100%' }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Realistic Target</Typography>
                <Typography variant="h6" sx={{ mb: 1 }}>{output.expected_outcome?.realistic?.price}</Typography>
                <Typography variant="body2">{output.expected_outcome?.realistic?.strategy}</Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption">Probability:</Typography>
                  <Typography variant="body2">{output.expected_outcome?.realistic?.probability}</Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card sx={{ bgcolor: 'warning.light', color: 'warning.contrastText', height: '100%' }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Walk Away Point</Typography>
                <Typography variant="h6" sx={{ mb: 1 }}>{output.expected_outcome?.walkaway?.price}</Typography>
                <Typography variant="body2">{output.expected_outcome?.walkaway?.reason}</Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption">Market Impact:</Typography>
                  <Typography variant="body2">{output.expected_outcome?.walkaway?.impact}</Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>Leverage Points</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List dense>
                  {output.analysis?.leverage_points?.map((point, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon>
                        <CheckCircleIcon color="success" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={point.point}
                        secondary={point.explanation}
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          </Grid>
          <Grid item xs={12} md={6}>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>Negotiation Timeline</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List dense>
                  {output.timeline?.map((step, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon>
                        {idx + 1}.
                      </ListItemIcon>
                      <ListItemText 
                        primary={step.action}
                        secondary={step.timing}
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderLegalDetails = (output) => {
    if (!output) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          <GavelIcon sx={{ mr: 1 }} /> Closing Process Overview
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Current Status</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Phase</Typography>
                    <Typography variant="body1">{output.status?.current_phase}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Expected Closing</Typography>
                    <Typography variant="body1">{output.status?.expected_closing_date}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2">Next Action</Typography>
                    <Typography variant="body1">{output.status?.next_action}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Required Documents</Typography>
                <List dense>
                  {output.documents_needed?.map((doc, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon>
                        <CheckCircleIcon fontSize="small" color={doc.status === 'completed' ? 'success' : 'action'} />
                      </ListItemIcon>
                      <ListItemText 
                        primary={doc.name}
                        secondary={
                          <Typography variant="caption" color={doc.deadline ? 'error' : 'textSecondary'}>
                            {doc.status === 'pending' ? `Due by: ${doc.deadline}` : `Completed: ${doc.completed_date}`}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Transaction Details</Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Box>
                    <Typography variant="subtitle2" color="primary">Purchase Agreement</Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, ml: 2 }}>
                      <Typography variant="body2">
                        <strong>Purchase Price:</strong> {output.transaction?.purchase_price}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Earnest Money:</strong> {output.transaction?.earnest_money}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Down Payment:</strong> {output.transaction?.down_payment}
                      </Typography>
                    </Box>
                  </Box>

                  <Box>
                    <Typography variant="subtitle2" color="primary">Key Dates</Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, ml: 2 }}>
                      <Typography variant="body2">
                        <strong>Inspection Period:</strong> {output.key_dates?.inspection_period}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Title Review:</strong> {output.key_dates?.title_review}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Final Walkthrough:</strong> {output.key_dates?.final_walkthrough}
                      </Typography>
                    </Box>
                  </Box>

                  <Box>
                    <Typography variant="subtitle2" color="primary">Closing Costs (Estimated)</Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, ml: 2 }}>
                      {output.closing_costs?.map((cost, idx) => (
                        <Typography key={idx} variant="body2">
                          <strong>{cost.name}:</strong> {cost.amount}
                        </Typography>
                      ))}
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>Closing Process Timeline</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List dense>
                  {output.timeline?.map((step, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon>
                        <CheckCircleIcon fontSize="small" color={step.completed ? 'success' : 'action'} />
                      </ListItemIcon>
                      <ListItemText 
                        primary={step.action}
                        secondary={
                          <Typography variant="caption">
                            {step.completed ? `Completed: ${step.completion_date}` : `Due: ${step.due_date}`}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderLifestyleDetails = (output) => {
    if (!output) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          🌟 Lifestyle Insights
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  <LocationOnIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Nearby Amenities
                </Typography>
                <List dense>
                  {output.nearby_amenities?.map((amenity, idx) => (
                    <ListItem key={`amenity-${amenity.amenity}-${idx}`}>
                      <ListItemText 
                        primary={amenity.amenity}
                        secondary={`${amenity.distance} - ${amenity.details}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  <RestaurantIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Local Gems
                </Typography>
                <List dense>
                  {output.neighborhood_gems?.map((gem, idx) => (
                    <ListItem key={idx}>
                      <ListItemText 
                        primary={gem.name}
                        secondary={gem.description}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Local Tips</Typography>
                {output.local_tips?.map((tip, idx) => (
                  <Box key={idx} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <span style={{ marginRight: 8 }}>{tip.emoji}</span>
                    <Typography variant="body2">{tip.tip}</Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderLocationDetails = (output) => {
    if (!output) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          <DirectionsBusIcon sx={{ mr: 1 }} /> Location Analysis
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Commute Info</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  <strong>Average Commute:</strong> {output.average_commute_time}
                </Typography>
                
                <Typography variant="subtitle2" gutterBottom>Key Distances</Typography>
                {output.key_distances && Object.entries(output.key_distances).map(([key, value]) => (
                  <Typography key={key} variant="body2">
                    <strong>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {value}
                  </Typography>
                ))}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>Transport Options</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {output.transport_options?.map((option, idx) => (
                    <Chip key={idx} label={option} variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderAgentOutput = (agent, output) => {
    if (!output) return null;

    switch (agent) {
      case 'Mike':
        const properties = output.final_recommendations?.properties || output.initial_search?.properties || [];
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
              <HomeIcon sx={{ mr: 1 }} /> Property Recommendations
            </Typography>
            <Grid container spacing={2}>
              {properties.map((property, idx) => renderPropertyCard(property, `property-${property.name}-${idx}`))}
            </Grid>
          </Box>
        );

      case 'Jessica':
        return renderNegotiationDetails(output);

      case 'Robert':
        return renderLegalDetails(output);

      case 'Emma':
        return renderLifestyleDetails(output);

      case 'Jack':
        return renderLocationDetails(output);

      case 'Sarah':
        // For Sarah's summary, render all the collected information
        if (output.residential_summary || output.negotiation_summary || output.legal_summary) {
          return (
            <Box sx={{ mt: 2 }}>
              <Typography variant="h5" sx={{ mb: 3, textAlign: 'center', fontWeight: 'bold' }}>
                📋 Complete Analysis Summary
              </Typography>

              {output.residential_summary?.final_recommendations?.properties && (
                <Box sx={{ mb: 4 }}>
                  <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                    <HomeIcon sx={{ mr: 1 }} /> Final Property Recommendations
                  </Typography>
                  <Grid container spacing={2}>
                    {output.residential_summary.final_recommendations.properties.map((property, idx) => 
                      renderPropertyCard(property, idx)
                    )}
                  </Grid>
                </Box>
              )}

              {output.negotiation_summary && (
                <Box sx={{ mb: 4 }}>
                  {renderNegotiationDetails(output.negotiation_summary)}
                </Box>
              )}

              {output.legal_summary && (
                <Box sx={{ mb: 4 }}>
                  {renderLegalDetails(output.legal_summary)}
                </Box>
              )}

              {output.lifestyle_summary && (
                <Box sx={{ mb: 4 }}>
                  {renderLifestyleDetails(output.lifestyle_summary)}
                </Box>
              )}

              {output.location_summary && (
                <Box sx={{ mb: 4 }}>
                  {renderLocationDetails(output.location_summary)}
                </Box>
              )}
            </Box>
          );
        }
        return null;

      default:
        return null;
    }
  };

  const renderAgentMessage = (message, uniqueKey) => {    
    return (
      <motion.div
        key={uniqueKey}
        layout
        {...messageTransition}
      >
        <Box sx={{ 
          display: 'flex',
          flexDirection: 'column',
          alignItems: message.type === 'user' ? 'flex-end' : 'flex-start',
          width: '100%',
          mb: 2
        }}>
          {/* Compact Agent Header */}
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 1,
            mb: 0.5
          }}>
            {/* Simple Agent Avatar with Emoji */}
            <Box sx={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: `${getAgentColor(message.agent)}15`,
              color: getAgentColor(message.agent),
              fontSize: '1rem',
              border: `1px solid ${getAgentColor(message.agent)}30`
            }}>
              {message.emoji || '👤'}
            </Box>

            {/* Compact Agent Info */}
            <Typography variant="body2" sx={{ 
              color: getAgentColor(message.agent),
              fontWeight: 500,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}>
              {message.agent}
              {message.messageType && message.messageType !== 'default' && (
                <Chip 
                  label={message.messageType}
                  size="small"
                  sx={{ 
                    height: 20,
                    fontSize: '0.7rem',
                    backgroundColor: `${getAgentColor(message.agent)}15`,
                    color: getAgentColor(message.agent)
                  }}
                />
              )}
            </Typography>
          </Box>

          {/* Message Content */}
          <Box sx={{ width: '100%', maxWidth: message.type === 'user' ? '70%' : '85%' }}>
            <Paper 
              elevation={1}
              sx={{ 
                backgroundColor: message.type === 'user' ? 'primary.main' : 'background.paper',
                color: message.type === 'user' ? 'white' : 'text.primary',
                borderRadius: 1.5,
                p: 1.5,
                position: 'relative',
                border: `1px solid ${message.type === 'user' ? 'transparent' : getAgentColor(message.agent)}15`,
              }}
            >
              {message.type === 'typing' ? (
                <ReactTypingEffect 
                  text={[`${message.agent} is thinking...`, `${message.agent} is analyzing...`]}
                  speed={50}
                  eraseSpeed={50}
                  typingDelay={100}
                  className="typing-effect"
                />
              ) : (
                <>
                  <Typography sx={{ whiteSpace: 'pre-wrap', mb: message.output ? 2 : 0 }}>
                    {message.content}
                  </Typography>
                  
                  {/* Render structured output */}
                  {renderAgentOutput(message.agent, message.output)}
                </>
              )}
            </Paper>
          </Box>

          {/* Transition Arrow for Handoffs */}
          {message.messageType === 'handoff' && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
            >
              <Box sx={{ 
                width: '100%',
                display: 'flex',
                justifyContent: 'center',
                my: 2
              }}>
                <Typography 
                  variant="body2" 
                  sx={{ 
                    color: 'text.secondary',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                    fontStyle: 'italic'
                  }}
                >
                  ↓ Passing to next agent ↓
                </Typography>
              </Box>
            </motion.div>
          )}
        </Box>
      </motion.div>
    );
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Paper 
        elevation={3} 
        sx={{ 
          flexGrow: 1,
          mb: 2, 
          p: 2, 
          overflow: 'auto',
          backgroundColor: '#fafafa',
          display: 'flex',
          flexDirection: 'column',
          gap: 2
        }}
      >
        <AnimatePresence mode="popLayout">
          {messages.map((message, index) => {
            // Generate a truly unique key combining multiple identifiers
            const uniqueKey = `${message.type}-${message.agent || 'user'}-${index}-${message.messageType || 'default'}`;
            return (
              <React.Fragment key={uniqueKey}>
                {renderAgentMessage(message, uniqueKey)}
              </React.Fragment>
            );
          })}
        </AnimatePresence>
        {loading && (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            p: 3
          }}>
            <Box sx={{ textAlign: 'center' }}>
              <CircularProgress sx={{ mb: 2 }} />
              <ReactTypingEffect 
                text={["Analyzing your request...", "Searching properties...", "Consulting with experts..."]}
                speed={50}
                eraseSpeed={50}
                typingDelay={100}
                className="typing-effect"
              />
            </Box>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Paper>

      <motion.form 
        onSubmit={handleSubmit}
        initial={false}
        animate={loading ? { opacity: 0.7 } : { opacity: 1 }}
      >
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask about properties (e.g., 'I'm looking for a place near Dallas University')"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
              }
            }}
          />
          <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
            <IconButton 
              type="submit" 
              color="primary" 
              disabled={!input.trim() || loading}
              sx={{ 
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
                '&:disabled': {
                  bgcolor: 'grey.300',
                }
              }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : <SendIcon />}
            </IconButton>
          </motion.div>
        </Box>
      </motion.form>
    </Box>
  );
}

export default ChatInterface;
