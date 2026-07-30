# CLAUDE.md - AI Assistant Context for AlgoCratic Futures

## Project Overview
AlgoCratic Futures is an educational assessment platform disguised as a dystopian corporate employee portal. It's a MUD (Multi-User Dungeon) that uses roleplay and satire to create an engaging learning environment where student progress is tracked as "productivity metrics."

## Core Philosophy
- **Educational Satire**: We critique surveillance capitalism while teaching real skills
- **Immersive Assessment**: Learning objectives hidden behind corporate dystopian themes
- **Player Agency**: Students explore at their own pace through the storm drains

## Critical System Context

### The Sacred Clearance System (DO NOT MODIFY)
```
R (Red) → O (Orange) → Y (Yellow) → G (Green) → B (Blue) → I (Indigo) → V (Violet) → UV (Ultraviolet)
```
This hierarchy comes from the original `core.pl.py` and must be preserved. Green clearance = Project Management track.

### Architecture Overview
```
Terminal MUD → Room System (YAML) → Agent System → Future WebSocket Layer
     ↓              ↓                    ↓
  Player Input   Room Files         Liza (NPC)      Real-time Updates
```

## Current Working State
✅ **What's Working:**
- Terminal-based MUD with room navigation
- YAML-based room system with corporate/reality dual descriptions
- Liza agent with tiered personality responses
- Basic conversation system with keyword triggers
- Test suite passing (4/4 tests)

⚠️ **What's Partially Working:**
- Frontend exists but WebSocket not connected
- Database exists but not fully integrated
- Agent tiers implemented but using mock responses

❌ **What's Not Working:**
- WebSocket connection between frontend and backend
- PocketFlow/Ollama integration for AI responses
- Multiplayer functionality
- Persistence between sessions

## File Structure That Matters
```
backend/
  app.py                 # FastAPI server (WebSocket endpoint exists)
  terminal_mud.py        # Main game loop
  terminal_integration.py # Command processor
  room_system.py         # Room loader and navigation
  agent_system.py        # NPC conversation engine
  agent_prompts_tiered.py # Personality tiers (Alpha→Delta)
  
frontend/
  index.html            # Corporate portal UI
  app.js               # WebSocket client (needs connection)
  
rooms/
  boardwalk_arcade/    # Starting area with Liza
  anonymous_sysop/     # Storm drain hidden areas
```

## Key Technical Decisions

### Why Terminal First?
- Faster iteration and testing
- No WebSocket complexity initially
- Pure text interface matches MUD heritage
- Can add web layer incrementally

### Why YAML for Rooms?
- Human-readable for non-programmers
- Easy for writers to contribute content
- Supports complex nested structures
- Git-friendly for version control

### Why Tiered Agent System?
- Allows degradation when AI unavailable
- Different model sizes for different NPCs
- Cost-effective (smaller models for simpler agents)
- Ollama ready: Alpha (mixtral), Beta (llama2:7b), Gamma (phi), Delta (tinyllama)

## Priority Tasks (What Ships Value)

### 🚢 SHIP NOW (MVP Critical)
1. **Fix WebSocket Connection** - Frontend exists, just needs wiring
2. **Connect Ollama** - Local models ready, just needs integration
3. **Document Room Authoring** - Enable content creators

### 📦 SHIP SOON (Post-MVP)
4. Test multiplayer with 2+ terminals
5. Add persistence to database
6. Implement broken cabinet tutorial

### 🗄️ DEFER (Nice to Have)
7. AI code review for large PRs
8. Personality states for NPCs
9. Annual report generation
10. Advanced clearance progression

## Quick Command Reference

### Start the System
```bash
cd backend
source venv/bin/activate  # If venv exists
python launch_mvp.py      # Shows menu
```

### Test Everything
```bash
python test_mvp.py        # Quick validation
python app.py            # Start API server
```

### Common Issues & Solutions

**Liza not responding?**
- Use `talk to liza` not just `talk liza`
- Make sure you're on the boardwalk
- Check agent_system.py line 68 (TODO: PocketFlow)

**Can't find storm drain?**
- From boardwalk, type `tunnel`
- It's a hidden exit (won't show in normal exits list)

**WebSocket not connecting?**
- Backend WebSocket exists at ws://localhost:8000/ws/{id}
- Frontend tries to connect but no handler wired up
- See app.js line 42 and backend/enhanced_websocket.py

## Code Smells to Watch For

1. **Hardcoded player ID**: Currently "player1" everywhere
2. **Mock AI responses**: agent_system.py returns canned responses
3. **No session management**: Each run starts fresh
4. **Terminal-only multiplayer**: WebSocket needed for real multiplayer

## Testing Checklist

Before committing:
1. Run `python test_mvp.py` - all 4 tests should pass
2. Start game, navigate rooms, talk to Liza
3. Check that hidden exits work (tunnel from boardwalk)
4. Verify no import errors in any module

## The Story So Far

This started as a Perl MUD about clearance levels, evolved into an educational assessment platform, and is now becoming a multiplayer learning environment. The storm drains represent the "real" system beneath the corporate facade - where actual learning happens away from surveillance metrics.

Sweeney (Green clearance/PM) is leading development. Kevin offered GitHub automation help. Other interns are MIA or responding cryptically. The codebase is intentionally dystopian but must remain obviously satirical.

## Remember

- **Preserve the clearance system** - It's sacred legacy code
- **Keep the satire obvious** - We critique, not promote surveillance  
- **Test at 3 AM** - For authentic Sweeney mode experience
- **Some code is too pure to refactor** - Ancient MUD proverb

## Contact & Context

- Main repo: `/Users/norrisa/Documents/dev/github/the_intern`
- Project home: `projects/algocratic-futures/`
- Current branch: `feature/algocratic-base-platform`
- Last standup: See `docs/STANDUP_NOTES.md`

---

*"Your Learning is Our Asset" - AlgoCratic Futures Corporate Motto*