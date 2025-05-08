# CSI Agent Chat Window - API Setup Guide

This guide explains how to set up API keys for the CSI Agent Chat Window, both for local development and when deploying to Streamlit Community Cloud.

## Local Development Setup

### 1. Get an OpenAI API Key

1. Create an account at [OpenAI's platform](https://platform.openai.com/) if you don't already have one
2. Navigate to the [API Keys section](https://platform.openai.com/api-keys)
3. Click "Create new secret key"
4. Copy the generated API key (it starts with "sk-")

### 2. Set Up Local Environment Variables

There are two ways to add your API key locally:

#### Option A: Using a .env file (recommended for development)

1. Create a file named `.env` in the `/projects/vn-interface/streamlit/` directory
2. Add your OpenAI API key to the file:
   ```
   OPENAI_API_KEY=sk-your_api_key_here
   ```
3. The application will automatically load this key using the `python-dotenv` package

#### Option B: Enter API key in the application UI

1. Run the application
2. In the sidebar, expand the "API Connection" section
3. Enter your OpenAI API key in the password field
4. Click "Confirm API Key"

## Streamlit Community Cloud Setup

When deploying to Streamlit Community Cloud, you'll need to set up secrets:

1. Create a file named `.streamlit/secrets.toml` in your repository with:
   ```toml
   [api_keys]
   openai = "sk-your_api_key_here"
   ```

2. In the Streamlit Community Cloud dashboard:
   - Go to your app settings
   - Click on "Secrets"
   - Add the same content as above

3. Update the application code to access secrets:
   ```python
   # In agent_chat_window.py
   if 'openai_api_key' not in st.session_state:
       st.session_state.openai_api_key = st.secrets["api_keys"]["openai"] if "api_keys" in st.secrets else ""
   ```

## Using Demo Mode (No API Key)

If you don't have an API key or want to test the application without making API calls:

1. Run the application
2. In the sidebar, expand the "API Connection" section
3. Check the "Use Demo Mode (No API)" option
4. The application will use mock responses instead of making actual API calls

## Troubleshooting

### API Connection Issues

- **Error: "Authentication Error"**: Your API key may be invalid or expired. Generate a new key.
- **Error: "Insufficient Quota"**: Your account may be out of credits. Check your usage on the OpenAI dashboard.
- **No API key visible in GitHub**: For security, NEVER commit your API key to GitHub. Use `.env` files and secrets instead.

### Security Notes

- Never share your API key publicly
- Don't commit your `.env` file or `.streamlit/secrets.toml` to version control
- Add these files to your `.gitignore`
- Rotate your API keys periodically

## Testing the Avatar System Only

If you only want to test the avatar visualization system without API integration:

```bash
cd projects/vn-interface/streamlit
streamlit run avatar_test.py
```

The avatar test application doesn't require any API keys and allows you to explore all the visual features of the agent chat window.