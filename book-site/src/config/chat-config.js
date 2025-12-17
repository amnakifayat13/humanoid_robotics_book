/**
 * Chat Configuration Module
 * Browser-safe version for React / Docusaurus.
 * Environment variables should be prefixed with REACT_APP_ in .env
 */

const getEnv = (key, defaultValue) => {
  if (typeof process !== 'undefined' && process.env?.[key] !== undefined) {
    return process.env[key];
  }
  // fallback for browser (window.__env__ or default)
  if (typeof window !== 'undefined' && window.__env__?.[key] !== undefined) {
    return window.__env__[key];
  }
  return defaultValue;
};

export const ChatConfig = {
  API_BASE_URL: getEnv('REACT_APP_DEPLOYED_URL', 'https://humanoid-robotics-book-994461288184.us-central1.run.app'),

  MAX_HISTORY: parseInt(getEnv('REACT_APP_MAX_HISTORY', '50'), 10),
  REQUEST_TIMEOUT: parseInt(getEnv('REACT_APP_REQUEST_TIMEOUT', '30000'), 10),

  MAX_RETRY_ATTEMPTS: parseInt(getEnv('REACT_APP_MAX_RETRY_ATTEMPTS', '3'), 10),
  RETRY_DELAY: parseInt(getEnv('REACT_APP_RETRY_DELAY', '1000'), 10),

  ENABLE_TYPING_INDICATOR: getEnv('REACT_APP_ENABLE_TYPING_INDICATOR', 'true') !== 'false',
  ENABLE_MESSAGE_PERSISTENCE: getEnv('REACT_APP_ENABLE_MESSAGE_PERSISTENCE', 'true') !== 'false',

  MIN_SELECTED_TEXT_LENGTH: parseInt(getEnv('REACT_APP_MIN_SELECTED_TEXT_LENGTH', '10'), 10),
  MAX_SELECTED_TEXT_LENGTH: parseInt(getEnv('REACT_APP_MAX_SELECTED_TEXT_LENGTH', '1000'), 10),

  CHAT_WINDOW_WIDTH: getEnv('REACT_APP_CHAT_WINDOW_WIDTH', '400px'),
  CHAT_WINDOW_HEIGHT: getEnv('REACT_APP_CHAT_WINDOW_HEIGHT', '600px'),

  ENABLE_SELECTED_TEXT_FEATURE: getEnv('REACT_APP_ENABLE_SELECTED_TEXT_FEATURE', 'true') !== 'false',
  ENABLE_SOURCE_CITATIONS: getEnv('REACT_APP_ENABLE_SOURCE_CITATIONS', 'true') !== 'false',
};

// ---- Validation / Warnings ----
if (ChatConfig.MAX_HISTORY <= 0) {
  console.warn('[ChatConfig] MAX_HISTORY should be > 0, using default 50');
  ChatConfig.MAX_HISTORY = 50;
}

if (ChatConfig.MIN_SELECTED_TEXT_LENGTH < 0) {
  console.warn('[ChatConfig] MIN_SELECTED_TEXT_LENGTH should be >= 0, using default 10');
  ChatConfig.MIN_SELECTED_TEXT_LENGTH = 10;
}

if (ChatConfig.MAX_SELECTED_TEXT_LENGTH < ChatConfig.MIN_SELECTED_TEXT_LENGTH) {
  console.warn(
    '[ChatConfig] MAX_SELECTED_TEXT_LENGTH < MIN_SELECTED_TEXT_LENGTH, adjusting'
  );
  ChatConfig.MAX_SELECTED_TEXT_LENGTH = ChatConfig.MIN_SELECTED_TEXT_LENGTH * 100;
}

// ✅ Optional runtime helper
export const isApiUrlConfigured = () => {
  if (!ChatConfig.API_BASE_URL) {
    console.warn(
      '[ChatConfig] REACT_APP_DEPLOYED_URL is missing, chat may not work properly.'
    );
    return false;
  }
  return true;
};
