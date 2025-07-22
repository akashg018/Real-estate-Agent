import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';

function ResponseDisplay({ response }) {
  if (!response || !response.conversation) return null;

  return (
    <Box sx={{ mb: 2 }}>
      {response.conversation.map((step, index) => (
        <Paper key={index} elevation={3} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            {step.emoji} {step.name} — <small>{step.role}</small>
          </Typography>

          <Typography variant="body1" sx={{ mb: 2 }}>
            {step.message}
          </Typography>

          {step.output && renderAgentOutput(step.name, step.output)}
        </Paper>
      ))}
    </Box>
  );
}

function renderAgentOutput(agentName, output) {
switch (agentName.trim().toLowerCase()) {
  case "mike":
    return renderResidentialOutput(output);
  case "jessica":
    return renderNegotiationOutput(output);
  case "robert":
    return renderLegalOutput(output);
  case "emma":
    return renderLifestyleOutput(output);
  case "jack":
    return renderLocationOutput(output);
  default:
    return null;
 }
}

function renderResidentialOutput(output) {
  const properties = output?.final_recommendations?.properties || [];
  if (properties.length === 0) return null;

  return (
    <>
      <Typography variant="subtitle1" gutterBottom>🏡 Final Property Recommendations</Typography>
      <Grid container spacing={2}>
        {properties.map((property, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>{property.name}</Typography>
                <Typography variant="body2" color="text.secondary">{property.price}</Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>{property.highlight}</Typography>
                {property.features.map((feature, i) => (
                  <Chip key={i} label={feature} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                ))}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </>
  );
}

function renderNegotiationOutput(output) {
  const { analysis, strategy, expected_outcome } = output || {};
  if (!strategy) return null;

  return (
    <>
      <Typography variant="subtitle1" gutterBottom>💰 Negotiation Strategy</Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>{strategy.message}</Typography>
      <Typography variant="body2"><strong>Initial Offer:</strong> {strategy.initial_offer?.amount}</Typography>
      <Typography variant="body2"><strong>Reason:</strong> {strategy.initial_offer?.reasoning}</Typography>

      <Divider sx={{ my: 2 }} />

      <Typography variant="body2"><strong>Leverage Points:</strong></Typography>
      <List dense>
        {analysis?.leverage_points?.map((point, idx) => (
          <ListItem key={idx}><ListItemText primary={point} /></ListItem>
        ))}
      </List>

      <Typography variant="body2"><strong>Expected Outcome:</strong></Typography>
      <List dense>
        {Object.entries(expected_outcome || {}).map(([key, val]) => (
          <ListItem key={key}><ListItemText primary={`${key}: ${val}`} /></ListItem>
        ))}
      </List>
    </>
  );
}

function renderLegalOutput(output) {
  if (!output) return null;

  return (
    <>
      {/* Initial Search Message */}
      <Typography variant="subtitle1" gutterBottom>📝 Legal Review Summary</Typography>
      <Typography variant="body2" sx={{ mb: 2 }}>
        {output.initial_search?.message}
      </Typography>

      {/* Property-wise Contracts */}
      {output.initial_search?.contracts?.map((contract, idx) => (
        <Card key={idx} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="subtitle2" gutterBottom>
              📑 {contract.property || 'Unnamed Property'}
            </Typography>

            <Typography variant="body2" sx={{ mb: 1 }}><strong>Key Legal Terms:</strong></Typography>
            <List dense>
              {Object.entries(contract.key_terms || {}).map(([term, value], i) => (
                <ListItem key={i}>
                  <ListItemText
                    primary={term.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    secondary={typeof value === 'object' ? JSON.stringify(value) : value}
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      ))}

      {/* Legal Points Analysis */}
      <Typography variant="subtitle2" gutterBottom>📋 Key Legal Points to Consider:</Typography>
      <List dense>
        {output.analysis?.points?.map((point, idx) => (
          <ListItem key={idx}>
            <ListItemText primary={point} />
          </ListItem>
        ))}
      </List>

      {/* Final Recommendations */}
      <Typography variant="subtitle2" sx={{ mt: 2 }}>⚖️ Final Legal Recommendations</Typography>

      {/* Required Documents */}
      <Typography variant="body2"><strong>Required Documents:</strong></Typography>
      <List dense>
        {output.final_recommendations?.documents_needed?.map((doc, idx) => (
          <ListItem key={idx}>
            <ListItemText primary={doc} />
          </ListItem>
        ))}
      </List>

      {/* Legal Timeline */}
      <Typography variant="body2" sx={{ mt: 2 }}><strong>Legal Process Timeline:</strong></Typography>
      <List dense>
        {output.final_recommendations?.legal_timeline?.map((step, idx) => (
          <ListItem key={idx}>
            <ListItemText primary={step} />
          </ListItem>
        ))}
      </List>
    </>
  );
}


function renderLifestyleOutput(output) {
  if (!output?.neighborhood_guides) return null;

  return (
    <>
      <Typography variant="subtitle1" gutterBottom>🌟 Lifestyle Evaluation</Typography>
      {output.neighborhood_guides.map((guide, idx) => (
        <Box key={idx} sx={{ mb: 2 }}>
          <Typography variant="subtitle2">{guide.name}</Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>{guide.description}</Typography>
          <Typography variant="body2"><strong>Amenities:</strong> {guide.amenities.join(', ')}</Typography>
          <Typography variant="body2"><strong>Foodie Tips:</strong> {guide.foodie_tips.join(', ')}</Typography>
          <Typography variant="body2"><strong>Pros:</strong> {guide.pros.join(', ')}</Typography>
          <Typography variant="body2"><strong>Cons:</strong> {guide.cons.join(', ')}</Typography>
        </Box>
      ))}
    </>
  );
}

function renderLocationOutput(output) {
  if (!output) return null;

  const { average_commute_time, key_distances, transport_options } = output;

  return (
    <>
      <Typography variant="subtitle1" gutterBottom>📍 Neighborhood Snapshot</Typography>

      {average_commute_time && (
        <Typography variant="body2" sx={{ mb: 1 }}>
          <strong>Average Commute Time:</strong> {average_commute_time}
        </Typography>
      )}

      {key_distances && (
        <>
          <Typography variant="body2"><strong>Key Distances:</strong></Typography>
          <List dense>
            {Object.entries(key_distances).map(([location, distance], idx) => (
              <ListItem key={idx}>
                <ListItemText
                  primary={location.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  secondary={distance}
                />
              </ListItem>
            ))}
          </List>
        </>
      )}

      {Array.isArray(transport_options) && transport_options.length > 0 && (
        <>
          <Typography variant="body2"><strong>Available Transport Options:</strong></Typography>
          <List dense>
            {transport_options.map((option, idx) => (
              <ListItem key={idx}>
                <ListItemText primary={option} />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </>
  );
}
export default ResponseDisplay;
