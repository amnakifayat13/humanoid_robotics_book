// TypeScript type definitions for the chat interface based on the data model

export interface Message {
  message_id: string;
  thread_id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string; // ISO 8601 datetime
  status: 'sent' | 'delivered' | 'error';
}

export interface Thread {
  thread_id: string;
  created_at: string; // ISO 8601 datetime
  last_activity: string; // ISO 8601 datetime
  metadata: Record<string, any>; // Additional thread-specific data
}

export interface ChatRequest {
  message: string;
  thread_id?: string; // Optional for new threads
}

export interface SelectedTextChatRequest {
  message: string;
  selected_text: string;
  thread_id?: string; // Optional for new threads
}

export interface ChatResponse {
  answer: string;
  thread_id: string;
  sources?: Array<{
    text: string;
    score: number;
    metadata: Record<string, any>;
  }>;
}

export interface ErrorResponse {
  error: string;
  message: string;
}

export interface ThreadStorage {
  thread_id: string;
  created_at: string;
  last_activity: string;
  messages: Message[];
}