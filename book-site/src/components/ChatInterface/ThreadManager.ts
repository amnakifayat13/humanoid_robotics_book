// ThreadManager service for browser storage operations
import { ThreadStorage, Message } from './types';
import { generateUUID } from './UUID';

const THREAD_STORAGE_KEY = 'humanoid_robotics_chat_thread';
const THREAD_TIMEOUT = process.env.REACT_APP_DEFAULT_THREAD_TIMEOUT
  ? parseInt(process.env.REACT_APP_DEFAULT_THREAD_TIMEOUT)
  : 86400000; // 24 hours in milliseconds

class ThreadManager {
  // Get the current thread from storage
  getThread(): ThreadStorage | null {
    try {
      const stored = localStorage.getItem(THREAD_STORAGE_KEY);
      if (!stored) {
        return null;
      }

      const thread: ThreadStorage = JSON.parse(stored);

      // Check if thread is expired
      const now = new Date().getTime();
      const lastActivity = new Date(thread.last_activity).getTime();
      if (now - lastActivity > THREAD_TIMEOUT) {
        this.clearThread();
        return null;
      }

      return thread;
    } catch (error) {
      console.error('Error retrieving thread from storage:', error);
      return null;
    }
  }

  // Save a thread to storage
  saveThread(thread: ThreadStorage): boolean {
    try {
      // Check if storage quota is exceeded
      localStorage.setItem(THREAD_STORAGE_KEY, JSON.stringify(thread));
      return true;
    } catch (error) {
      if (error instanceof DOMException && (error.name === 'QuotaExceededError' || error.name === 'NS_ERROR_DOM_QUOTA_REACHED')) {
        console.error('Storage quota exceeded. Clearing old thread data.');
        this.clearThread();
        return false;
      }
      console.error('Error saving thread to storage:', error);
      return false;
    }
  }

  // Create a new thread
  createThread(): ThreadStorage {
    const threadId = generateUUID();
    const now = new Date().toISOString();

    const newThread: ThreadStorage = {
      thread_id: threadId,
      created_at: now,
      last_activity: now,
      messages: [],
    };

    this.saveThread(newThread);
    return newThread;
  }

  // Add a message to the current thread
  addMessage(message: Message): boolean {
    const thread = this.getThread() || this.createThread();

    // Update the thread with the new message
    thread.messages.push(message);
    thread.last_activity = new Date().toISOString();

    return this.saveThread(thread);
  }

  // Update the last activity timestamp
  updateLastActivity(): boolean {
    const thread = this.getThread();
    if (!thread) {
      return false;
    }

    thread.last_activity = new Date().toISOString();
    return this.saveThread(thread);
  }

  // Clear the current thread from storage
  clearThread(): void {
    try {
      localStorage.removeItem(THREAD_STORAGE_KEY);
    } catch (error) {
      console.error('Error clearing thread from storage:', error);
    }
  }

  // Get all messages for the current thread
  getMessages(): Message[] {
    const thread = this.getThread();
    return thread ? thread.messages : [];
  }

  // Check if storage is available
  isStorageAvailable(): boolean {
    try {
      const test = '__storage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (e) {
      return false;
    }
  }
}

export default new ThreadManager();