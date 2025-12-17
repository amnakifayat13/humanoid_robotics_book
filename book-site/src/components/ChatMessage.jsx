import React from 'react';

/**
 * ChatMessage Component
 * Displays individual chat messages with proper formatting
 */
const ChatMessage = ({ message, sender }) => {
  const isUser = sender === 'user';

  return (
    <div className={`chat-message ${sender}`}>
      <div className="message-content">
        {message.content}
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <small>Sources: {message.sources.join(', ')}</small>
          </div>
        )}
      </div>
      <div className="message-timestamp">
        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default ChatMessage;