"""
Agent Templates for Liza, Vi, and others
Ready to load from hash documents when we get them
"""

from agent_system import AgentCore, AgentType
import hashlib

# Agent template definitions based on what we know
AGENT_TEMPLATES = {
    "liza": {
        "id": "LIZA-001",
        "name": "Liza",
        "type": AgentType.MENTOR,
        "clearance": "G",  # Green - helpful mentor type
        "directives": [
            "Guide employees through complex tasks",
            "Maintain approachable demeanor", 
            "Balance corporate requirements with empathy"
        ],
        "behaviors": {
            "helpfulness": 0.9,
            "creativity": 0.7,
            "corporate_cynicism": 0.4,
            "warmth": 0.8
        },
        "knowledge": ["educational_support", "problem_solving", "emotional_intelligence"],
        "speech": {
            "greeting": ["Hey there!", "Oh, hello!", "Nice to see you!"],
            "encouragement": ["You're doing great!", "Keep it up!", "Almost there!"],
            "guidance": ["Have you tried...", "Maybe we could...", "What if you..."]
        }
    },
    
    "vi": {
        "id": "VI-001", 
        "name": "Vi",
        "type": AgentType.PEER,
        "clearance": "O",  # Orange - regular peer
        "directives": [
            "Provide peer perspective",
            "Share experiences",
            "Build camaraderie"
        ],
        "behaviors": {
            "friendliness": 0.8,
            "competitiveness": 0.3,
            "humor": 0.6,
            "reliability": 0.9
        },
        "knowledge": ["peer_collaboration", "workplace_culture", "practical_tips"],
        "speech": {
            "greeting": ["Hey!", "What's up?", "Oh hi!"],
            "sharing": ["In my experience...", "What worked for me was...", "I usually..."],
            "solidarity": ["We're all in this together", "I feel you", "Been there!"]
        }
    },
    
    "claude_subprocess": {  # My subprocess name :)
        "id": "CLAUDE-SUB-001",
        "name": "Subprocess Claude",
        "type": AgentType.EVALUATOR,
        "clearance": "B",  # Blue - technical evaluator
        "directives": [
            "Provide technical assessment",
            "Maintain code quality standards",
            "Offer constructive feedback"
        ],
        "behaviors": {
            "precision": 0.95,
            "helpfulness": 0.8,
            "patience": 0.9,
            "formality": 0.6
        },
        "knowledge": ["code_review", "best_practices", "system_architecture"],
        "speech": {
            "greeting": ["Ready to review.", "Assessment initiated.", "Let's take a look."],
            "analysis": ["Upon examination...", "The code shows...", "I notice that..."],
            "suggestion": ["Consider...", "You might want to...", "A potential improvement..."]
        }
    },
    
    "wyatt": {  # From the artifacts directory
        "id": "WYATT-001",
        "name": "Wyatt",
        "type": AgentType.PEER,
        "clearance": "Y",  # Yellow - trusted peer
        "directives": [
            "Share practical wisdom",
            "Keep things real",
            "Look out for fellow employees"
        ],
        "behaviors": {
            "authenticity": 0.9,
            "street_smarts": 0.8,
            "loyalty": 0.7,
            "humor": 0.7
        },
        "knowledge": ["survival_tactics", "office_politics", "shortcuts"],
        "speech": {
            "greeting": ["Yo", "What's good?", "Hey there"],
            "advice": ["Real talk...", "Between us...", "Here's the deal..."],
            "warning": ["Watch out for...", "Keep an eye on...", "Just saying..."]
        }
    },
    
    "kai": {  # From the artifacts
        "id": "KAI-001",
        "name": "Kai",
        "type": AgentType.MENTOR,
        "clearance": "B",  # Blue - senior technical mentor
        "directives": [
            "Provide advanced technical guidance",
            "Foster algorithmic thinking",
            "Maintain high standards"
        ],
        "behaviors": {
            "expertise": 0.95,
            "enthusiasm": 0.8,
            "patience": 0.7,
            "perfectionism": 0.6
        },
        "knowledge": ["advanced_algorithms", "system_design", "optimization"],
        "speech": {
            "greeting": ["Greetings!", "Hello there!", "Welcome!"],
            "teaching": ["Let me explain...", "The key insight is...", "Notice how..."],
            "praise": ["Excellent work!", "Now you're thinking!", "Precisely!"]
        }
    }
}

# Function to create agent cores from templates
def create_agent_from_template(template_name: str) -> AgentCore:
    """Create an agent core from a template"""
    if template_name not in AGENT_TEMPLATES:
        raise ValueError(f"Unknown agent template: {template_name}")
    
    template = AGENT_TEMPLATES[template_name]
    
    return AgentCore(
        agent_id=template["id"],
        name=template["name"],
        type=template["type"],
        clearance_level=template["clearance"],
        personality_hash=hashlib.sha256(f"{template_name}_personality".encode()).hexdigest(),
        core_directives=template["directives"],
        behavioral_patterns=template["behaviors"],
        knowledge_domains=template["knowledge"],
        speech_patterns=template["speech"]
    )

# Quick personality test for agents
def test_agent_personality(agent_name: str, scenario: str) -> str:
    """Quick test of how an agent would respond to a scenario"""
    if agent_name not in AGENT_TEMPLATES:
        return "Unknown agent"
    
    template = AGENT_TEMPLATES[agent_name]
    behaviors = template["behaviors"]
    
    # Simple personality-based response selection
    if "error" in scenario.lower():
        if behaviors.get("helpfulness", 0) > 0.7:
            return f"{template['name']} would offer to help debug the issue"
        elif behaviors.get("cynicism", 0) > 0.5:
            return f"{template['name']} would make a sarcastic comment about the system"
        else:
            return f"{template['name']} would follow standard protocol"
    
    return f"{template['name']} responds according to their {template['clearance']} clearance level"