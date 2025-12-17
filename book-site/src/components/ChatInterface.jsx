import React, { useState, useRef, useEffect } from 'react';
import ChatInput from './ChatInput';
import { ChatConfig } from '../config/chat-config';


const ChatInterface = ({ threadId, selectedText }) => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const sendMessage = async (text, selectedTextInput) => {
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      // Use the passed selectedText parameter or the one from props
      const actualSelectedText = selectedTextInput !== undefined ? selectedTextInput : selectedText;

      // Determine which endpoint to use based on whether selectedText is provided
      const endpoint = actualSelectedText
        ? `${ChatConfig.API_BASE_URL}/api/v1/chat/selected-text`
        : `${ChatConfig.API_BASE_URL}/api/v1/chat`;

      const requestBody = {
        message: text, // Changed from 'query' to 'message'
        thread_id: threadId,
      };

      // Only add selected_text if it exists and we're using the selected-text endpoint
      if (actualSelectedText) {
        requestBody.selected_text = actualSelectedText;
      }

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: 'system', content: data.answer || 'No response.' },
      ]);
    } catch (err) {
      console.error('Chat API error:', err);
      setMessages((prev) => [
        ...prev,
        { role: 'system', content: '⚠️ Error talking to assistant.' },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            Ask questions about this chapter 📘
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}

        {isTyping && (
          <div className="chat-message system typing-indicator">
            <span></span><span></span><span></span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ✅ INPUT FIELD IS HERE */}
      <ChatInput onSendMessage={sendMessage} selectedText={selectedText} />
    </>
  );
};

export default ChatInterface;
