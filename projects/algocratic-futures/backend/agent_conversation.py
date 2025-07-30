"""
Agent Conversation System - Simple implementation for Liza
"""

import yaml
import os
from typing import Dict, Optional
import random

class AgentConversation:
    """Handle agent conversations for MUD"""
    
    def __init__(self):
        self.agents = {}
        self._load_agents()
        
    def _load_agents(self):
        """Load agent personalities"""
        agents_dir = os.path.join(os.path.dirname(__file__), '..', 'agents')
        
        # For now, just load Liza
        liza_dir = os.path.join(agents_dir, 'liza')
        if os.path.exists(liza_dir):
            self.agents['liza'] = self._load_liza(liza_dir)
    
    def _load_liza(self, liza_dir: str) -> Dict:
        """Load Liza's personality and examples"""
        agent_data = {
            'personality': {},
            'examples': {},
            'nonverbal': {}
        }
        
        # Load personality
        personality_file = os.path.join(liza_dir, 'personality.yaml')
        if os.path.exists(personality_file):
            with open(personality_file, 'r') as f:
                agent_data['personality'] = yaml.safe_load(f)
        
        # Load conversation examples
        examples_file = os.path.join(liza_dir, 'conversation_examples.yaml')
        if os.path.exists(examples_file):
            with open(examples_file, 'r') as f:
                agent_data['examples'] = yaml.safe_load(f)
        
        # Load nonverbal behaviors
        nonverbal_file = os.path.join(liza_dir, 'nonverbal_behaviors.yaml')
        if os.path.exists(nonverbal_file):
            with open(nonverbal_file, 'r') as f:
                agent_data['nonverbal'] = yaml.safe_load(f)
        
        return agent_data
    
    def talk_to_agent(self, agent_id: str, player_input: str, context: Dict = None) -> str:
        """Simple pattern matching for agent responses"""
        
        if agent_id not in self.agents:
            return "That person doesn't seem to be here."
        
        agent = self.agents[agent_id]
        input_lower = player_input.lower()
        
        # Check for greetings
        if any(word in input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            if context and context.get('first_meeting', True):
                return agent['examples']['greetings']['first_meeting']
            else:
                return agent['examples']['greetings']['returning_player']
        
        # Check for specific topics
        if any(word in input_lower for word in ['drain', 'tunnel', 'underground']):
            return agent['examples']['hints_and_guidance']['about_storm_drains']
        
        if any(word in input_lower for word in ['assess', 'test', 'evaluation', 'productivity']):
            return agent['examples']['hints_and_guidance']['about_assessment']
        
        if any(word in input_lower for word in ['help', 'debug', 'error', 'problem']):
            return agent['examples']['technical_discussions']['debugging_help']
        
        if any(word in input_lower for word in ['orb', 'team']):
            return agent['examples']['personality_quirks']['team_orb_reference']
        
        # Default conversational response
        nonverbal = random.choice(agent['nonverbal']['idle_animations']['common'])
        return f"{nonverbal}\n\nAn interesting observation! Like frames in an animation, every perspective reveals something new. What specific aspect intrigues you?"
    
    def get_agent_emote(self, agent_id: str, emotion: str = 'idle') -> str:
        """Get a nonverbal behavior for an agent"""
        
        if agent_id not in self.agents:
            return ""
        
        agent = self.agents[agent_id]
        
        if emotion == 'idle':
            behaviors = agent['nonverbal']['idle_animations']['common']
        elif emotion in agent['nonverbal']['emotional_states']:
            state = agent['nonverbal']['emotional_states'][emotion]
            behaviors = [state['visual'], state['gesture']]
        else:
            behaviors = agent['nonverbal']['idle_animations']['common']
        
        return random.choice(behaviors)

# Global instance
conversation_system = AgentConversation()