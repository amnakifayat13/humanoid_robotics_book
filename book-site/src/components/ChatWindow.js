import React from 'react';

const ChatWindow = ({ messages, onClose }) => {
  return (
    <div
      style={{
        position: 'fixed',
        bottom: '90px',
        right: '20px',
        width: '350px',
        height: '400px',
        backgroundColor: 'white',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          padding: '10px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>Chatbot</span>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'white', fontSize: '20px', cursor: 'pointer' }}>
          &times;
        </button>
      </div>
      <div style={{ flexGrow: 1, padding: '10px', overflowY: 'auto' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '10px', textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <span
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '15px',
                backgroundColor: msg.sender === 'user' ? '#e0f7fa' : '#f1f0f0',
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div style={{ padding: '10px', borderTop: '1px solid #eee' }}>
        {/* Input will go here later */}
        Type your message...
      </div>
    </div>
  );
};

export default ChatWindow;