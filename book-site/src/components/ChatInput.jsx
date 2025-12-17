import React, { useState, useRef, useEffect } from 'react';

const ChatInput = ({ onSendMessage, selectedText }) => {
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (selectedText) {
      setInputValue(`Regarding:\n"${selectedText}"\n\nQuestion: `);
      textareaRef.current?.focus();
    }
  }, [selectedText]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    setIsProcessing(true);

    try {
      await onSendMessage(inputValue, selectedText);
      setInputValue('');
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 140) + 'px';
    }
  }, [inputValue]);

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <div className="chat-input-container">
        <textarea
          ref={textareaRef}
          placeholder="Ask about this book..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isProcessing}
          rows={1}
        />
        <button type="submit" className="send-button" disabled={isProcessing}>
          {isProcessing ? '…' : '→'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
