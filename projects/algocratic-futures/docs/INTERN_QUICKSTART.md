# Intern Quick Start Guide

Welcome to AlgoCratic Futures, employee. Your onboarding is mandatory.

## Getting Started in 5 Minutes

### 1. Clone and Setup
```bash
git clone [repo]
cd projects/algocratic-futures
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

### 2. Run the Backend
```bash
cd backend
python app.py
# Server starts on http://localhost:8000
```

### 3. Open Frontend
```bash
# In another terminal
cd frontend
# Just open index.html in a browser (Chrome recommended)
# Or use Python's simple server:
python -m http.server 8080
```

## Key Files to Understand

1. **backend/clearance_system.py** - The sacred clearance logic (READ, don't modify)
2. **backend/app.py** - Main API endpoints
3. **frontend/app.js** - Terminal interface and WebSocket client
4. **core/root/core.pl.py** - Original Perl system (for reference)

## Your First Task

1. Open the web interface
2. Type `help` in the terminal
3. Try `clock in` to start your shift
4. File a surveillance report with `report EMP-123`
5. Check your metrics with `status`

## Important Context

This is an **educational roleplay system** where:
- Students play employees at a dystopian corporation
- Learning objectives are disguised as "productivity metrics"
- It's satire/critique of surveillance capitalism
- Every dystopian element serves an educational purpose

## Code Style Guide

### Backend (Python)
```python
# Use dystopian variable names that hint at real purpose
productivity_score = 85  # Actually: assignment completion rate
loyalty_index = 92       # Actually: collaboration score
algorithmic_thinking = 78 # Actually: problem-solving assessment
```

### Frontend (JavaScript)
```javascript
// Corporate doublespeak in comments
this.fileReport(targetId); // Peer assessment disguised as surveillance
this.updateMetric('loyalty', 10); // Reward collaborative behavior
```

## Common Tasks

### Add a New Terminal Command
1. Edit `frontend/app.js`
2. Add to the `commands` object in `processCommand()`
3. Update the help text

### Add a New API Endpoint
1. Edit `backend/app.py`
2. Follow the dystopian naming convention
3. Return data in corporate speak

### Create a New Assessment Method
1. Design the in-world justification
2. Map to real learning objectives
3. Implement collection mechanism
4. Add visualization to dashboard

## Debugging Tips

- Check browser console for WebSocket errors
- Backend logs show all "surveillance" activity
- Use `sweeney mode` command between 2-5 AM
- Clearance advancement is based on real metrics

## Need Help?

- Read the main README.md
- Check the educational context document
- Look at the original Perl code for clearance logic
- Ask PM Sweeney (Green clearance, manages the chaos)

## Remember

You're building an educational tool that:
1. Teaches real skills (programming, collaboration, critical thinking)
2. Critiques surveillance and commodification
3. Maintains narrative coherence
4. Makes assessment engaging

---

*"Your contribution to the Algorithm is noted and appreciated"*