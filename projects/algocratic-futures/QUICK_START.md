# AlgoCratic Futures - Quick Start Guide

## 🚀 Fastest Setup (2 minutes)

```bash
# Clone and enter project
git clone https://github.com/norrisaftcc/the_intern.git
cd the_intern/projects/algocratic-futures

# Run automated setup
./setup.sh

# Launch the game
source venv/bin/activate
python launch_mvp.py
```

## 🎮 What to Try First

### Option 2: Meet Liza on the Boardwalk
```
python launch_mvp.py
Select option: 2

> look
You're on the boardwalk. Liza is here!

> talk to liza
[*Monocle adjusts, displaying cascading data*]
Dr. Anderson here, though please - call me LIZA...

> say hello
> talk to liza about storm drains
> emote waves
```

### Key Commands
- **Movement**: `n`, `s`, `e`, `w`, or exit names like `arcade`
- **Looking**: `look`, `look at [thing]`
- **Talking**: `talk to liza`, `say [message]`
- **Actions**: `emote [action]`
- **Help**: `help`

## 🗺️ Quick Map

```
Boardwalk (START - Liza is here!)
    |
    ├── arcade → Arcade Entrance → Tutorial Games
    |
    └── tunnel → Storm Drains (hidden - the real game!)
```

## 🎯 Goals

1. **Talk to Liza** - She gives hints about the true nature of things
2. **Find the Storm Drains** - Hidden entrance on boardwalk
3. **Complete Arcade Tutorials** - Learn all MUD commands
4. **Explore** - Each room has corporate/reality descriptions

## 🐛 Quick Troubleshooting

**Can't find Liza?**
- You start on the boardwalk
- Type `look` to see who's there
- Use `talk to liza`

**Import errors?**
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

**Want to see code in action?**
```bash
# Terminal 1: Watch the backend
cd backend && python app.py

# Terminal 2: Play the game
python terminal_mud.py
```

## 💡 Tips

- Liza speaks in animation metaphors
- [*Actions appear in brackets*]
- [[Double brackets are internal thoughts]]
- The corporate descriptions hide the truth
- Storm drains lead to the real game

---

*"Your Learning is Our Asset"* 🏢

Need full docs? See README.md