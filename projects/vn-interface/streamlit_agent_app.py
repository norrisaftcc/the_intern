import streamlit as st
import requests
import json
from datetime import datetime
import os

# --- App Configuration ---
st.set_page_config(page_title="Circuit - AI Detective", layout="wide")

# --- State Management ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'emotion_state' not in st.session_state:
    st.session_state.emotion_state = {
        'circuit_pattern': {
            'intensity': 0.5,
            'rhythm': 'steady',
            'color_shift': 'thoughtful'
        },
        'holographic_state': {
            'brightness': 0.7,
            'complexity': 0.5,
            'movement': 'stable'
        }
    }
if 'fork_id' not in st.session_state:
    st.session_state.fork_id = "alpha-main"

# --- UI Components ---
def render_avatar(emotion_state):
    """Render the avatar with current emotional state"""
    intensity = emotion_state['circuit_pattern']['intensity']
    color_shift = emotion_state['circuit_pattern']['color_shift']
    
    # Map color_shift to actual colors
    color_map = {
        'thoughtful': '#1E90FF',  # Blue
        'excitement': '#9370DB',  # Purple
        'amused': '#20B2AA',      # Teal
    }
    color = color_map.get(color_shift, '#1E90FF')
    
    # Adjust brightness based on intensity
    brightness = int(100 + (intensity * 100))
    
    avatar_html = f"""
    <div style="background-color: {color}; filter: brightness({brightness}%); 
         padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h3 style="color: white;">Kal 'Circuit' Chen</h3>
        <p style="color: white;">Python Detective Extraordinaire</p>
    </div>
    """
    return avatar_html

def save_to_memory_api(content, path="user/interaction", fork_type="Alpha"):
    """Save interaction to memory API (mocked for now)"""
    memory = {
        'path': path,
        'content': content,
        'fork_type': fork_type,
        'metadata': {'timestamp': datetime.now().isoformat()}
    }
    # In a real implementation, this would call your API
    # requests.post('http://localhost:5000/memories', json=memory)
    return memory

def process_message(user_input):
    """Process user message and update agent state"""
    # Get current emotion state
    emotion = st.session_state.emotion_state
    
    # Simple emotion detection
    if any(word in user_input.lower() for word in ['excited', 'amazing', 'wow']):
        emotion['circuit_pattern']['intensity'] = 0.8
        emotion['circuit_pattern']['rhythm'] = 'pulsing'
        emotion['circuit_pattern']['color_shift'] = 'excitement'
    elif any(word in user_input.lower() for word in ['funny', 'lol', 'haha']):
        emotion['circuit_pattern']['intensity'] = 0.7
        emotion['circuit_pattern']['rhythm'] = 'rippling'
        emotion['circuit_pattern']['color_shift'] = 'amused'
    else:
        emotion['circuit_pattern']['intensity'] = 0.5
        emotion['circuit_pattern']['rhythm'] = 'steady'
        emotion['circuit_pattern']['color_shift'] = 'thoughtful'
    
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_to_memory_api({"message": user_input, "role": "user"})
    
    # Generate response (in production, call your LLM here)
    if "python" in user_input.lower():
        response = "[*Tips fedora*] Python, my specialty! Let me help you debug that issue."
    elif "github" in user_input.lower():
        response = "[*Pushes up glasses*] GitHub, the backbone of version control. What specifically are you working on?"
    else:
        response = "[*Adjusts hoodie*] Interesting case you've brought me. Let me investigate further..."
    
    # Save agent response
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_to_memory_api({"message": response, "role": "assistant"})
    
    # Update emotion state
    st.session_state.emotion_state = emotion

# --- Sidebar ---
st.sidebar.title("Circuit's Detective Board")
st.sidebar.markdown("Case Files & Evidence")

# Fork selection
fork_type = st.sidebar.selectbox(
    "Select Fork Type",
    ["Alpha", "Beta", "Gamma"],
    index=0
)

# Debug emotion state
with st.sidebar.expander("Emotion Debug Panel"):
    st.json(st.session_state.emotion_state)

# Memory trace
with st.sidebar.expander("Memory Trace"):
    if st.button("Clear Memories"):
        st.session_state.messages = []
    
    # Show last 5 memories
    for i, msg in enumerate(st.session_state.messages[-5:]):
        st.text(f"{msg['role']}: {msg['content'][:30]}...")

# --- Main Interface ---
col1, col2 = st.columns([2, 5])

with col1:
    # Avatar display
    st.markdown(render_avatar(st.session_state.emotion_state), unsafe_allow_html=True)
    
    # Emote buttons
    st.write("Quick Emotes:")
    emote_cols = st.columns(3)
    if emote_cols[0].button("😎 Investigate"):
        st.session_state.emotion_state['circuit_pattern']['color_shift'] = 'thoughtful'
        st.session_state.emotion_state['circuit_pattern']['intensity'] = 0.6
    if emote_cols[1].button("💡 Idea"):
        st.session_state.emotion_state['circuit_pattern']['color_shift'] = 'excitement' 
        st.session_state.emotion_state['circuit_pattern']['intensity'] = 0.9
    if emote_cols[2].button("🕵️ Detective"):
        st.session_state.emotion_state['circuit_pattern']['color_shift'] = 'amused'
        st.session_state.emotion_state['circuit_pattern']['intensity'] = 0.7

with col2:
    # Chat interface
    st.title("Circuit's Detective Agency")
    st.markdown("*Where Python bugs have nowhere to hide*")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    if prompt := st.chat_input("What case can I help you with today?"):
        process_message(prompt)
        st.rerun()

# Footer
st.markdown("---")
st.caption("Circuit Chen | Cyberpunk Detective Agency | v0.1")