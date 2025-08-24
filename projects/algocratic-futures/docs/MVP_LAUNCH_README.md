# AlgoCratic Futures - MVP Launch Guide

## Quick Start

```bash
cd projects/algocratic-futures
python launch_mvp.py
```

Choose:
1. **Terminal MUD** - Pure text adventure with adventurelib
2. **Web Interface** - Full dystopian corporate experience  
3. **Both** - Run everything (recommended)

## What's Working

### Boardwalk Arcade MVP
- ✅ Basic movement (n/s/e/w and special exits)
- ✅ Look/examine commands
- ✅ Take/drop items (tickets!)
- ✅ Tutorial rooms teaching commands
- ✅ Hidden storm drain entrance

### Using adventurelib
- Simple command parsing with @when decorators
- Room connections without complex graphs
- Inventory management built-in
- Perfect for quick text adventure MVP

## Architecture Notes

### Current Simplifications
- Hardcoded rooms (not loading from YAML yet)
- Basic clearance system (just tracking, not enforcing)
- No persistence (resets on restart)
- Agents not integrated yet

### Future Enhancements
- Load rooms from YAML files
- Connect agent system
- Use PocketFlow for agent behavior graphs/FSMs
- Add WebSocket for multiplayer
- Integrate with Evennia eventually

## Testing the Tutorial

1. Start at boardwalk
2. Go `arcade` to enter
3. Go `north` to main hall
4. Try `movement` to learn movement
5. Get `ticket` for rewards
6. Explore other tutorials

## For Developers

The MVP uses:
- **adventurelib** for command parsing
- **FastAPI** for web backend
- **Simple Room objects** for locations
- **Basic game state** tracking

Next steps:
- Wire up room loader
- Add agent interactions
- Test with real players
- Iterate based on feedback

---

*"Ship the arcade, perfect it later"*