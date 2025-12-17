# Quickstart: Frontend ChatKit Integration

## Overview
This guide will help you set up and run the ChatKit integration for the Docusaurus documentation site. The integration provides a chat interface on every documentation page that connects to your RAG-powered backend.

## Prerequisites
- Node.js 18+ installed
- Access to the backend API with endpoints at `/api/v1/chat` and `/api/v1/chat/selected-text`
- Docusaurus 2.x project set up in the `book-site` directory

## Installation Steps

### 1. Install Dependencies
```bash
cd book-site
npm install @openai/chatkit
```

### 2. Create Chat Components
Create the following directory structure:
```
book-site/src/components/BookChatbot/
├── BookChatbot.jsx
├── ChatInterface.jsx
├── ChatMessage.jsx
└── ChatInput.jsx
```

### 3. Configure API Connection
Update the chat components to connect to your backend API endpoints:
- Full documentation queries: `POST /api/v1/chat`
- Selected text queries: `POST /api/v1/chat/selected-text`

### 4. Integrate with Docusaurus Layout
Override the default Docusaurus layout by creating:
```
book-site/src/theme/Layout/index.jsx
```

This component should wrap the default layout and inject the BookChatbot component.

## Running the Application
```bash
cd book-site
npm start
```

The documentation site will be available at http://localhost:3000 with the chat interface available on all pages.

## Key Configuration Options
- `API_BASE_URL`: Base URL for backend API calls
- `CHAT_MODEL`: Model identifier for the chat interface (if needed)
- `MAX_HISTORY`: Maximum number of messages to maintain in conversation history

## Testing
1. Visit any documentation page
2. Verify the chat interface appears
3. Test sending a message and receiving a response
4. Test the selected text functionality by selecting text and asking a question
5. Navigate between pages to verify conversation persistence

## Troubleshooting
- If the chat interface doesn't appear, verify the layout override is properly implemented
- If API calls fail, check the backend endpoint configuration
- If conversation state doesn't persist, verify localStorage permissions and implementation