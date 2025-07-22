import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Container, CssBaseline } from '@mui/material';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';

const theme = createTheme({
  palette: {
    primary: { main: '#2196f3' },
    secondary: { main: '#f50057' },
    background: { default: '#f5f5f5' },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState(null);

  const formatMessageContent = (msg) => {
    const message = msg.message;
    let formattedContent = [];

    // Handle initial property search
    if (message.initial_search) {
      formattedContent.push({
        content: message.initial_search.message,
        type: 'search'
      });

      if (message.initial_search.properties?.length > 0) {
        const propertyList = message.initial_search.properties
          .map(p => `🏠 ${p.name}\n${p.description || ''}\nPrice: ${p.price}`)
          .join('\n\n');
        formattedContent.push({
          content: propertyList,
          type: 'properties'
        });
      }
    }

    // Handle analysis messages
    if (message.analysis) {
      formattedContent.push({
        content: message.analysis.message,
        type: 'analysis'
      });

      if (message.analysis.rejected_properties?.length > 0) {
        const rejections = message.analysis.rejected_properties
          .map(p => `❌ ${p.name}: ${p.reason}`)
          .join('\n');
        formattedContent.push({
          content: rejections,
          type: 'rejections'
        });
      }

      if (message.analysis.strategy?.length > 0) {
        const strategy = message.analysis.strategy.join('\n• ');
        formattedContent.push({
          content: `Strategy Points:\n• ${strategy}`,
          type: 'strategy'
        });
      }
    }

    // Handle strategy messages
    if (message.strategy) {
      formattedContent.push({
        content: message.strategy.message,
        type: 'strategy'
      });

      if (message.strategy.points?.length > 0) {
        const points = message.strategy.points.join('\n• ');
        formattedContent.push({
          content: `Key Points:\n• ${points}`,
          type: 'points'
        });
      }
    }

    // Handle final recommendations
    if (message.final_recommendations) {
      formattedContent.push({
        content: message.final_recommendations.message,
        type: 'recommendations'
      });

      if (message.final_recommendations.properties?.length > 0) {
        const properties = message.final_recommendations.properties
          .map(p => `✨ ${p.name}\n${p.highlight || ''}\nPrice: ${p.price}`)
          .join('\n\n');
        formattedContent.push({
          content: properties,
          type: 'final_properties'
        });
      }
    }

    // Handle summary messages
    if (message.summary) {
      formattedContent.push({
        content: message.summary,
        type: 'summary'
      });
    }

    return formattedContent.length > 0
      ? formattedContent
      : [{
          content: message.toString(),
          type: 'text'
        }];
  };

  const handleSendMessage = async (message) => {
    setLoading(true);
    setMessages(prev => [...prev, { type: 'user', content: message }]);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setCurrentResponse(data);

      if (Array.isArray(data.conversation)) {
        let previousAgent = null;
        
        for (const msg of data.conversation) {
          // Add typing indicator
          setMessages(prev => [...prev, {
            type: 'typing',
            agent: msg.name,
            content: '...',
            emoji: msg.emoji,
            role: msg.role
          }]);

          // Simulate typing time
          const typingTime = Math.min(2000, 500 + Math.random() * 1000);
          await new Promise(resolve => setTimeout(resolve, typingTime));

          // Remove typing indicator
          setMessages(prev => prev.filter(m => m.type !== 'typing'));

          // If it's a new agent speaking, add a handoff effect
          if (previousAgent && previousAgent !== msg.name) {
            setMessages(prev => [...prev.slice(0, -1), {
              ...prev[prev.length - 1],
              messageType: 'handoff',
              handoff: msg.name
            }]);
            await new Promise(resolve => setTimeout(resolve, 1000));
          }

          // Process agent's messages
          const formattedMessages = formatMessageContent(msg);
          
          for (const formattedMsg of formattedMessages) {
            setMessages(prev => [...prev, {
              type: 'agent',
              agent: msg.name,
              content: formattedMsg.content,
              emoji: msg.emoji,
              role: msg.role,
              messageType: msg.type,
              contentType: formattedMsg.type
            }]);

            // Add slight delay between multiple messages from same agent
            await new Promise(resolve => setTimeout(resolve, 800));
          }

          previousAgent = msg.name;
        }
      } else {
        setMessages(prev => [...prev, {
          type: 'agent',
          agent: 'Sarah',
          content: 'Sorry, I encountered an error. Please try again.',
          emoji: '👱‍♀️',
          role: 'Team Lead',
          messageType: 'error'
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        type: 'agent',
        agent: 'Sarah',
        content: 'Sorry, I encountered an error. Please try again.',
        emoji: '👱‍♀️',
        messageType: 'error'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
        <Header />
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          sx={{ flexGrow: 1 }}
        />
      </Container>
    </ThemeProvider>
  );
}

export default App;
