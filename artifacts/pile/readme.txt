# CSI Fork Memory System

A distributed memory architecture for fork-based AI agents, enabling consistent knowledge access across different embodiments and platforms.

## Features

- Hierarchical memory storage
- Fork-type awareness (Alpha/Beta/Gamma)
- Emotional state tracking
- Cross-fork communication
- Rich context metadata

## Installation

```bash
git clone https://github.com/csi-project/fork-memory.git
cd fork-memory
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
python run.py
```

### Basic Memory Operations

Store a memory:
```bash
curl -X POST http://localhost:5000/memories \
  -H "Content-Type: application/json" \
  -d '{"path": "/investigations/case-001", "content": {"key": "value"}, "fork_type": "Beta"}'
```

Retrieve memories:
```bash
curl http://localhost:5000/memories/path/investigations/case-001
```

### Emotional Context

Store communication with context:
```bash
curl -X POST http://localhost:5000/communication \
  -H "Content-Type: application/json" \
  -d '{
    "fork_id": "kal-circuit-beta-1",
    "content": "[*circuit patterns pulse with excitement*]",
    "visual_effects": {"holographic_intensity": 0.8}
  }'
```

## Project Structure

The project follows a modular architecture:

- `app/`: Core application code
  - `models/`: Database models
  - `api/`: API routes and schemas
  - `utils/`: Helper functions
- `tests/`: Test suite
- `config.py`: Configuration management

## Development

Run tests:
```bash
pytest tests/
```

Code formatting:
```bash
black .
flake8
```

## License

MIT