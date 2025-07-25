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

  const handleSendMessage = async (message) => {
    setLoading(true);
    setMessages(prev => [...prev, { 
      type: 'user', 
      content: message,
      id: Date.now()
    }]);

    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      if (data.conversation) {
        let previousAgent = null;
        
        for (const msg of data.conversation) {
          // Add typing indicator
          setMessages(prev => [...prev, {
            type: 'typing',
            agent: msg.name,
            content: '...',
            emoji: msg.emoji,
            role: msg.role,
            id: Date.now()
          }]);

          // Simulate typing time
          await new Promise(resolve => setTimeout(resolve, Math.min(2000, 500 + Math.random() * 1000)));

          // Remove typing indicator
          setMessages(prev => [
            ...prev.filter(m => m.type !== 'typing'),
            {
              id: Date.now(),
              type: 'agent',
              agent: msg.name,
              content: msg.message,
              emoji: msg.emoji,
              role: msg.role,
              messageType: msg.type,
              output: msg.output
            }
          ]);

          // If it's a new agent speaking, add a handoff effect
          if (previousAgent && previousAgent !== msg.name) {
            setMessages(prev => [...prev.slice(0, -1), {
              ...prev[prev.length - 1],
              messageType: 'handoff',
              handoff: msg.name
            }]);
            await new Promise(resolve => setTimeout(resolve, 1000));
          }

          previousAgent = msg.name;
        }
      } else {
        setMessages(prev => [...prev, {
          id: Date.now(),
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
        id: Date.now(),
        type: 'agent',
        agent: 'Sarah',
        content: 'Sorry, I encountered an error. Please try again.',
        emoji: '👱‍♀️',
        role: 'Team Lead',
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
