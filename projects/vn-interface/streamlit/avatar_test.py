import streamlit as st
from avatar_svg import generate_avatar_svg

# Set page configuration
st.set_page_config(
    page_title="CSI Avatar Test",
    page_icon="🕵️",
    layout="wide"
)

st.title("CSI Agent Avatar Test")
st.markdown("This interactive demo lets you test the SVG avatar system with different states, fork types, and character designs.")

# Sidebar controls
st.sidebar.title("Avatar Controls")

# Character type selection
character_types = {
    "circuit": "Cyberpunk Detective (Kai)",
    "teacherbot": "Educational Assistant",
    "debug_whiz": "Debugging Specialist"
}

character_type = st.sidebar.selectbox(
    "Character Type",
    options=list(character_types.keys()),
    format_func=lambda x: character_types[x]
)

# Fork type selection
fork_type = st.sidebar.selectbox(
    "Fork Type",
    options=["Alpha", "Beta", "Gamma"],
    help="Fork types represent different agent capabilities."
)

# State selection
state = st.sidebar.selectbox(
    "Emotional State",
    options=["default", "thinking", "excited", "teaching", "confused", "success"],
    help="The emotional state of the avatar."
)

# Intensity slider
intensity = st.sidebar.slider(
    "Emotion Intensity",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="How intensely the emotion is displayed."
)

# Generate SVG
svg = generate_avatar_svg(
    state=state,
    fork_type=fork_type,
    intensity=intensity,
    character_type=character_type
)

# Display the avatar
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(svg, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"## {character_types[character_type]}")
    st.markdown(f"**Fork Type:** {fork_type}")
    st.markdown(f"**State:** {state.title()}")
    st.markdown(f"**Intensity:** {intensity:.1f}")
    
    st.markdown("---")
    
    st.markdown("### Character Traits")
    if character_type == "circuit":
        st.markdown("""
        - Cyberpunk detective aesthetic
        - Electric blue circuit patterns
        - Detective fedora hat
        - Tech-savvy problem solver
        """)
    elif character_type == "teacherbot":
        st.markdown("""
        - Educational assistant style
        - Calming sea green colors
        - Glasses for scholarly appearance
        - Shows book when in teaching mode
        """)
    elif character_type == "debug_whiz":
        st.markdown("""
        - Debugging specialist look
        - Energetic tomato red accents
        - Circuit patterns show processing
        - Magnifying glass when investigating
        """)

# Emote examples
st.markdown("---")
st.markdown("## Example Emotes")

emotes = {
    "circuit": [
        "[*adjusts glasses thoughtfully*]",
        "[*circuit patterns glow with excitement*]",
        "[*tips fedora slightly*]",
        "[*projects holographic diagram*]"
    ],
    "teacherbot": [
        "[*opens digital textbook*]",
        "[*highlights key concept*]",
        "[*patiently explains*]",
        "[*draws virtual diagram*]"
    ],
    "debug_whiz": [
        "[*frantically scrolls through code*]",
        "[*gasps dramatically at bug discovery*]",
        "[*virtual magnifying glass appears*]",
        "[*types debugging commands at lightning speed*]"
    ]
}

for emote in emotes[character_type]:
    st.code(emote)

# Footer
st.markdown("---")
st.caption("CSI Avatar Test | Creative Solutions Investigation")