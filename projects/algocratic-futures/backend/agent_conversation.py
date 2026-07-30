"""
Agent Conversation System - Simple implementation for Liza
"""

import yaml
import os
from typing import Dict, Optional
import random
from sqlalchemy.orm import Session
from database import log_conversation, get_or_create_user, update_student_progress

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
    
    def talk_to_agent(self, agent_id: str, player_input: str, context: Dict = None, 
                     db: Session = None, user_id: int = None, room_location: str = None) -> str:
        """Enhanced pattern matching with conversation memory"""
        
        if agent_id not in self.agents:
            return "That person doesn't seem to be here."
        
        agent = self.agents[agent_id]
        input_lower = player_input.lower()
        
        # Check conversation history for relationship context
        conversation_count = 0
        if db and user_id:
            from database import ConversationHistory
            conversation_count = db.query(ConversationHistory).filter(
                ConversationHistory.user_id == user_id,
                ConversationHistory.agent_id == agent_id
            ).count()
        
        # Determine if this is a first meeting
        is_first_meeting = conversation_count == 0
        
        # Check for greetings
        if any(word in input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            if is_first_meeting:
                response = agent['examples']['greetings']['first_meeting']
            else:
                response = agent['examples']['greetings']['returning_player']
        elif any(word in input_lower for word in ['drain', 'tunnel', 'underground']):
            response = agent['examples']['hints_and_guidance']['about_storm_drains']
        elif any(word in input_lower for word in ['assess', 'test', 'evaluation', 'productivity']):
            response = agent['examples']['hints_and_guidance']['about_assessment']
        elif any(word in input_lower for word in ['help', 'debug', 'error', 'problem']):
            response = agent['examples']['technical_discussions']['debugging_help']
        elif any(word in input_lower for word in ['orb', 'team']):
            response = agent['examples']['personality_quirks']['team_orb_reference']
        else:
            # Default conversational response
            nonverbal = random.choice(agent['nonverbal']['idle_animations']['common'])
            response = f"{nonverbal}\n\nAn interesting observation! Like frames in an animation, every perspective reveals something new. What specific aspect intrigues you?"
        
        # Log conversation if database connection available
        if db and user_id:
            try:
                log_conversation(
                    db=db,
                    user_id=user_id,
                    agent_id=agent_id,
                    user_input=player_input,
                    agent_response=response,
                    room_location=room_location,
                    context={'conversation_count': conversation_count + 1}
                )
                
                # Update student progress for Liza conversations
                if agent_id == 'liza':
                    update_student_progress(
                        db=db,
                        user_id=user_id,
                        liza_conversations=conversation_count + 1
                    )
            except Exception as e:
                print(f"Warning: Could not log conversation: {e}")
        
        return response
    
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