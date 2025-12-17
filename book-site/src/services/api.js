/**
 * API Service Module
 * Handles communication with backend chat API endpoints
 */

import { ChatConfig } from '../config/chat-config';

class ChatApiService {
  constructor() {
    this.baseURL = ChatConfig.API_BASE_URL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  // ✅ General chat
async sendMessage(message, threadId) {
  return this._makeRequest(`${this.baseURL}/api/v1/chat`, {
    message: message,
    thread_id: threadId
  });
}


  // ✅ Selected text chat
  async sendSelectedTextMessage(message, selectedText, threadId) {
  return this._makeRequest(`${this.baseURL}/api/v1/chat/selected-text`, {
    message: message,
    selected_text: selectedText,
    thread_id: threadId
  });
}

  async _makeRequest(url, body, attempt = 1) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch(url, {
        method: 'POST',
        headers: this.defaultHeaders,
        body: JSON.stringify(body),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout');
      }

      if (attempt < 3 && this._isRetryableError(error)) {
        await this._delay(Math.pow(2, attempt) * 1000);
        return this._makeRequest(url, body, attempt + 1);
      }

      throw error;
    }
  }

  _isRetryableError(error) {
    return error.message.includes('Failed to fetch') ||
           error.message.includes('timeout') ||
           error.message.includes('5');
  }

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const chatApi = new ChatApiService();
