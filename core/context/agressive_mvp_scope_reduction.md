# Aggressive MVP Scope Reduction for Robot-Only Avatar System

## Components to completely ignore

Based on my analysis of the NOM Network repositories, here are the entire repositories and major components you should **completely remove**:

### 1. **Entire Repositories to Delete:**
- **Melba-Toaster** - The entire Godot/Live2D frontend (80-90% complexity reduction)
- **melba-stt** - Discord voice transcription bot (not needed for robots)
- **Twitchchat_Reader** - Twitch integration (entertainment-focused)
- **melba-tts** - Custom voice synthesis (use standard TTS instead)

### 2. **Major Subsystems to Remove:**
- **Live2D Cubism SDK** and all dependencies
- **Godot Engine** integration
- **NRCLex emotion analysis** library
- **Spout2/OBS** streaming integration
- **Discord/Twitch** integrations
- **Custom voice models** (singing, TTS v2/v3)
- **Control Panel** UI system

## Files and features to delete from kept components

### From **melba-backend**:
- All Live2D parameter sync code
- Emotion blending algorithms
- Physics simulation components
- Complex animation interpolation
- Breathing/idle animation systems
- WebSocket messages for organic avatars:
  - `breath_animation_start/stop`
  - `facial_expression_blend`
  - `physics_parameter_update`
  - `live2d_parameter_sync`
  - `complex_emotion_transition`

### From **Melba-Toast-AI**:
- NRCLex emotion analysis integration
- Personality modeling systems
- Complex voice synthesis hooks
- Streaming consciousness features
- Entertainment-focused prompts

## Minimal architecture diagram

```
┌─────────────────────┐
│   Robot Hardware    │
│  (LED eyes, servos) │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Robot Controller   │
│  (Python FastAPI)   │
│  - State machine    │
│  - Hardware control │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  PocketFlow Agent   │
│  + Ollama Backend   │
│  (Local LLM)        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   Simple TTS        │
│  (edge-tts/espeak) │
└─────────────────────┘
```

### Core Components (3 files total):
1. **robot_backend.py** - FastAPI server with WebSocket support
2. **agent_manager.py** - PocketFlow multi-agent orchestration
3. **hardware_interface.py** - Robot control (LEDs, servos)

## Realistic 1-week timeline with daily goals

### **Day 1: Environment Setup & Core Backend**
- Install PocketFlow + Ollama
- Create minimal FastAPI backend
- Implement basic WebSocket communication
- Test LLM integration with simple prompts

### **Day 2: Hardware Interface**
- Build hardware abstraction layer
- Implement LED control system (RGB values, patterns)
- Add servo control for mechanical movements
- Create state machine (idle, listening, speaking, thinking)

### **Day 3: Multi-Agent Architecture**
- Implement PocketFlow graph for multi-agent coordination
- Create specialized agents (conversation, task, knowledge)
- Build agent communication protocol
- Test multi-agent interactions

### **Day 4: Audio Integration**
- Integrate edge-tts or espeak for robot voice
- Implement audio output queue
- Add basic STT if needed (optional)
- Test full conversation loop

### **Day 5: Robot Personality & Testing**
- Define robot character templates
- Create simple personality system (no emotions)
- Build example robot personas
- Integration testing

### **Day 6: Polish & Documentation**
- Error handling and recovery
- Performance optimization
- Create setup scripts
- Write basic documentation

### **Day 7: Demo & Examples**
- Build 2-3 example robot characters
- Create demo scenarios
- Record demonstration videos
- Package for release

## Absolute minimum viable feature set

### **Core Features Only:**

1. **LLM Integration**
   - Single Ollama connection
   - Basic prompt engineering
   - 2-3 agent types maximum

2. **Robot Control**
   - LED eyes (color, brightness)
   - 3-5 servo positions
   - Simple state indicators

3. **Communication**
   - Text input via API
   - Text-to-speech output
   - Basic WebSocket for real-time

4. **Multi-Agent Capability**
   - Coordinator agent
   - 2 specialist agents
   - Simple message passing

### **What You DON'T Need:**
- Visual avatars
- Emotion modeling
- Streaming features
- Chat integrations
- Complex animations
- Voice synthesis
- Control panels
- Live2D anything

### **Recommended Starting Point:**

Look at the existing **melba-mini** repository - it's already described as a "smaller alternative to Melba-Toast-AI" and likely contains a simplified version you can further strip down.

### **Initial File Structure:**
```
robot-avatar-mvp/
├── robot_backend.py      # 150 lines
├── agent_manager.py      # 100 lines  
├── hardware_interface.py # 100 lines
├── config.yaml          # 20 lines
├── requirements.txt     # 10 lines
└── examples/
    ├── led_robot.py
    └── servo_robot.py
```

### **Total Complexity Reduction:**
- **90% fewer dependencies**
- **85% less code**
- **From 7 services to 1**
- **From 4 languages to 1 (Python)**
- **Setup time: Days → Hours**

This aggressive reduction maintains the core value proposition (AI-powered robot avatars with multi-agent capability) while eliminating all the complexity designed for organic VTuber avatars.