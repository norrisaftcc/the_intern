# AlgoCratic Futures - Immersive Assessment Platform

> "Your Learning is Our Asset"

## Quick Start (for the interns)

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (just open in browser for now)
open frontend/index.html
```

## What This Is

An educational roleplay assessment system disguised as a dystopian corporate employee portal. Students/players work at "AlgoCratic Futures" where their learning progress is tracked as productivity metrics.

## Core Components

### 1. Clearance System (SACRED - DO NOT MODIFY)
- Preserves original ROYGBIV/UV hierarchy from `core.pl.py`
- R (Red) through UV (Ultraviolet) clearance levels
- Green = Project Management track (that's you Sweeney!)

### 2. Assessment Methods
- **Peer Surveillance Reports** - Students evaluate each other in character
- **Productivity Dashboards** - Real-time learning analytics 
- **Corporate Evaluations** - Instructor feedback as performance reviews
- **Annual Reports** - Portfolio generation as shareholder reports

### 3. Current Status
- ✅ Basic backend API (FastAPI)
- ✅ Terminal-based frontend 
- ✅ WebSocket real-time updates
- ✅ Clearance system integration
- 🚧 PocketFlow integration needed
- 🚧 Database persistence
- 🚧 Annual report generation

## For New Interns

1. **Read the context doc** about educational roleplay assessment
2. **Preserve the clearance system** - it's based on the original Perl code
3. **Maintain the dystopian theme** but remember it's satire/critique
4. **All metrics must map to real learning objectives**

## PocketFlow Integration Points

Need to connect:
- Local model endpoints for AI-driven assessments
- Real-time metrics processing
- Natural language evaluation of student submissions
- Automated report generation

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Web Frontend  │────▶│  FastAPI Backend │────▶│  Legacy Bridge  │
│  (Terminal UI)  │     │  (Assessment API)│     │ (Perl clearance)│
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                         │
         └───────────────────────┴─────────────────────────┘
                                 │
                          ┌──────▼────────┐
                          │  PocketFlow   │
                          │ (Local Models)│
                          └───────────────┘
```

## Sweeney Mode

Activated between 2-5 AM. Features:
- Enhanced debug logging
- Reality distortion effects
- Coffee level warnings
- "Understanding the code" achievement at 48+ hours

## Next Steps

1. Set up proper database (SQLite → PostgreSQL)
2. Implement full surveillance report system
3. Create annual report generator with visualizations
4. Add more terminal commands
5. Build instructor dashboard
6. Integration tests

## Contributing

- Follow the dystopian naming conventions
- Keep the satire obvious (we're critiquing surveillance, not promoting it)
- Document any new "corporate policies" (game mechanics)
- Test at 3 AM for authentic Sweeney mode experience

---

*"Some code is too pure to refactor" - Ancient MUD Proverb*