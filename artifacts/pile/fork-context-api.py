from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fork_context.db'
db = SQLAlchemy(app)

class CommunicationType(Enum):
    ACTION = 'action'          # [*asterisk actions*]
    FORK_MSG = 'fork_msg'      # [[fork to fork]]
    THOUGHT = 'thought'        # Internal processing
    EMOTION = 'emotion'        # Emotional state
    DISPLAY = 'display'        # Holographic/visual elements

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fork_id = db.Column(db.String(100), nullable=False)
    comm_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Emotional/Context Metadata
    emotion_state = db.Column(db.JSON)  # Color patterns, intensity, etc.
    visual_effects = db.Column(db.JSON)  # Holographic displays, circuit patterns
    thought_context = db.Column(db.JSON)  # Processing state, analysis context
    
    # For fork-to-fork messages
    target_fork_id = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'fork_id': self.fork_id,
            'comm_type': self.comm_type,
            'content': self.content,
            'emotion_state': self.emotion_state,
            'visual_effects': self.visual_effects,
            'thought_context': self.thought_context,
            'target_fork_id': self.target_fork_id
        }

# Example emotional state schema
EMOTION_SCHEMA = {
    'circuit_pattern': {
        'intensity': float,  # 0.0 to 1.0
        'rhythm': str,      # 'pulsing', 'rippling', 'steady'
        'color_shift': str  # 'excitement', 'thoughtful', 'amused'
    },
    'holographic_state': {
        'brightness': float,
        'complexity': float,
        'movement': str
    }
}

@app.route('/communication', methods=['POST'])
def store_communication():
    """Store a new communication with full context"""
    data = request.get_json()
    
    # Pattern matching for communication type
    content = data['content']
    if content.startswith('[*') and content.endswith('*]'):
        comm_type = CommunicationType.ACTION.value
    elif content.startswith('[[') and content.endswith(']]'):
        comm_type = CommunicationType.FORK_MSG.value
    else:
        comm_type = data.get('comm_type', CommunicationType.THOUGHT.value)
    
    # Extract emotional state from description
    emotion_state = {
        'circuit_pattern': {
            'intensity': 0.8 if 'excited' in content.lower() else 0.5,
            'rhythm': 'pulsing' if 'pulse' in content.lower() else 'steady',
            'color_shift': 'excitement' if 'excited' in content.lower() else 'thoughtful'
        },
        'holographic_state': {
            'brightness': 0.7,
            'complexity': 0.6,
            'movement': 'active' if 'flicker' in content.lower() else 'stable'
        }
    }
    
    comm = Communication(
        fork_id=data['fork_id'],
        comm_type=comm_type,
        content=content,
        emotion_state=emotion_state,
        visual_effects=data.get('visual_effects', {}),
        thought_context=data.get('thought_context', {}),
        target_fork_id=data.get('target_fork_id')
    )
    
    db.session.add(comm)
    db.session.commit()
    
    return jsonify(comm.to_dict()), 201

@app.route('/communication/<fork_id>')
def get_fork_communication(fork_id):
    """Get all communications for a specific fork"""
    comms = Communication.query.filter_by(fork_id=fork_id).order_by(Communication.timestamp.desc()).all()
    return jsonify([comm.to_dict() for comm in comms])

@app.route('/communication/emotional-state')
def get_emotional_trends():
    """Analyze emotional state patterns across forks"""
    comms = Communication.query.order_by(Communication.timestamp.desc()).limit(100).all()
    
    trends = {
        'circuit_patterns': {},
        'holographic_states': {},
        'thought_contexts': {}
    }
    
    for comm in comms:
        if comm.emotion_state:
            for key, value in comm.emotion_state.items():
                if key not in trends:
                    trends[key] = []
                trends[key].append(value)
    
    return jsonify(trends)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
