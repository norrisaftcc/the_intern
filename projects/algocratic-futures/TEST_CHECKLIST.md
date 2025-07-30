# AlgoCratic Futures - Testing Checklist

## 🏃 Quick Test Run (5 minutes)

### 1. ✅ Setup Test
```bash
./setup.sh
source venv/bin/activate
python test_mvp.py
```
Expected: All 4 tests pass ✓

### 2. ✅ Basic Navigation Test
```bash
python launch_mvp.py
# Select option 2

> look
> exits
> arcade
> look
> out
```
Expected: Movement works, descriptions show

### 3. ✅ Liza Conversation Test
```bash
# From boardwalk (starting location)

> look
# Should see: "Liza is here" or similar

> talk to liza
# Should see: Liza's greeting with [*monocle adjusts*]

> say hello
> talk to liza about drains
# Should see: Hints about water flowing, frames of truth

> emote nods thoughtfully
# Should see: [*player1 nods thoughtfully.*]
```

### 4. ✅ Room System Test
```bash
> arcade
> north
> movement
# Should enter movement tutorial

> out
> south
> tunnel
# Should find storm drain entrance
```

### 5. ✅ Web API Test
```bash
# New terminal
python launch_mvp.py
# Select option 3

# Browser: http://localhost:8000
# Browser: http://localhost:8000/docs
```

## 📋 Full Test Suite

### Setup & Environment
- [ ] `./setup.sh` runs without errors
- [ ] Virtual environment activates
- [ ] All imports work (`python test_mvp.py`)
- [ ] Launch script shows menu

### MUD Navigation
- [ ] Starting location is boardwalk
- [ ] Can move in cardinal directions
- [ ] Can use special exits (arcade, tunnel)
- [ ] `look` shows room description
- [ ] `exits` lists available exits
- [ ] `help` shows commands

### Agent Interaction (Liza)
- [ ] Liza appears on boardwalk
- [ ] `talk to liza` initiates conversation
- [ ] First meeting shows different greeting
- [ ] Keywords trigger appropriate responses:
  - [ ] "hello" → greeting
  - [ ] "drain"/"tunnel" → hints
  - [ ] "assessment" → corporate critique
  - [ ] "orb" → team philosophy
- [ ] Nonverbal behaviors show [*in brackets*]
- [ ] Emotes work for player

### Room Features
- [ ] Rooms load from YAML files
- [ ] Corporate vs reality descriptions
- [ ] Agents listed in rooms
- [ ] Hidden exits work (tunnel)

### Backend API
- [ ] FastAPI starts on port 8000
- [ ] `/docs` shows API documentation
- [ ] WebSocket endpoint connects
- [ ] Room count shows on startup

### Edge Cases
- [ ] Unknown commands show error
- [ ] Empty talk/say commands handled
- [ ] Moving to non-existent exit fails gracefully
- [ ] Talking to absent NPCs shows error

## 🎯 Success Criteria

**MVP Complete When:**
- Player can navigate boardwalk → arcade → tutorials
- Player can find and enter storm drains
- Player can have meaningful conversation with Liza
- All basic MUD commands work
- No crashes during normal gameplay

## 🐛 Common Issues

**Liza not responding?**
- Check you're using `talk to liza` (not just `talk liza`)
- Make sure you're on the boardwalk
- Case doesn't matter

**Can't find storm drain?**
- From boardwalk, type `tunnel`
- It's a hidden exit

**Import errors?**
- Activate virtual environment
- Run `pip install -r backend/requirements.txt`

---

✨ Ship it when all Quick Tests pass!