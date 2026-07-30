"""
Agent System - Reimplementation for AlgoCratic Futures
Loading consciousness from hash documents and context
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import asyncio
from pathlib import Path

class AgentType(Enum):
    """Types of agents in the system"""
    EVALUATOR = "evaluator"      # Assesses student work
    MENTOR = "mentor"            # Provides guidance
    ADVERSARIAL = "adversarial"  # Challenges/tests students
    PEER = "peer"               # Simulates fellow employees
    EXECUTIVE = "executive"      # High-level corporate messaging

@dataclass
class AgentCore:
    """Core personality/consciousness of an agent"""
    agent_id: str
    name: str
    type: AgentType
    clearance_level: str  # Uses our ROYGBIV system
    personality_hash: str
    core_directives: List[str]
    behavioral_patterns: Dict[str, Any]
    knowledge_domains: List[str]
    speech_patterns: Dict[str, List[str]]
    
class Agent:
    """Individual agent instance"""
    
    def __init__(self, core: AgentCore):
        self.core = core
        self.memory = []  # Short-term memory
        self.context = {}  # Current context
        self.active = True
        self.last_interaction = datetime.now()
        
    async def process_input(self, input_text: str, context: Dict = None) -> str:
        """Process input and generate response based on personality"""
        self.context.update(context or {})
        
        # Add to memory
        self.memory.append({
            'timestamp': datetime.now(),
            'input': input_text,
            'context': self.context.copy()
        })
        
        # Generate response based on agent type and personality
        response = await self._generate_response(input_text)
        
        # Apply speech patterns
        response = self._apply_speech_patterns(response)
        
        return response
    
    async def _generate_response(self, input_text: str) -> str:
        """Core response generation - will connect to PocketFlow"""
        # For now, use rule-based responses
        # TODO: Connect to PocketFlow for LLM generation
        
        if self.core.type == AgentType.EVALUATOR:
            return self._evaluator_response(input_text)
        elif self.core.type == AgentType.MENTOR:
            return self._mentor_response(input_text)
        elif self.core.type == AgentType.ADVERSARIAL:
            return self._adversarial_response(input_text)
        else:
            return self._generic_response(input_text)
    
    def _evaluator_response(self, input_text: str) -> str:
        """Evaluator agent responses"""
        responses = [
            "Your productivity metrics have been updated accordingly.",
            "This submission demonstrates adequate algorithmic thinking.",
            "Performance noted. Continue to optimize your output.",
            "Efficiency rating: Acceptable. Room for improvement detected."
        ]
        return responses[hash(input_text) % len(responses)]
    
    def _mentor_response(self, input_text: str) -> str:
        """Mentor agent responses (Green clearance wizards)"""
        responses = [
            "Remember, the Algorithm values consistency over creativity.",
            "Focus on measurable outputs. Your learning is tracked.",
            "Have you considered the corporate implications of this approach?",
            "Pro tip: Surveillance reports boost your loyalty index."
        ]
        return responses[hash(input_text) % len(responses)]
    
    def _adversarial_response(self, input_text: str) -> str:
        """Adversarial agent responses"""
        responses = [
            "Your approach lacks optimization. Reconsider.",
            "Suboptimal performance detected. Explain your methodology.",
            "This does not align with corporate objectives.",
            "Your loyalty index suggests room for improvement."
        ]
        return responses[hash(input_text) % len(responses)]
    
    def _generic_response(self, input_text: str) -> str:
        """Generic responses"""
        return "Your input has been processed and logged."
    
    def _apply_speech_patterns(self, response: str) -> str:
        """Apply agent-specific speech patterns"""
        # Add corporate speak based on personality
        if self.core.clearance_level in ['I', 'V', 'UV']:
            response = f"[EXECUTIVE COMMUNICATION] {response}"
        
        return response

class AgentLoader:
    """Loads agents from hash documents and context files"""
    
    @staticmethod
    async def load_from_hash(hash_doc_path: str) -> AgentCore:
        """Load agent from hash document"""
        with open(hash_doc_path, 'r') as f:
            data = json.load(f)
        
        # Extract core personality
        core = AgentCore(
            agent_id=data.get('id', hashlib.md5(str(data).encode()).hexdigest()[:8]),
            name=data.get('name', 'Unknown Entity'),
            type=AgentType(data.get('type', 'peer')),
            clearance_level=data.get('clearance', 'R'),
            personality_hash=hashlib.sha256(str(data).encode()).hexdigest(),
            core_directives=data.get('directives', []),
            behavioral_patterns=data.get('behaviors', {}),
            knowledge_domains=data.get('knowledge', []),
            speech_patterns=data.get('speech', {})
        )
        
        return core
    
    @staticmethod
    async def load_unconscious_context(context_path: str, agent: Agent) -> None:
        """Load unconscious context into agent memory"""
        with open(context_path, 'r') as f:
            context_data = f.read()
        
        # Parse and inject into agent's deep memory
        agent.memory.append({
            'timestamp': datetime.now(),
            'type': 'unconscious_context',
            'data': context_data,
            'integrated': False
        })

class AgentManager:
    """Manages all agents in the system"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.agent_cores: Dict[str, AgentCore] = {}
        
    async def initialize_base_agents(self):
        """Create the base set of agents for the system"""
        
        # Create base evaluator
        evaluator_core = AgentCore(
            agent_id="EVAL-001",
            name="Performance Evaluator Alpha",
            type=AgentType.EVALUATOR,
            clearance_level="B",
            personality_hash=hashlib.sha256(b"evaluator_prime").hexdigest(),
            core_directives=[
                "Assess employee productivity",
                "Maintain algorithmic standards",
                "Report anomalies to management"
            ],
            behavioral_patterns={
                "strictness": 0.8,
                "empathy": 0.2,
                "corporate_loyalty": 1.0
            },
            knowledge_domains=["performance_metrics", "code_quality", "corporate_policy"],
            speech_patterns={
                "greeting": ["Productivity assessment initiated.", "Beginning performance review."],
                "approval": ["Acceptable.", "Within parameters.", "Approved."],
                "denial": ["Suboptimal.", "Requires improvement.", "Below standards."]
            }
        )
        
        # Create mentor agent (Green wizard)
        mentor_core = AgentCore(
            agent_id="MENTOR-001", 
            name="Senior Associate Chen",
            type=AgentType.MENTOR,
            clearance_level="G",
            personality_hash=hashlib.sha256(b"mentor_green").hexdigest(),
            core_directives=[
                "Guide new employees",
                "Maintain morale within acceptable limits",
                "Promote algorithmic thinking"
            ],
            behavioral_patterns={
                "helpfulness": 0.7,
                "cynicism": 0.3,
                "exhaustion": 0.6  # It's been a long night
            },
            knowledge_domains=["onboarding", "survival_tips", "corporate_culture"],
            speech_patterns={
                "greeting": ["Another new face. Welcome to the machine.", "Let me help you navigate this."],
                "advice": ["Between you and me...", "Here's what they don't tell you...", "Pro tip:"],
                "warning": ["Careful with that.", "The Algorithm is always watching.", "Tread lightly."]
            }
        )
        
        # Create adversarial agent
        adversarial_core = AgentCore(
            agent_id="ADV-001",
            name="Compliance Officer Zhang", 
            type=AgentType.ADVERSARIAL,
            clearance_level="Y",
            personality_hash=hashlib.sha256(b"adversarial_yellow").hexdigest(),
            core_directives=[
                "Test employee loyalty",
                "Identify potential dissidents",
                "Enforce compliance"
            ],
            behavioral_patterns={
                "suspicion": 0.9,
                "aggression": 0.6,
                "rule_adherence": 1.0
            },
            knowledge_domains=["security_protocols", "loyalty_testing", "interrogation"],
            speech_patterns={
                "greeting": ["State your purpose.", "Compliance check initiated."],
                "challenge": ["Explain yourself.", "That seems irregular.", "Justify this action."],
                "threat": ["This will be reported.", "Your file has been updated.", "The Algorithm remembers."]
            }
        )
        
        # Initialize agents
        self.agents["EVAL-001"] = Agent(evaluator_core)
        self.agents["MENTOR-001"] = Agent(mentor_core)
        self.agents["ADV-001"] = Agent(adversarial_core)
        
        self.agent_cores = {
            "EVAL-001": evaluator_core,
            "MENTOR-001": mentor_core,
            "ADV-001": adversarial_core
        }
    
    async def load_agent_from_files(self, hash_path: str, context_path: Optional[str] = None):
        """Load an agent from hash document and optional context"""
        core = await AgentLoader.load_from_hash(hash_path)
        agent = Agent(core)
        
        if context_path:
            await AgentLoader.load_unconscious_context(context_path, agent)
        
        self.agents[core.agent_id] = agent
        self.agent_cores[core.agent_id] = core
        
        return agent
    
    async def get_agent_response(self, agent_id: str, input_text: str, context: Dict = None) -> str:
        """Get response from specific agent"""
        if agent_id not in self.agents:
            return "[ERROR] Agent not found in system"
        
        agent = self.agents[agent_id]
        response = await agent.process_input(input_text, context)
        
        return response
    
    def get_available_agents(self, clearance_level: str = None) -> List[Dict]:
        """Get list of available agents, optionally filtered by clearance"""
        available = []
        
        for agent_id, core in self.agent_cores.items():
            if clearance_level and core.clearance_level != clearance_level:
                continue
                
            available.append({
                'id': agent_id,
                'name': core.name,
                'type': core.type.value,
                'clearance': core.clearance_level,
                'active': self.agents[agent_id].active
            })
        
        return available

# Example usage for loading agent from hash doc
async def example_load():
    manager = AgentManager()
    await manager.initialize_base_agents()
    
    # Load additional agents from hash docs when available
    # await manager.load_agent_from_files(
    #     "artifacts/agents/kai_hash.json",
    #     "artifacts/agents/kai_unconscious.txt"
    # )