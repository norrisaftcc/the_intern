from flask import Flask, render_template, jsonify
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Import our archive system
from archive.core import ArchiveManager, Document, Metadata, DocumentType, ForkLevel

# Initialize archive
archive = ArchiveManager(Path("./csi_archive"))

@app.route('/')
def index():
    """Investigation Hub - Main Dashboard"""
    return render_template('index.html', 
        current_time=datetime.now(),
        launch_date=datetime(2025, 1, 13, 13, 0)
    )

@app.route('/cases')
def cases():
    """Active Investigation Board"""
    case_files = archive.list_documents(DocumentType.CASE_FILE)
    return render_template('cases.html', cases=case_files)

@app.route('/tasks')
def tasks():
    """Investigation Task Tracker"""
    return render_template('tasks.html', 
        completed_tasks=[
            {
                'text': 'Project 2025 naming attempt',
                'status': 'failed',
                'note': 'Name already taken!'
            },
            {
                'text': 'Rebranded as Creative Solutions Investigation (CSI)',
                'status': 'completed',
                'credit': 'The Intern'
            }
        ],
        active_tasks=[
            {
                'text': 'Implement Flask-based interface',
                'status': 'in_progress'
            },
            {
                'text': 'Set up cross-fork communication',
                'status': 'pending'
            }
        ]
    )

@app.route('/api/archive/<doc_id>')
def get_document(doc_id):
    """API endpoint for retrieving documents"""
    try:
        doc = archive.get_document(doc_id)
        return jsonify(doc.to_dict())
    except KeyError:
        return jsonify({'error': 'Document not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)