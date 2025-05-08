"""
Avatar SVG generation for the CSI Agent Chat Window
"""

def generate_avatar_svg(state="default", fork_type="Alpha", intensity=0.7, character_type="circuit"):
    """
    Generate an SVG avatar based on character state and fork type
    
    Parameters:
    - state: The emotional state of the avatar (default, thinking, excited, teaching, confused, success)
    - fork_type: Alpha, Beta, or Gamma
    - intensity: Emotion intensity from 0.0 to 1.0
    - character_type: Character style template (circuit, teacherbot, debug_whiz)
    
    Returns:
    - SVG markup as a string
    """
    # Base colors for different fork types
    fork_colors = {
        "Alpha": {
            "primary": "#4A90E2",
            "secondary": "#2176CC",
            "accent": "#6FB1FF",
            "text": "#FFFFFF"
        },
        "Beta": {
            "primary": "#34C759",
            "secondary": "#28A745",
            "accent": "#5FE587",
            "text": "#FFFFFF"
        },
        "Gamma": {
            "primary": "#9370DB",
            "secondary": "#7D53C3",
            "accent": "#B29AE8",
            "text": "#FFFFFF"
        }
    }
    
    # Character-specific attributes
    character_attributes = {
        "circuit": {
            "hat": True,
            "glasses": True,
            "circuit_lines": True,
            "hair_color": "#00BFFF",  # Electric blue
            "feature": "fedora"
        },
        "teacherbot": {
            "hat": False,
            "glasses": True,
            "circuit_lines": False,
            "hair_color": "#2E8B57",  # Sea green
            "feature": "book"
        },
        "debug_whiz": {
            "hat": False,
            "glasses": True,
            "circuit_lines": True,
            "hair_color": "#FF6347",  # Tomato red
            "feature": "magnifier"
        }
    }
    
    # Get colors for fork type
    colors = fork_colors.get(fork_type, fork_colors["Alpha"])
    
    # Get character attributes
    attrs = character_attributes.get(character_type, character_attributes["circuit"])
    
    # Adjust brightness based on intensity
    brightness_factor = 0.7 + (intensity * 0.5)
    
    # Helper function to adjust color brightness
    def adjust_brightness(hex_color, factor):
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Adjust brightness
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Brightness-adjusted colors
    primary_color = adjust_brightness(colors["primary"], brightness_factor)
    secondary_color = adjust_brightness(colors["secondary"], brightness_factor)
    accent_color = adjust_brightness(colors["accent"], brightness_factor)
    
    # State-specific animations and elements
    animations = {
        "default": "",
        "thinking": """
            <animate attributeName="opacity" values="1;0.7;1" dur="3s" repeatCount="indefinite" />
        """,
        "excited": """
            <animate attributeName="transform" attributeType="XML" type="translate" 
                     values="0,0; 0,-5; 0,0" dur="0.5s" repeatCount="indefinite" />
        """,
        "teaching": """
            <animate attributeName="stroke-width" values="2;3;2" dur="2s" repeatCount="indefinite" />
        """,
        "confused": """
            <animate attributeName="transform" attributeType="XML" type="rotate" 
                     values="0 200 180; 5 200 180; 0 200 180; -5 200 180; 0 200 180" 
                     dur="2s" repeatCount="indefinite" />
        """,
        "success": """
            <animate attributeName="fill" values="${primary_color};${accent_color};${primary_color}" 
                     dur="2s" repeatCount="indefinite" />
        """.replace("${primary_color}", primary_color).replace("${accent_color}", accent_color)
    }
    
    # Get animation for current state
    animation = animations.get(state, "")
    
    # Generate the SVG
    svg = f"""
    <svg width="250" height="300" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <style>
            .circuit-line {{
                stroke: {accent_color};
                stroke-width: 2;
                stroke-dasharray: 5,5;
            }}
            @keyframes pulse {{
                0% {{ opacity: 0.5; }}
                50% {{ opacity: 1; }}
                100% {{ opacity: 0.5; }}
            }}
            .pulse {{
                animation: pulse 2s infinite;
            }}
        </style>
        
        <!-- Face/Head -->
        <g transform="translate(100, 50)" {animation}>
            <!-- Head Shape -->
            <circle cx="100" cy="120" r="100" fill="{primary_color}" />
            
            <!-- Circuit Patterns (if applicable) -->
            {generate_circuit_patterns(attrs["circuit_lines"], accent_color, state) if attrs["circuit_lines"] else ""}
            
            <!-- Eyes -->
            {generate_eyes(state, attrs["glasses"], secondary_color, accent_color)}
            
            <!-- Mouth -->
            {generate_mouth(state, colors["text"])}
            
            <!-- Nose -->
            <path d="M100,120 L105,135 L95,135 Z" fill="none" stroke="{colors['text']}" stroke-width="2" />
            
            <!-- Hair -->
            {generate_hair(attrs["hair_color"], state)}
            
            <!-- Feature Item (hat, book, magnifier) -->
            {generate_feature(attrs["feature"], secondary_color, accent_color, state)}
        </g>
        
        <!-- Fork Type Indicator -->
        <text x="200" y="380" text-anchor="middle" fill="{secondary_color}" font-family="Arial" font-size="20">
            {fork_type} Fork
        </text>
    </svg>
    """
    
    return svg


def generate_circuit_patterns(show_circuits, accent_color, state):
    """Generate circuit patterns based on state"""
    if not show_circuits:
        return ""
    
    # Different patterns for different states
    if state == "excited":
        pulse_class = "class='pulse'"
    else:
        pulse_class = ""
    
    return f"""
        <!-- Circuit Pattern -->
        <path {pulse_class} d="M30,80 L70,80 L70,60 L90,60 L90,100 L120,100 L120,80 L150,80 L150,100 L170,100" 
              class="circuit-line" fill="none" />
        <path {pulse_class} d="M30,140 L50,140 L50,160 L100,160 L100,180 L150,180 L150,160 L170,160" 
              class="circuit-line" fill="none" />
        <path {pulse_class} d="M70,40 L70,20 L120,20 L120,40" 
              class="circuit-line" fill="none" />
    """


def generate_eyes(state, has_glasses, secondary_color, accent_color):
    """Generate eyes based on state and whether glasses are present"""
    
    # Eye base
    eyes = f"""
        <!-- Eyes -->
        <ellipse cx="70" cy="100" rx="15" ry="{10 if state == 'excited' else 15}" fill="white" />
        <ellipse cx="130" cy="100" rx="15" ry="{10 if state == 'excited' else 15}" fill="white" />
    """
    
    # Pupils change with state
    if state == "thinking":
        # Looking up and to the side
        eyes += f"""
            <circle cx="75" cy="95" r="5" fill="{secondary_color}" />
            <circle cx="135" cy="95" r="5" fill="{secondary_color}" />
        """
    elif state == "confused":
        # One eye squinting
        eyes += f"""
            <circle cx="70" cy="100" r="5" fill="{secondary_color}" />
            <ellipse cx="130" cy="100" rx="8" ry="4" fill="{secondary_color}" />
        """
    elif state == "excited":
        # Wide-open eyes
        eyes += f"""
            <circle cx="70" cy="100" r="7" fill="{secondary_color}" />
            <circle cx="130" cy="100" r="7" fill="{secondary_color}" />
            <circle cx="73" cy="97" r="2" fill="white" />
            <circle cx="133" cy="97" r="2" fill="white" />
        """
    else:
        # Default eyes
        eyes += f"""
            <circle cx="70" cy="100" r="6" fill="{secondary_color}" />
            <circle cx="130" cy="100" r="6" fill="{secondary_color}" />
        """
    
    # Add glasses if applicable
    if has_glasses:
        eyes += f"""
            <!-- Glasses -->
            <circle cx="70" cy="100" r="20" fill="none" stroke="{accent_color}" stroke-width="2" />
            <circle cx="130" cy="100" r="20" fill="none" stroke="{accent_color}" stroke-width="2" />
            <line x1="90" y1="100" x2="110" y2="100" stroke="{accent_color}" stroke-width="2" />
            <line x1="50" y1="100" x2="40" y2="95" stroke="{accent_color}" stroke-width="2" />
            <line x1="150" y1="100" x2="160" y2="95" stroke="{accent_color}" stroke-width="2" />
        """
    
    return eyes


def generate_mouth(state, text_color):
    """Generate mouth based on state"""
    if state == "excited":
        # Big smile
        return f"""
            <path d="M70,150 Q100,180 130,150" fill="none" stroke="{text_color}" stroke-width="3" />
        """
    elif state == "confused":
        # Squiggly unsure line
        return f"""
            <path d="M70,150 Q85,155 100,150 Q115,145 130,150" fill="none" stroke="{text_color}" stroke-width="3" />
        """
    elif state == "thinking":
        # Straight thoughtful line
        return f"""
            <line x1="70" y1="150" x2="130" y2="150" stroke="{text_color}" stroke-width="3" />
        """
    elif state == "success":
        # Confident smirk
        return f"""
            <path d="M70,150 Q100,170 130,150" fill="none" stroke="{text_color}" stroke-width="3" />
        """
    else:
        # Slight smile
        return f"""
            <path d="M70,150 Q100,165 130,150" fill="none" stroke="{text_color}" stroke-width="3" />
        """


def generate_hair(hair_color, state):
    """Generate hair with given color, style varies by state"""
    # Pulsing effect for excited state
    pulse_class = "class='pulse'" if state == "excited" else ""
    
    return f"""
        <!-- Hair -->
        <path {pulse_class} d="M40,80 Q50,50 70,40 Q100,20 130,40 Q150,50 160,80" 
              fill="{hair_color}" />
    """


def generate_feature(feature, secondary_color, accent_color, state):
    """Generate feature item based on character type and state"""
    if feature == "fedora":
        # Hat tilted differently based on state
        tilt = "transform='rotate(-10)'" if state == "success" else ""
        return f"""
            <!-- Fedora -->
            <g {tilt}>
                <path d="M25,60 Q100,-10 175,60" fill="{secondary_color}" />
                <path d="M20,60 Q100,80 180,60 L160,80 Q100,100 40,80 Z" fill="{secondary_color}" />
                <path d="M100,60 Q100,70 100,80" fill="none" stroke="{accent_color}" stroke-width="2" />
            </g>
        """
    elif feature == "book":
        # Book appears on teaching state
        if state == "teaching":
            return f"""
                <!-- Open Book -->
                <g transform="translate(0, 180) scale(0.5)">
                    <rect x="60" y="0" width="80" height="10" fill="{secondary_color}" />
                    <rect x="55" y="10" width="90" height="100" fill="white" stroke="{secondary_color}" stroke-width="2" />
                    <line x1="100" y1="10" x2="100" y2="110" stroke="{secondary_color}" stroke-width="2" />
                    <line x1="70" y1="30" x2="90" y2="30" stroke="{accent_color}" stroke-width="2" />
                    <line x1="70" y1="50" x2="90" y2="50" stroke="{accent_color}" stroke-width="2" />
                    <line x1="70" y1="70" x2="90" y2="70" stroke="{accent_color}" stroke-width="2" />
                    <line x1="110" y1="30" x2="130" y2="30" stroke="{accent_color}" stroke-width="2" />
                    <line x1="110" y1="50" x2="130" y2="50" stroke="{accent_color}" stroke-width="2" />
                    <line x1="110" y1="70" x2="130" y2="70" stroke="{accent_color}" stroke-width="2" />
                </g>
            """
        return ""
    elif feature == "magnifier":
        # Magnifier appears on thinking or confused state
        if state in ["thinking", "confused"]:
            return f"""
                <!-- Magnifying Glass -->
                <g transform="translate(160, 80) rotate(30)">
                    <circle cx="0" cy="0" r="20" fill="none" stroke="{accent_color}" stroke-width="3" />
                    <line x1="14" y1="14" x2="30" y2="30" stroke="{accent_color}" stroke-width="3" />
                </g>
            """
        return ""
    else:
        return ""