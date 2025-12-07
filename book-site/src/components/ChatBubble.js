import React, { useState } from 'react';

const ChatBubble = ({ onClick }) => {
  return (
    <div
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '60px',
        height: '60px',
        borderRadius: '50%',
        backgroundColor: '#007bff',
        color: 'white',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
        boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        fontSize: '24px',
      }}
      onClick={onClick}
    >
      💬
    </div>
  );
};

export default ChatBubble;