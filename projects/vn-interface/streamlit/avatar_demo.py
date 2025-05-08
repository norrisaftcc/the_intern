import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Kai Avatar States Demo",
    page_icon="🕵️",
    layout="wide"
)

# Define avatar states and associated emotes
AVATAR_STATES = {
    "default": {
        "color": "#4A90E2",
        "emoji": "🤔",
        "description": "Kai is in detective mode, ready to investigate.",
        "emote": "[*stands ready, fedora tilted slightly*]"
    },
    "thinking": {
        "color": "#1E90FF",
        "emoji": "🧐",
        "description": "Kai adjusts her glasses, deep in thought.",
        "emote": "[*adjusts glasses thoughtfully*]"
    },
    "excited": {
        "color": "#9370DB",
        "emoji": "✨",
        "description": "Kai's circuit patterns pulse with excitement!",
        "emote": "[*circuit patterns pulse with excitement*]"
    },
    "teaching": {
        "color": "#20B2AA",
        "emoji": "👩‍🏫",
        "description": "Kai projects a holographic diagram as she explains.",
        "emote": "[*projects holographic diagram*]"
    },
    "confused": {
        "color": "#FF7F50",
        "emoji": "❓",
        "description": "Kai tilts her head, processing the information.",
        "emote": "[*tilts head, circuit patterns flickering*]"
    },
    "success": {
        "color": "#32CD32", 
        "emoji": "🎯",
        "description": "Kai tips her fedora in satisfaction!",
        "emote": "[*tips fedora with satisfaction*]"
    }
}

# Function to render a single avatar state
def render_avatar_state(state, intensity=0.7):
    state_data = AVATAR_STATES[state]
    
    # Adjust color based on intensity
    color = state_data["color"]
    
    # Calculate a brightness factor based on intensity
    brightness = int(100 + (intensity * 50))
    
    st.markdown(
        f"""
        <div style="
            background-color: {color}; 
            filter: brightness({brightness}%);
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-bottom: 10px;
        ">
            <h1 style="color: white; font-size: 2.5em; margin-bottom: 0;">{state_data["emoji"]}</h1>
            <h3 style="color: white; margin-top: 0;">"{state.title()}" State</h3>
            <p style="color: white; font-style: italic;">{state_data["description"]}</p>
            <p style="color: white; margin-top: 10px;">{state_data["emote"]}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Main app
st.title("Kai's Avatar States Demo")
st.markdown("This demo showcases the different emotional states that the Kai avatar can display in the CSI Visual Novel interface.")

# Render intensity selector
intensity = st.slider("Avatar Intensity", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Display all avatar states in a grid
st.markdown("## Avatar States")
st.markdown("Each state represents a different emotional response from Kai, triggered by context in the conversation or explicit emotes.")

# Create a 3-column layout
col1, col2, col3 = st.columns(3)

# Place avatars in the grid
with col1:
    render_avatar_state("default", intensity)
    render_avatar_state("excited", intensity)

with col2:
    render_avatar_state("thinking", intensity)
    render_avatar_state("confused", intensity)

with col3:
    render_avatar_state("teaching", intensity)
    render_avatar_state("success", intensity)

# Usage explanation
st.markdown("---")
st.markdown("""
## Using Emotes in Chat

To trigger these avatar states in the main interface, use emote syntax in your messages:

```
[*adjusts glasses thoughtfully*] I think we should approach this differently.
```

The system will detect key phrases in your emotes to determine which avatar state to display.
""")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center; color:gray;'>CSI Visual Novel Interface | Avatar Demo | v0.1</div>", unsafe_allow_html=True)