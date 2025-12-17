# Data Model: Frontend ChatKit Integration

## Entity: Conversation Thread
**Description**: Represents a continuous conversation with a unique identifier, containing a sequence of user messages and system responses

**Fields**:
- `threadId` (string): Unique identifier for the conversation thread, used for persistence across page navigation
- `messages` (array): Collection of chat messages in chronological order
- `createdAt` (timestamp): When the conversation was initiated
- `lastActiveAt` (timestamp): When the last message was exchanged
- `isActive` (boolean): Whether the conversation is currently active

**Validation Rules**:
- threadId must be a valid UUID or string identifier
- messages array must not exceed maximum size to prevent memory issues
- createdAt and lastActiveAt must be valid timestamps

## Entity: Chat Message
**Description**: Individual communication unit containing the message content, timestamp, sender type (user/system), and metadata

**Fields**:
- `id` (string): Unique identifier for the message
- `content` (string): The actual message text content
- `sender` (enum): Either "user" or "system" indicating message origin
- `timestamp` (timestamp): When the message was sent/received
- `status` (enum): "sending", "sent", "received", "error" for UI state management
- `metadata` (object): Additional information like source citations for system responses

**Validation Rules**:
- content must not be empty or exceed maximum character limit
- sender must be either "user" or "system"
- timestamp must be a valid timestamp
- status must be one of the defined enum values

## Entity: Selected Text Context
**Description**: Additional information about user-selected content that constrains the scope of responses

**Fields**:
- `text` (string): The actual selected text content
- `sourcePage` (string): URL or identifier of the page where text was selected
- `selectionBounds` (object): Position information for the selected text (start/end indices)
- `timestamp` (timestamp): When the text was selected

**Validation Rules**:
- text must not be empty when this context is used
- sourcePage must be a valid page identifier from the documentation site
- timestamp must be a valid timestamp

## Relationships
- One Conversation Thread contains many Chat Messages (one-to-many)
- One Chat Message may have zero or one Selected Text Context (one-to-zero-or-one)

## State Transitions

### Conversation Thread States:
1. **New**: Thread created but no messages exchanged
2. **Active**: Messages are being exchanged
3. **Paused**: User navigated away but thread still exists in memory
4. **Archived**: Thread completed or exceeded time limits

### Chat Message States:
1. **Sending**: Message submitted but not yet confirmed by backend
2. **Sent**: Message confirmed sent to backend
3. **Received**: Response received from backend
4. **Error**: Message failed to send or receive properly

## API Data Contracts

### Request: Send Message
```
{
  "message": "User's question or message",
  "threadId": "optional existing thread ID",
  "selectedText": "optional selected text context"
}
```

### Response: Message Reply
```
{
  "answer": "System's response",
  "threadId": "ID of the conversation thread",
  "sources": ["optional list of source documents used"]
}
```

### Request: Selected Text Query
```
{
  "message": "User's question about selected text",
  "selectedText": "The text that was selected",
  "threadId": "optional existing thread ID"
}
```

### Response: Selected Text Reply
```
{
  "answer": "System's response based only on selected text",
  "threadId": "ID of the conversation thread"
}
```