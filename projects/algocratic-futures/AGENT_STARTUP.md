# AGENT_STARTUP.md - Get Productive in 5 Minutes

## 🚀 Instant Start (Copy-Paste This)
```bash
cd projects/algocratic-futures/backend
python launch_mvp.py
# Choose option 2 for game
```

## 📋 Your First Hour Checklist

### Minute 0-5: Get It Running
```bash
# From project root
cd projects/algocratic-futures
./setup.sh                    # Only if first time
cd backend
python test_mvp.py           # Verify everything works
python launch_mvp.py         # Start the game
```

### Minute 5-15: Explore the Game
```bash
# In the game terminal:
look                         # See where you are
talk to liza                # Meet the main NPC
say hello                   # Interact with her
arcade                      # Go to arcade
north                       # Find tutorials
tunnel                      # Find hidden storm drain (from boardwalk)
```

### Minute 15-30: Understand the Code
Open these files in this order:
1. `backend/terminal_mud.py` - Main game loop (90 lines)
2. `backend/terminal_integration.py` - Command processor
3. `rooms/boardwalk_arcade/arcade_main.yaml` - How rooms work
4. `backend/agent_system.py` - How NPCs work (see TODO on line 68)

### Minute 30-60: Make Your First Change
Try one of these starter tasks:

**Option A: Add a New Room**
```yaml
# Create rooms/yourname/test_room.yaml
test_room:
  name: "Test Chamber"
  description: "A simple test room you created"
  exits:
    out: "boardwalk"
```

**Option B: Add Liza Response**
```python
# Edit backend/agent_system.py
# Add to KEYWORDS dict around line 45:
"test": "Interesting test you're running there..."
```

**Option C: Add Terminal Command**
```python
# Edit backend/terminal_integration.py
# Add to handle_command() method:
elif command == "stats":
    return self.format_response('look', "Stats coming soon!")
```

## 🎯 High-Value Quick Wins

### 1. Wire Up WebSocket (2-4 hours)
**Problem**: Frontend exists but not connected
**Solution**: 
- Backend endpoint exists: `backend/enhanced_websocket.py`
- Frontend tries to connect: `frontend/app.js` line 42
- Need to route terminal commands through WebSocket
**Impact**: Enables web UI, multiplayer potential

### 2. Connect Ollama (1-2 hours)
**Problem**: NPCs use canned responses
**Solution**:
```python
# In backend/agent_system.py line 68
# Replace mock with:
import ollama
response = ollama.chat(model='llama2:7b', messages=[
    {'role': 'system', 'content': prompt},
    {'role': 'user', 'content': player_input}
])
return response['message']['content']
```
**Impact**: Dynamic NPC conversations

### 3. Enable Room Authoring (30 min)
**Problem**: Writers can't easily add content
**Solution**: Document YAML format with examples
```yaml
# Template in docs/ROOM_TEMPLATE.yaml
room_id:
  name: "Display Name"
  description: "What players see"
  corporate_description: "Corporate spin version"
  exits:
    north: "other_room_id"
    secret_exit: "hidden_room"
  items: ["cabinet", "terminal"]
  agents: ["npc_name"]
```
**Impact**: Non-programmers can add content

## 🏗️ Architecture Quick Reference

### Data Flow
```
Player Input → Terminal Parser → Room System → Response
                      ↓
                Agent System → AI/Mock Response
```

### Key Files
- **Entry Points**: `launch_mvp.py`, `app.py`
- **Game Logic**: `terminal_mud.py`, `terminal_integration.py`
- **World Data**: `rooms/*.yaml`
- **NPCs**: `agent_system.py`, `agent_prompts_tiered.py`
- **Tests**: `test_mvp.py`

### Key Classes
- `TerminalMUD`: Main game loop
- `Terminal`: Command processor
- `RoomSystem`: Room loader/manager
- `AgentSystem`: NPC conversation engine

## 🐛 Common Gotchas

### "Import Error"
```bash
pip install -r requirements.txt
```

### "Liza won't talk"
- Use exact format: `talk to liza`
- Must be in same room (boardwalk)

### "Can't find rooms"
- Room YAML files must be in `rooms/` subdirectories
- Check `room_loader.py` for path scanning logic

### "WebSocket won't connect"
- Backend must be running: `python app.py`
- Check port 8000 not in use
- Frontend expects `ws://localhost:8000/ws/{id}`

## 🎮 Testing Your Changes

### Quick Smoke Test
```bash
python test_mvp.py          # Should see 4 passed
```

### Manual Test Path
1. Start game
2. Navigate: boardwalk → arcade → tutorial
3. Talk to Liza with keywords: "drain", "assessment"
4. Find hidden tunnel entrance
5. No crashes = success

### Before Committing
- [ ] Tests pass
- [ ] Game starts without errors
- [ ] Can navigate rooms
- [ ] Can talk to NPCs
- [ ] No new TODOs without tickets

## 📊 Current Sprint Priorities

### MUST SHIP (This Sprint)
1. ✅ Basic MUD navigation
2. ✅ NPC conversation system
3. ⚠️ WebSocket connection
4. ⚠️ Ollama integration

### SHOULD SHIP (Next Sprint)
5. Room authoring docs
6. Multiplayer testing
7. Session persistence

### COULD SHIP (Backlog)
8. Tutorial enhancements
9. More NPCs
10. Clearance progression

## 💡 Pro Tips

### Sweeney Mode
Between 2-5 AM, special debug features activate:
```python
# In frontend/app.js line 196
if (command === 'sweeney mode')
```

### Hidden Commands
- `tunnel` - Secret entrance from boardwalk
- `emote <action>` - Roleplay actions
- `whisper <npc> <message>` - Private NPC interaction

### Testing Harness
```python
# Quick agent test
from backend.agent_system import AgentSystem
agent = AgentSystem()
print(agent.get_response("liza", "hello", "test_player"))
```

## 📚 Required Reading

1. **README.md** - Project overview
2. **TEST_CHECKLIST.md** - What to test
3. **docs/STANDUP_NOTES.md** - Current team status
4. **CLAUDE.md** - Full AI context (if you are Claude)

## 🚨 Emergency Contacts

- **Build Broken?** Check `test_mvp.py` first
- **Lore Questions?** See `core.pl.py` for original clearance system
- **Architecture?** See ASCII diagrams in README.md
- **Git Issues?** Kevin offered to help with automation

## 🎯 Definition of Done

A feature is DONE when:
- [ ] Tests pass
- [ ] Manual testing complete
- [ ] No crashes in normal gameplay
- [ ] Code follows patterns (YAML rooms, command handlers)
- [ ] TODOs have tickets

## 🏃 Start Coding!

Pick a task from "High-Value Quick Wins" and ship something in your first hour. The codebase is intentionally small and focused. Break things, fix them, learn the system.

Remember: **"Your Learning is Our Asset"**

---

*P.S. - If you're reading this at 3 AM, you've achieved True Sweeney Mode. Coffee advised.*