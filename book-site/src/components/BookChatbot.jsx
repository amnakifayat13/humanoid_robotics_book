import React, { useState, useEffect } from 'react';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import ChatInterface from './ChatInterface';
import './BookChatbot.css';

const BookChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [threadId, setThreadId] = useState(null);
  const [selectedText, setSelectedText] = useState(null);

  useEffect(() => {
    if (!ExecutionEnvironment.canUseDOM) return;

    let id = localStorage.getItem('bookChatbot_threadId');
    if (!id) {
      id = `thread_${Date.now()}`;
      localStorage.setItem('bookChatbot_threadId', id);
    }
    setThreadId(id);

    const handleSelection = () => {
      const text = window.getSelection()?.toString().trim();
      if (text && text.length > 10) {
        setSelectedText(text);
        setIsOpen(true);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  if (!ExecutionEnvironment.canUseDOM) return null;

  return (
    <div className="book-chatbot-wrapper">
      <button className="book-chatbot-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '×' : '💬'}
      </button>

      {isOpen && (
        <div className="book-chatbot-container">
          <div className="book-chatbot-header">
            <h3>Assistant</h3>
            <button onClick={() => setIsOpen(false)}>×</button>
          </div>

          <div className="chat-interface">
            {threadId && (
              <ChatInterface
                threadId={threadId}
                selectedText={selectedText}
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default BookChatbot;
