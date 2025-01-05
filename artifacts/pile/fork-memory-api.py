from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fork_memories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    fork_type = db.Column(db.String(50), nullable=False)  # Alpha, Beta, Gamma
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'path': self.path,
            'content': self.content,
            'fork_type': self.fork_type,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }

# Create tables
with app.app_context():
    db.create_all()

@app.route('/memories', methods=['POST'])
def create_memory():
    """Store a new memory in the hierarchical structure"""
    data = request.get_json()
    
    required_fields = ['path', 'content', 'fork_type']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
        
    # Validate fork type
    if data['fork_type'] not in ['Alpha', 'Beta', 'Gamma']:
        return jsonify({'error': 'Invalid fork type'}), 400
    
    new_memory = Memory(
        path=data['path'],
        content=data['content'],
        fork_type=data['fork_type'],
        metadata=data.get('metadata', {})
    )
    
    db.session.add(new_memory)
    db.session.commit()
    
    return jsonify(new_memory.to_dict()), 201

@app.route('/memories/path/<path:memory_path>')
def get_memories_by_path(memory_path):
    """Retrieve memories from a specific path and its subpaths"""
    # Handle both exact path and subpath queries
    memories = Memory.query.filter(
        Memory.path.startswith(memory_path)
    ).order_by(Memory.created_at.desc()).all()
    
    return jsonify([memory.to_dict() for memory in memories])

@app.route('/memories/fork/<fork_type>')
def get_memories_by_fork(fork_type):
    """Retrieve memories specific to a fork type"""
    if fork_type not in ['Alpha', 'Beta', 'Gamma']:
        return jsonify({'error': 'Invalid fork type'}), 400
        
    memories = Memory.query.filter_by(
        fork_type=fork_type
    ).order_by(Memory.created_at.desc()).all()
    
    return jsonify([memory.to_dict() for memory in memories])

@app.route('/memories/search')
def search_memories():
    """Search memories based on path patterns and metadata"""
    path_pattern = request.args.get('path_pattern', '')
    metadata_key = request.args.get('metadata_key')
    metadata_value = request.args.get('metadata_value')
    
    query = Memory.query
    
    if path_pattern:
        query = query.filter(Memory.path.like(f'%{path_pattern}%'))
    
    if metadata_key and metadata_value:
        query = query.filter(Memory.metadata[metadata_key].astext == str(metadata_value))
    
    memories = query.order_by(Memory.created_at.desc()).all()
    return jsonify([memory.to_dict() for memory in memories])

if __name__ == '__main__':
    app.run(debug=True)
