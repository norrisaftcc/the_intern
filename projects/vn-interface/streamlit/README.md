# CSI Visual Novel Interface - Streamlit Prototype

A proof of concept for the CSI Visual Novel interface using Streamlit instead of Gradio.

## Features

- Interactive avatar that changes state based on emotes
- Chat interface with emote support using `[*action*]` syntax
- Emote log sidebar that tracks character actions
- Fork type selection (Alpha, Beta, Gamma)
- Test emote buttons to see different avatar states
- Simple AI responses based on keywords

## Running the App

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run vn_interface_poc.py
   ```

3. The app will launch in your default web browser at http://localhost:8501

## Usage Tips

- Type messages in the chat input at the bottom
- Include emotes in your messages using the format: `[*adjusts glasses*]`
- Try keywords like "github", "python", or "csi" to see different responses
- Use the sidebar to change fork types or test different emotes
- Watch the emote log in the sidebar to see a history of character actions

## Implementation Notes

This prototype demonstrates:
- Dynamic avatar changes based on character emotion
- Emote extraction and processing
- Chat history with different message types
- Interactive UI elements for testing
- Simple response generation based on keywords