import React from 'react';

function ConversationWindow({ conversation }) {
  return (
    <div className="conversation-window">
      {conversation.map((turn, index) => (
        <div key={index} className="conversation-turn">
          <p><strong>User:</strong> {turn.user}</p>
          <p><strong>AI:</strong> {turn.ai}</p>
        </div>
      ))}
    </div>
  );
}

export default ConversationWindow;