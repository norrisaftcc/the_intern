# Backlog Priorities - AlgoCratic Futures MVP

## 🎯 Sprint 0: Ship Core Value (THIS WEEK)

### P0 - CRITICAL PATH (Do These First, In Order)
1. **WebSocket Connection** [2-4 hrs]
   - Wire `frontend/app.js` to `backend/enhanced_websocket.py`
   - Route terminal commands through WebSocket
   - Test with single player
   - **Why Critical**: Unlocks web UI, enables remote play

2. **Ollama Integration** [1-2 hrs]
   - Replace mock responses in `agent_system.py:68`
   - Use llama2:7b for Beta tier (Liza)
   - Fallback to mock if Ollama unavailable
   - **Why Critical**: Makes NPCs actually interactive

3. **Room Authoring Guide** [30 min]
   - Create `docs/ROOM_AUTHORING_GUIDE.md` with template
   - Add 2-3 example rooms
   - **Why Critical**: Enables content creation by non-devs

### P1 - NICE TO HAVE (If Time Permits)
4. **Basic Persistence** [2 hrs]
   - Save player position between sessions
   - Use existing SQLite database
   - **Why P1**: Not critical for demo/testing

## ❌ CUT FROM MVP (Move to Backlog)

### Complexity Not Worth It Right Now
- ~~AI code review workflow~~ - GitHub Actions complexity
- ~~Personality states for NPCs~~ - Tier system sufficient
- ~~Broken cabinet tutorial~~ - Rooms work, focus on core
- ~~Annual report generation~~ - Feature creep
- ~~Advanced clearance progression~~ - Current system works
- ~~Full multiplayer~~ - Single player + spectators enough

### Already Working Well Enough
- ~~Fix TODO/FIXME items~~ - Only 3 items, all non-critical
- ~~Document everything~~ - CLAUDE.md and AGENT_STARTUP.md sufficient

## 📊 Success Metrics

MVP is DONE when:
- [ ] Player can access game via web browser
- [ ] Liza responds dynamically using Ollama
- [ ] Non-technical person can add a room using guide
- [ ] No crashes during 15-minute play session

## 🚀 Post-MVP Roadmap (Next Sprint)

### Sprint 1: Polish & Scale
1. Multiplayer testing (2+ simultaneous players)
2. Session persistence (remember progress)
3. 3-5 more NPCs with different personalities
4. Tutorial room sequence

### Sprint 2: Enhancement
1. Achievement system
2. Clearance progression mechanics
3. More hidden areas
4. Sound effects/music

### Sprint 3: Assessment Features
1. Instructor dashboard
2. Student progress tracking
3. Report generation
4. Analytics

## 💀 Killed Features (Do Not Resurrect)

These seemed good but add complexity without proportional value:

- **Complex WebSocket state management** - Keep it simple
- **Real-time collaborative editing** - Not a Google Doc
- **3D visualization** - This is a text MUD
- **Blockchain integration** - Just... no
- **Microservices architecture** - Monolith is fine
- **React rewrite** - Vanilla JS works
- **TypeScript migration** - Not now
- **Docker orchestration** - python app.py is enough
- **CI/CD pipeline** - Manual testing sufficient for MVP

## 📝 Task Sizing Guide

**Small (30 min - 2 hrs)**
- Documentation updates
- Adding room files
- Simple bug fixes
- Adding NPC responses

**Medium (2-4 hrs)**  
- WebSocket integration
- Database connections
- New command handlers
- Test coverage

**Large (4-8 hrs)**
- Multiplayer system
- New game mechanics
- Frontend overhaul
- AI model training

**Too Large (Break Apart)**
- "Rewrite the system"
- "Make everything perfect"
- "Add all features"

## 🎪 The Three-Ring Rule

Every sprint should have:
1. **One Big Thing** - The main feature (WebSocket)
2. **Two Medium Things** - Supporting features (Ollama, Docs)
3. **Three Small Things** - Quick wins (bug fixes, responses)

Current Sprint:
1. Big: WebSocket connection
2. Medium: Ollama integration, Room authoring guide
3. Small: (Available for bug fixes discovered during implementation)

## ⚡ Quick Decision Framework

When deciding whether to add something:

**YES if:**
- Fixes a crash
- Enables other people to contribute
- Takes < 2 hours
- Directly improves player experience

**NO if:**
- "Would be cool if..."
- Requires new dependencies
- Changes core architecture
- Only benefits hypothetical users

**MAYBE if:**
- Multiple people request it
- Becomes bottleneck for testing
- Simplifies existing complexity

## 🔥 Current Fire Drills

*None!* The system is stable. Focus on shipping the P0 items.

## 📅 Timeline

**Week 1 (Current)**
- Day 1-2: WebSocket connection
- Day 3: Ollama integration  
- Day 4: Room authoring guide
- Day 5: Testing & polish

**Week 2**
- Gather feedback
- Fix critical bugs only
- Plan Sprint 1 based on actual usage

## 🏁 Definition of MVP Done

The MVP is complete when someone can:
1. Open a web browser
2. Connect to the game
3. Navigate rooms
4. Have a meaningful conversation with Liza
5. Find the hidden storm drains
6. Play for 15 minutes without crashes

That's it. Everything else is Sprint 1+.

---

*"Ship value, not features. Ship learning, not complexity."*