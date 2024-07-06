import React from 'react';

function Sidebar({ sessions, loadConversation, currentSession }) {
  return (
    <div className="sidebar">
      <h2>Sessions</h2>
      <ul>
        {sessions.map(session => (
          <li 
            key={session.id} 
            className={session.id === currentSession ? 'active' : ''}
            onClick={() => loadConversation(session.id)}
          >
            {session.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;