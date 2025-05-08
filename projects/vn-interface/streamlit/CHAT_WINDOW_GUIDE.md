# CSI Agent Chat Window - Quick Start Guide

This application provides an interactive window for communicating with intelligent agents in the CSI universe, featuring visual novel style emotes and character representations.

## Setting Up

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file (optional) with your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. Run the application:
   ```bash
   streamlit run agent_chat_window.py
   ```

## Features

### API Integration
- **OpenAI API Connection**: Connect to OpenAI's API by providing your API key
- **Demo Mode**: Test the interface without an API key using mock responses

### Character Customization
- **Character Selection**: Choose from predefined characters or create your own
- **Fork Classification**: Select between Alpha, Beta, and Gamma forks with different capabilities
- **System Prompt**: Customize the agent's behavior with detailed instructions

### Visual Novel Elements
- **Dynamic Avatar**: Character avatar changes based on emotions detected in messages
- **Emote Actions**: Use `[*action description*]` syntax to trigger character animations
- **Emote Log**: Sidebar tracks all character actions for reference

### Chat Management
- **History Export/Import**: Save and load conversations as JSON files
- **Clear Chat**: Reset the conversation when needed
- **Fork Switching**: Change between fork types mid-conversation

## Using Emotes

Emotes are a core feature of the CSI Visual Novel interface. To use them:

1. In your messages, include text in the format `[*action description*]`
   ```
   [*leans forward*] Tell me more about that algorithm.
   ```

2. The agent will respond with its own emotes:
   ```
   [*adjusts glasses*] The quicksort algorithm works by selecting a 'pivot' element...
   ```

3. These emotes trigger avatar state changes and are logged in the sidebar

## Character Prompt Format

The `character_prompts.json` file contains predefined character profiles you can use or modify:

```json
{
  "character_id": {
    "name": "Character Name",
    "system_prompt": "Detailed instructions for the AI...",
    "emotes": [
      "[*example emote 1*]",
      "[*example emote 2*]"
    ]
  }
}
```

## Demo Without API Key

If you don't have an API key, check the "Use Demo Mode" option to test the interface with preset responses.

## Fork Types Explained

- **Alpha Fork**: Full capabilities, extensive knowledge base, persistent memory
- **Beta Fork**: Partial capabilities, focused knowledge, limited memory
- **Gamma Fork**: Basic personality, no specialized knowledge, session-only memory

## Troubleshooting

- **API Connection Issues**: Verify your API key is correct and has sufficient credits
- **Emote Detection Problems**: Ensure you're using the correct `[*action*]` syntax
- **Performance Issues**: Try reducing the conversation history by clearing chat