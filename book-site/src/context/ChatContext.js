import React, { createContext, useContext, useReducer } from 'react';

// Initial state for the chat context
const initialState = {
  messages: [],
  threadId: null,
  isLoading: false,
  selectedText: null,
  error: null,
};

// Action types
const actionTypes = {
  SET_THREAD_ID: 'SET_THREAD_ID',
  ADD_MESSAGE: 'ADD_MESSAGE',
  UPDATE_MESSAGE_STATUS: 'UPDATE_MESSAGE_STATUS',
  SET_LOADING: 'SET_LOADING',
  SET_SELECTED_TEXT: 'SET_SELECTED_TEXT',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  CLEAR_MESSAGES: 'CLEAR_MESSAGES',
  SET_MESSAGES: 'SET_MESSAGES',
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case actionTypes.SET_THREAD_ID:
      return {
        ...state,
        threadId: action.payload,
      };
    case actionTypes.ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };
    case actionTypes.UPDATE_MESSAGE_STATUS:
      return {
        ...state,
        messages: state.messages.map(message =>
          message.id === action.payload.messageId
            ? { ...message, status: action.payload.status }
            : message
        ),
      };
    case actionTypes.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    case actionTypes.SET_SELECTED_TEXT:
      return {
        ...state,
        selectedText: action.payload,
      };
    case actionTypes.SET_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    case actionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case actionTypes.CLEAR_MESSAGES:
      return {
        ...state,
        messages: [],
      };
    case actionTypes.SET_MESSAGES:
      return {
        ...state,
        messages: action.payload,
      };
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const setThreadId = (threadId) => {
    dispatch({ type: actionTypes.SET_THREAD_ID, payload: threadId });
  };

  const addMessage = (message) => {
    dispatch({ type: actionTypes.ADD_MESSAGE, payload: message });
  };

  const updateMessageStatus = (messageId, status) => {
    dispatch({
      type: actionTypes.UPDATE_MESSAGE_STATUS,
      payload: { messageId, status }
    });
  };

  const setLoading = (isLoading) => {
    dispatch({ type: actionTypes.SET_LOADING, payload: isLoading });
  };

  const setSelectedText = (selectedText) => {
    dispatch({ type: actionTypes.SET_SELECTED_TEXT, payload: selectedText });
  };

  const setError = (error) => {
    dispatch({ type: actionTypes.SET_ERROR, payload: error });
  };

  const clearError = () => {
    dispatch({ type: actionTypes.CLEAR_ERROR });
  };

  const clearMessages = () => {
    dispatch({ type: actionTypes.CLEAR_MESSAGES });
  };

  const setMessages = (messages) => {
    dispatch({ type: actionTypes.SET_MESSAGES, payload: messages });
  };

  const value = {
    ...state,
    setThreadId,
    addMessage,
    updateMessageStatus,
    setLoading,
    setSelectedText,
    setError,
    clearError,
    clearMessages,
    setMessages,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

// Export action types for use in other files if needed
export { actionTypes };