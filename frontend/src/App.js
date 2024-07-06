import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ConversationWindow from './components/ConversationWindow';
import NewConversationButton from './components/NewConversationButton';
import axios from 'axios';
import './App.css';

function App() {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [conversation, setConversation] = useState([]);

  useEffect(() => {
    // Fetch sessions from backend
    axios.get('/api/sessions')
      .then(response => setSessions(response.data))
      .catch(error => console.error(error));
  }, []);

  const startNewConversation = () => {
    axios.post('/api/sessions')
      .then(response => {
        const newSession = response.data;
        setSessions([...sessions, newSession]);
        setCurrentSession(newSession.id);
        setConversation([]);
      })
      .catch(error => console.error(error));
  };

  const loadConversation = (sessionId) => {
    axios.get(`/api/sessions/${sessionId}`)
      .then(response => {
        setCurrentSession(sessionId);
        setConversation(response.data.conversation);
      })
      .catch(error => console.error(error));
  };

  return (
    <div className="App">
      <Sidebar 
        sessions={sessions} 
        loadConversation={loadConversation}
        currentSession={currentSession}
      />
      <div className="main-content">
        <NewConversationButton startNewConversation={startNewConversation} />
        <ConversationWindow conversation={conversation} />
      </div>
    </div>
  );
}

export default App;