import React, { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

function MessageInput({ sendMessage }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(message);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        label="Type your message"
        fullWidth
      />
      <Button type="submit" variant="contained" color="primary">
        Send
      </Button>
    </form>
  );
}

export default MessageInput;