import React from 'react';
import { List, ListItem, ListItemText, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const SessionList = ({ sessions, onSelect, onDelete }) => {
  return (
    <List>
      {sessions.map((session, index) => (
        <ListItem
          key={index}
          button
          onClick={() => onSelect(session)}
        >
          <ListItemText primary={session.name} />
          <IconButton edge="end" onClick={() => onDelete(session)}>
            <DeleteIcon />
          </IconButton>
        </ListItem>
      ))}
    </List>
  );
};

export default SessionList;