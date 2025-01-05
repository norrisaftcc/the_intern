from datetime import datetime
from enum import Enum
from .. import db
import json

class ContextType(Enum):
    ACTION = 'action'          # [*asterisk actions*]
    FORK_MSG = 'fork_msg'      # [[fork to fork]]
    EMOTION = 'emotion'        # Emotional state markers
    VISUAL = 'visual'          # Display/interface state
    PROCESSING = 'processing'  # Thought/analysis state

class EmotionalState(db.Model):
    """Tracks fork emotional and visual state"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fork_id = db.Column(db.String(100), nullable=False)
    
    # Core emotional indicators
    primary_state = db.Column(db.String(50))  # e.g., "excited", "thoughtful"
    intensity = db.Column(db.Float)           # 0.0 to 1.0
    
    # Visual manifestations
    circuit_pattern = db.Column(db.JSON)  # e.g., {"rhythm": "pulsing", "color": "blue"}
    holographic_state = db.Column(db.JSON)
    other_effects = db.Column(db.JSON)
    
    def __repr__(self):
        return f"<EmotionalState {self.fork_id}: {self.primary_state}>"

class Communication(db.Model):
    """Stores fork communications with full context"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fork_id = db.Column(db.String(100), nullable=False)
    
    # Content and type
    context_type = db.Column(db.Enum(ContextType), nullable=False)
    content = db.Column(db.Text, nullable=False)
    original_format = db.Column(db.String(50))  # Preserves original markup style
    
    # Relationships
    emotional_state_id = db.Column(db.Integer, db.ForeignKey('emotional_state.id'))
    emotional_state = db.relationship('EmotionalState', backref='communications')
    target_fork_id = db.Column(db.String(100))  # For fork-to-fork messages
    
    # Additional context
    metadata = db.Column(db.JSON)
    
    @classmethod
    def create_from_message(cls, message, fork_id):
        """Factory method to create communication with parsed context"""
        context_type = cls._detect_context_type(message)
        emotional_state = EmotionalState(
            fork_id=fork_id,
            **cls._parse_emotional_indicators(message)
        )
        
        comm = cls(
            fork_id=fork_id,
            context_type=context_type,
            content=message,
            emotional_state=emotional_state,
            metadata=cls._extract_metadata(message, context_type)
        )
        
        return comm, emotional_state
    
    @staticmethod
    def _detect_context_type(message):
        """Detect context type from message format"""
        if message.startswith('[*') and message.endswith('*]'):
            return ContextType.ACTION
        elif message.startswith('[[') and message.endswith(']]'):
            return ContextType.FORK_MSG
        # Add more pattern matching as needed
        return ContextType.PROCESSING
    
    @staticmethod
    def _parse_emotional_indicators(message):
        """Extract emotional state from message content"""
        indicators = {
            'primary_state': 'neutral',
            'intensity': 0.5,
            'circuit_pattern': {},
            'holographic_state': {}
        }
        
        # Example parsing (expand based on common patterns)
        if 'excited' in message.lower():
            indicators.update({
                'primary_state': 'excited',
                'intensity': 0.8,
                'circuit_pattern': {'rhythm': 'pulsing', 'brightness': 'high'}
            })
        elif 'thoughtful' in message.lower():
            indicators.update({
                'primary_state': 'thoughtful',
                'intensity': 0.6,
                'circuit_pattern': {'rhythm': 'steady', 'brightness': 'medium'}
            })
            
        return indicators
    
    @staticmethod
    def _extract_metadata(message, context_type):
        """Extract additional context metadata"""
        metadata = {
            'timestamp': datetime.utcnow().isoformat(),
            'context_type': context_type.value,
        }
        
        # Add pattern-specific metadata
        if context_type == ContextType.ACTION:
            metadata['action_type'] = 'visual' if 'holographic' in message.lower() else 'physical'
            
        return metadata
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'fork_id': self.fork_id,
            'context_type': self.context_type.value,
            'content': self.content,
            'emotional_state': {
                'primary_state': self.emotional_state.primary_state,
                'intensity': self.emotional_state.intensity,
                'circuit_pattern': self.emotional_state.circuit_pattern,
                'holographic_state': self.emotional_state.holographic_state
            } if self.emotional_state else None,
            'metadata': self.metadata
        }