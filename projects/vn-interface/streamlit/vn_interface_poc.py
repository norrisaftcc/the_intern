import streamlit as st
import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="CSI - Visual Novel Interface",
    page_icon="🕵️",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_emote' not in st.session_state:
    st.session_state.current_emote = "default"
if 'emotion_intensity' not in st.session_state:
    st.session_state.emotion_intensity = 0.5
if 'emote_log' not in st.session_state:
    st.session_state.emote_log = []
if 'fork_type' not in st.session_state:
    st.session_state.fork_type = "Alpha"

# Define avatar states and associated emotes
AVATAR_STATES = {
    "default": {
        "color": "#4A90E2",
        "emoji": "🤔",
        "description": "Kai is in detective mode, ready to investigate."
    },
    "thinking": {
        "color": "#1E90FF",
        "emoji": "🧐",
        "description": "Kai adjusts her glasses, deep in thought."
    },
    "excited": {
        "color": "#9370DB",
        "emoji": "✨",
        "description": "Kai's circuit patterns pulse with excitement!"
    },
    "teaching": {
        "color": "#20B2AA",
        "emoji": "👩‍🏫",
        "description": "Kai projects a holographic diagram as she explains."
    },
    "confused": {
        "color": "#FF7F50",
        "emoji": "❓",
        "description": "Kai tilts her head, processing the information."
    },
    "success": {
        "color": "#32CD32", 
        "emoji": "🎯",
        "description": "Kai tips her fedora in satisfaction!"
    }
}

# Function to extract emotes from message
def extract_emotes(message):
    # Simple emote extraction (anything between [* and *])
    emote_start = message.find("[*")
    emote_end = message.find("*]")
    
    emotes = []
    clean_message = message
    
    # Extract all emotes
    while emote_start != -1 and emote_end != -1:
        emote_text = message[emote_start+2:emote_end]
        emotes.append(emote_text)
        
        # Remove from clean message
        clean_message = clean_message.replace(f"[*{emote_text}*]", "")
        
        # Find next emote
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
    elif "circuit" in emote_text or "excitement" in emote_text or "excited" in emote_text:
        return "excited"
    elif "holographic" in emote_text or "diagram" in emote_text or "teaching" in emote_text:
        return "teaching"
    elif "confused" in emote_text or "processing" in emote_text:
        return "confused"
    elif "tips" in emote_text or "fedora" in emote_text or "satisfied" in emote_text:
        return "success"
    else:
        return "default"

# Function to render avatar
def render_avatar(state, intensity=0.5):
    state_data = AVATAR_STATES[state]
    
    # Adjust color based on intensity
    color = state_data["color"]
    
    # Calculate a brightness factor based on intensity
    brightness = int(100 + (intensity * 50))
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: {color}; 
                filter: brightness({brightness}%);
                padding: 20px; 
                border-radius: 10px; 
                text-align: center;
                animation: pulse 2s infinite;
            ">
                <h1 style="color: white; font-size: 3em; margin-bottom: 0;">{state_data["emoji"]}</h1>
                <h3 style="color: white; margin-top: 0;">Kai "Circuit" Chen</h3>
                <p style="color: white; font-style: italic;">{state_data["description"]}</p>
            </div>
            <style>
                @keyframes pulse {{
                    0% {{
                        transform: scale(1);
                    }}
                    50% {{
                        transform: scale(1.05);
                    }}
                    100% {{
                        transform: scale(1);
                    }}
                }}
            </style>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        # Most recent message
        if st.session_state.messages:
            last_message = st.session_state.messages[-1]
            st.markdown(
                f"""
                <div style="
                    background-color: {color}20; 
                    padding: 15px; 
                    border-radius: 10px; 
                    border-left: 5px solid {color};
                ">
                    <p>{last_message['content']}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# Display the emote log in the sidebar
def show_emote_log():
    st.sidebar.title("Character Actions")
    
    for emote in st.session_state.emote_log:
        st.sidebar.markdown(
            f"""
            <div style="
                margin-bottom: 8px;
                padding: 8px;
                border-radius: 5px;
                background-color: {AVATAR_STATES[emote['state']]['color']}20;
                border-left: 3px solid {AVATAR_STATES[emote['state']]['color']};
            ">
                <small>{emote['timestamp']}</small><br>
                [*{emote['action']}*]
            </div>
            """,
            unsafe_allow_html=True
        )

# Function to process user message
def process_message(message):
    if not message.strip():
        return
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Process for emotes
    clean_message, emotes = extract_emotes(message)
    
    # If user included emotes, add to log
    for emote in emotes:
        emote_state = determine_avatar_state([emote])
        st.session_state.emote_log.insert(0, {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "action": emote,
            "state": emote_state
        })
    
    # Simple AI response based on keywords
    response = generate_ai_response(clean_message)
    
    # Process AI response for emotes
    clean_response, ai_emotes = extract_emotes(response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Update avatar state based on AI emotes
    if ai_emotes:
        new_state = determine_avatar_state(ai_emotes)
        st.session_state.current_emote = new_state
        
        # Add to emote log
        for emote in ai_emotes:
            st.session_state.emote_log.insert(0, {
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "action": emote,
                "state": new_state
            })
        
        # Set random intensity
        st.session_state.emotion_intensity = random.uniform(0.3, 0.9)

# Simple AI response generation
def generate_ai_response(message):
    message_lower = message.lower()
    
    # GitHub lesson responses
    if "github" in message_lower:
        if "account" in message_lower or "sign up" in message_lower:
            return "[*adjusts glasses thoughtfully*] Let me guide you through creating a GitHub account. First, navigate to github.com and click the Sign Up button in the top-right corner."
        elif "repository" in message_lower or "repo" in message_lower:
            return "[*circuit patterns pulse with excitement*] Creating a repository is easy! Click the + icon in the top-right corner of GitHub and select 'New repository'. Give it a name and description, then click 'Create repository'."
        elif "clone" in message_lower:
            return "[*projects holographic command line*] To clone a repository, you'll need the repository URL. Then run `git clone [URL]` in your terminal. This will download a copy of the repository to your machine."
        else:
            return "[*tips fedora slightly*] GitHub is an essential tool for version control. What specific aspect would you like to learn about?"
    
    # Python responses
    elif "python" in message_lower:
        if "install" in message_lower:
            return "[*brings up holographic instructions*] To install Python, visit python.org and download the latest version for your operating system. Follow the installation instructions, and don't forget to check 'Add Python to PATH'!"
        elif "function" in message_lower:
            return "[*excitedly draws in the air*] Functions in Python are defined using the `def` keyword. Here's a simple example: `def greet(name): return f\"Hello, {name}!\"`"
        else:
            return "[*circuit patterns glow with enthusiasm*] Python is my favorite language! What would you like to know about it?"
    
    # CSI project responses
    elif "csi" in message_lower or "creative solutions" in message_lower:
        return "[*holographic circuits intensify*] Creative Solutions Investigation is our framework for reimagining software development teams as investigative units. We use Python-based archive systems, Flask interfaces, and fork communication protocols!"
    
    # Default responses
    elif "hello" in message_lower or "hi" in message_lower:
        return "[*tips fedora*] Hello there! Kai 'Circuit' Chen at your service. How can I help with your investigation today?"
    elif "help" in message_lower:
        return "[*adjusts hoodie*] I'd be happy to help! I can guide you through GitHub basics, Python programming, or tell you about our CSI project. What would you like to know?"
    elif "thank" in message_lower:
        return "[*circuit patterns glow warmly*] You're welcome! Always happy to help a fellow investigator."
    else:
        return "[*taps chin thoughtfully*] Interesting... Tell me more about that, or ask me about GitHub, Python, or the CSI project."

# Main app layout
st.title("CSI - Visual Novel Interface")

# Fork type selector in sidebar
st.sidebar.title("Debug Options")
fork_options = ["Alpha", "Beta", "Gamma"]
selected_fork = st.sidebar.selectbox("Fork Type", fork_options, index=fork_options.index(st.session_state.fork_type))

if selected_fork != st.session_state.fork_type:
    st.session_state.fork_type = selected_fork
    # Add a system message about fork change
    st.session_state.messages.append({
        "role": "system", 
        "content": f"[Switching to {selected_fork} Fork]"
    })

# Manual emote testing in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Test Emotes")
emote_cols = st.sidebar.columns(3)

if emote_cols[0].button("Thinking"):
    st.session_state.current_emote = "thinking"
    st.session_state.emotion_intensity = 0.7
if emote_cols[1].button("Excited"):
    st.session_state.current_emote = "excited"
    st.session_state.emotion_intensity = 0.9
if emote_cols[2].button("Teaching"):
    st.session_state.current_emote = "teaching"
    st.session_state.emotion_intensity = 0.8

# Emote log in sidebar
st.sidebar.markdown("---")
show_emote_log()

# Main display area
render_avatar(st.session_state.current_emote, st.session_state.emotion_intensity)

# Chat history
st.markdown("### Conversation")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "system":
            st.markdown(f"<div style='text-align:center; color:gray; padding: 5px;'>{message['content']}</div>", unsafe_allow_html=True)
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
st.markdown(f"<div style='text-align:center; color:gray;'>CSI Visual Novel Interface | {st.session_state.fork_type} Fork | v0.1</div>", unsafe_allow_html=True)