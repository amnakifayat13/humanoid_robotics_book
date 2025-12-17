# Book Site with Chat Integration

This Docusaurus project includes an integrated chatbot that allows users to ask questions about the documentation content.

## Features

- **Global Chat Interface**: A chatbot is available on every documentation page
- **Full Documentation Search**: Ask questions about the entire book content
- **Selected Text Queries**: Select text on any page and ask specific questions about it
- **Persistent Conversations**: Conversation history is maintained across page navigation
- **Responsive Design**: Works on both desktop and mobile devices

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## How to Use

### Asking Questions
1. Click the chat button (💬) in the bottom-right corner of any page
2. Type your question in the input field at the bottom of the chat window
3. Press Enter or click the send button to submit your question

### Selected Text Queries
1. Select any text on a documentation page
2. The chat interface will automatically open with the selected text pre-filled
3. Ask your question about the selected content

### Managing Conversations
- Click "Clear Chat" to start a new conversation
- Your conversation history persists as you navigate between pages
- Close the chat window by clicking the × button

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
