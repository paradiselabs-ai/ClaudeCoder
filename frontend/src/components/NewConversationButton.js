import React from 'react';
import Button from '@mui/material/Button';

function NewConversationButton({ startNewConversation }) {
  return (
    <Button 
      variant="contained" 
      color="primary" 
      onClick={startNewConversation}
    >
      New Conversation
    </Button>
  );
}

export default NewConversationButton;