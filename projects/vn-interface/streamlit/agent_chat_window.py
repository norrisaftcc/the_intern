import streamlit as st
import openai
import json
import os
import datetime
import random
import pathlib
from dotenv import load_dotenv
from avatar_svg import generate_avatar_svg

# Load environment variables
load_dotenv()

# Load character prompts
def load_character_prompts():
    try:
        prompt_file = pathlib.Path(__file__).parent / "character_prompts.json"
        if prompt_file.exists():
            with open(prompt_file, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading character prompts: {e}")
        return {}

# Set page configuration
st.set_page_config(
    page_title="CSI Agent Chat Window",
    page_icon="🕵️",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_state' not in st.session_state:
    st.session_state.current_state = "default"
if 'emotion_intensity' not in st.session_state:
    st.session_state.emotion_intensity = 0.7
if 'emote_log' not in st.session_state:
    st.session_state.emote_log = []
if 'fork_type' not in st.session_state:
    st.session_state.fork_type = "Alpha"
if 'api_key_confirmed' not in st.session_state:
    st.session_state.api_key_confirmed = False
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = ""
if 'character_name' not in st.session_state:
    st.session_state.character_name = "Kai 'Circuit' Chen"
if 'character_type' not in st.session_state:
    st.session_state.character_type = "circuit"
if 'openai_api_key' not in st.session_state:
    # Try to get API key from environment variables or secrets
    api_key = os.getenv("OPENAI_API_KEY", "")
    # Check for Streamlit secrets
    if not api_key and hasattr(st, "secrets") and "api_keys" in st.secrets:
        api_key = st.secrets["api_keys"].get("openai", "")
    st.session_state.openai_api_key = api_key

# Define avatar states
AVATAR_STATES = {
    "default": {
        "color": "#4A90E2",
        "emoji": "🔍",
        "description": "Ready to investigate"
    },
    "thinking": {
        "color": "#1E90FF",
        "emoji": "🧐",
        "description": "Deep in thought"
    },
    "excited": {
        "color": "#9370DB",
        "emoji": "⚡",
        "description": "Circuit patterns pulsing"
    },
    "teaching": {
        "color": "#20B2AA",
        "emoji": "📊",
        "description": "Projecting holographics"
    },
    "confused": {
        "color": "#FF7F50",
        "emoji": "❓",
        "description": "Processing information"
    },
    "success": {
        "color": "#32CD32", 
        "emoji": "🎯",
        "description": "Investigation success"
    }
}

# Function to extract emotes
def extract_emotes(message):
    emote_start = message.find("[*")
    emote_end = message.find("*]")
    
    emotes = []
    clean_message = message
    
    while emote_start != -1 and emote_end != -1:
        emote_text = message[emote_start+2:emote_end]
        emotes.append(emote_text)
        
        clean_message = clean_message.replace(f"[*{emote_text}*]", "")
        
        message = message[emote_end+2:]
        emote_start = message.find("[*")
        emote_end = message.find("*]")
    
    return clean_message.strip(), emotes

# Function to determine avatar state from emotes
def determine_avatar_state(emotes):
    if not emotes:
        return "default"
    
    emote_text = " ".join(emotes).lower()
    
    if "glasses" in emote_text or "thinking" in emote_text:
        return "thinking"
    elif "circuit" in emote_text or "excite" in emote_text:
        return "excited"
    elif "holographic" in emote_text or "projection" in emote_text or "teach" in emote_text:
        return "teaching"
    elif "confused" in emote_text or "processing" in emote_text or "puzzled" in emote_text:
        return "confused"
    elif "fedora" in emote_text or "satisfied" in emote_text or "solved" in emote_text:
        return "success"
    else:
        return "default"

# Function to render avatar
def render_avatar():
    state = st.session_state.current_state
    intensity = st.session_state.emotion_intensity
    fork_type = st.session_state.fork_type
    character_type = st.session_state.character_type
    state_data = AVATAR_STATES[state]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Generate SVG avatar
        svg = generate_avatar_svg(
            state=state,
            fork_type=fork_type,
            intensity=intensity,
            character_type=character_type
        )
        
        # Display the avatar
        st.components.v1.html(svg, height=400)
        
        # Display character info below the avatar
        st.markdown(
            f"""
            <div style="
                text-align: center;
                margin-top: 10px;
                padding: 10px;
                background-color: {state_data["color"]}30;
                border-radius: 5px;
            ">
                <h3 style="margin: 0; color: {state_data["color"]};">{st.session_state.character_name}</h3>
                <p style="margin: 0; font-style: italic; color: {state_data["color"]};">{state_data["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return col2

# Display the emote log in the sidebar
def show_emote_log():
    st.sidebar.title("Character Actions")
    
    if not st.session_state.emote_log:
        st.sidebar.caption("No actions recorded yet.")
        return
    
    for emote in st.session_state.emote_log:
        state_color = AVATAR_STATES[emote.get('state', 'default')]['color']
        st.sidebar.markdown(
            f"""
            <div style="
                margin-bottom: 8px;
                padding: 8px;
                border-radius: 5px;
                background-color: {state_color}20;
                border-left: 3px solid {state_color};
            ">
                <small>{emote['timestamp']}</small><br>
                [*{emote['action']}*]
            </div>
            """,
            unsafe_allow_html=True
        )

# Function to set up the OpenAI client
def setup_openai_client():
    api_key = st.session_state.openai_api_key
    
    if not api_key:
        return None
        
    try:
        client = openai.OpenAI(api_key=api_key)
        # Test connection
        models = client.models.list(limit=1)
        return client
    except Exception as e:
        st.error(f"Error connecting to OpenAI API: {str(e)}")
        return None

# Function to generate response from API
def generate_api_response(client, messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # You can change to an appropriate model
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "[*looks confused*] I'm having trouble connecting right now. Could you try again?"

# Function to create conversation history for API
def create_conversation_history():
    # Start with system prompt
    conversation = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]
    
    # Add message history
    for message in st.session_state.messages:
        conversation.append({
            "role": message["role"],
            "content": message["content"]
        })
    
    return conversation

# Process user message and get agent response
def process_message(user_input):
    if not user_input.strip():
        return
    
    # Extract emotes from user message
    clean_message, user_emotes = extract_emotes(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input
    })
    
    # Add user emotes to log if present
    for emote in user_emotes:
        state = determine_avatar_state([emote])
        st.session_state.emote_log.insert(0, {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "action": emote,
            "state": state
        })
    
    # Create conversation history for API
    conversation = create_conversation_history()
    
    # Get response from API
    client = setup_openai_client()
    if client:
        response = generate_api_response(client, conversation)
    else:
        # Demo mode if no API key
        response = "[*adjusts glasses*] I'm in demo mode since there's no API connection. I can demonstrate the interface, but not provide real AI responses."
    
    # Extract emotes from API response
    clean_response, ai_emotes = extract_emotes(response)
    
    # Add to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })
    
    # Update avatar state based on AI emotes
    if ai_emotes:
        new_state = determine_avatar_state(ai_emotes)
        st.session_state.current_state = new_state
        
        # Add AI emotes to log
        for emote in ai_emotes:
            st.session_state.emote_log.insert(0, {
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "action": emote,
                "state": new_state
            })
        
        # Set random intensity for some variation
        st.session_state.emotion_intensity = random.uniform(0.6, 0.9)

# Configure settings
def configure_settings():
    st.sidebar.title("Agent Settings")
    
    # API Key setup
    with st.sidebar.expander("API Connection", expanded=not st.session_state.api_key_confirmed):
        api_key = st.text_input("OpenAI API Key", 
                               type="password", 
                               placeholder="sk-...",
                               help="Enter your OpenAI API key. This stays in your browser and is never sent to our servers.")
        
        if api_key:
            st.session_state.openai_api_key = api_key
            if st.button("Confirm API Key"):
                client = setup_openai_client()
                if client:
                    st.session_state.api_key_confirmed = True
                    st.success("API connection confirmed!")
                else:
                    st.error("Could not validate API key.")
        
        demo_mode = st.checkbox("Use Demo Mode (No API)", 
                              help="Run with mock responses instead of API calls.")
        
        if demo_mode:
            st.session_state.api_key_confirmed = True
    
    # Character settings
    with st.sidebar.expander("Character Settings", expanded=False):
        # Load available character prompts
        character_prompts = load_character_prompts()
        
        if character_prompts:
            characters = ["Custom"] + list(character_prompts.keys())
            selected_character = st.selectbox(
                "Character Template", 
                characters,
                help="Select a predefined character or create a custom one."
            )
            
            if selected_character != "Custom" and selected_character in character_prompts:
                # Load character data
                char_data = character_prompts[selected_character]
                if st.button(f"Load {char_data['name']}"):
                    st.session_state.character_name = char_data["name"]
                    st.session_state.system_prompt = char_data["system_prompt"]
                    
                    # Set character type based on selected character
                    if selected_character == "kai":
                        st.session_state.character_type = "circuit"
                    elif selected_character == "teacherbot":
                        st.session_state.character_type = "teacherbot"
                    elif selected_character == "debug_whiz":
                        st.session_state.character_type = "debug_whiz"
                    
                    st.session_state.messages.append({
                        "role": "system", 
                        "content": f"[Character switched to {char_data['name']}]"
                    })
                    st.success(f"Loaded {char_data['name']} character profile!")
                    
                    # Show example emotes
                    if "emotes" in char_data:
                        st.caption("Example emotes:")
                        for emote in char_data["emotes"][:3]:
                            st.code(emote)
        
        # Custom character settings
        character_name = st.text_input("Character Name", 
                                      value=st.session_state.character_name)
        if character_name and character_name != st.session_state.character_name:
            st.session_state.character_name = character_name
            st.session_state.messages.append({
                "role": "system", 
                "content": f"[Character name changed to {character_name}]"
            })
        
        # Character type selection
        char_type_options = {
            "circuit": "Cyberpunk Detective (Kai)",
            "teacherbot": "Educational Assistant",
            "debug_whiz": "Debugging Specialist"
        }
        
        selected_char_type = st.selectbox(
            "Avatar Style",
            options=list(char_type_options.keys()),
            index=list(char_type_options.keys()).index(st.session_state.character_type) 
                if st.session_state.character_type in char_type_options else 0,
            format_func=lambda x: char_type_options[x],
            help="Select the visual style for your agent's avatar"
        )
        
        if selected_char_type != st.session_state.character_type:
            st.session_state.character_type = selected_char_type
        
        # Fork type selection
        fork_options = ["Alpha", "Beta", "Gamma"]
        fork_type = st.selectbox(
            "Fork Type", 
            fork_options, 
            index=fork_options.index(st.session_state.fork_type),
            help="Fork types represent different agent capabilities."
        )
        
        if fork_type != st.session_state.fork_type:
            st.session_state.fork_type = fork_type
            st.session_state.messages.append({
                "role": "system", 
                "content": f"[Switching to {fork_type} Fork]"
            })
    
    # System prompt settings
    with st.sidebar.expander("System Prompt", expanded=False):
        system_prompt = st.text_area("System Prompt", 
                                    value=st.session_state.system_prompt or 
                                    f"You are {st.session_state.character_name}, a cyberpunk detective and AI programming expert. You're helping users solve coding mysteries and technical problems. You use [*emote actions*] to express yourself.")
        
        if st.button("Update System Prompt"):
            st.session_state.system_prompt = system_prompt
            st.success("System prompt updated!")
    
    # Test emotes
    with st.sidebar.expander("Test Emotes", expanded=False):
        st.caption("Click to test different avatar emotional states")
        emote_cols = st.columns(3)
        
        if emote_cols[0].button("Thinking"):
            st.session_state.current_state = "thinking"
            st.session_state.emotion_intensity = 0.7
        if emote_cols[1].button("Excited"):
            st.session_state.current_state = "excited"
            st.session_state.emotion_intensity = 0.9
        if emote_cols[2].button("Teaching"):
            st.session_state.current_state = "teaching"
            st.session_state.emotion_intensity = 0.8
    
    # Chat controls
    with st.sidebar.expander("Chat Controls", expanded=False):
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.emote_log = []
            st.session_state.current_state = "default"
            st.success("Chat history cleared!")
        
        st.download_button(
            "Export Chat History",
            data=json.dumps({
                "messages": st.session_state.messages,
                "emote_log": st.session_state.emote_log
            }, indent=2),
            file_name=f"csi_chat_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        uploaded_file = st.file_uploader("Import Chat History", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.session_state.messages = data.get("messages", [])
                st.session_state.emote_log = data.get("emote_log", [])
                st.success("Chat history imported successfully!")
            except Exception as e:
                st.error(f"Error importing chat history: {e}")

# Main application
def main():
    st.title("CSI Agent Chat Window")
    
    # Configure settings
    configure_settings()
    
    # Show emote log in sidebar
    show_emote_log()
    
    # Render avatar and get content column
    content_col = render_avatar()
    
    # Display chat history
    with content_col:
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "system":
                    st.markdown(
                        f"<div style='text-align:center; color:gray; padding: 5px;'>{message['content']}</div>", 
                        unsafe_allow_html=True
                    )
                else:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Type your message (use [*emotes*] for actions)...")
        if user_input:
            process_message(user_input)
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:gray;'>CSI Agent Chat Window | Creative Solutions Investigation | v0.1</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()