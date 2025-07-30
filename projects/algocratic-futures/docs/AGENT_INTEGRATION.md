# Agent Integration Guide

## Overview

The AlgoCratic Futures system includes AI agents that play various roles in the dystopian corporate roleplay. Each agent has a specific personality, clearance level, and purpose.

## Current Agents

### Core Team
- **Liza** (Green/G) - Friendly mentor, helps new employees navigate the system
- **Vi** (Orange/O) - Peer agent, provides solidarity and practical tips
- **Wyatt** (Yellow/Y) - Street-smart colleague who knows the shortcuts
- **Kai** (Blue/B) - Technical expert, teaches advanced concepts

### System Agents
- **Performance Evaluator Alpha** - Assesses productivity metrics
- **Senior Associate Chen** - Green wizard mentor (tired but helpful)
- **Compliance Officer Zhang** - Tests loyalty and enforces rules
- **Subprocess Claude** - Technical code reviewer (that's me!)

## Agent Architecture

```
┌─────────────────┐
│   Agent Core    │ <- Personality, clearance, directives
└────────┬────────┘
         │
┌────────▼────────┐
│     Agent       │ <- Active instance with memory
└────────┬────────┘
         │
┌────────▼────────┐
│ Agent Manager   │ <- Orchestrates all agents
└────────┬────────┘
         │
┌────────▼────────┐
│   PocketFlow    │ <- LLM processing (when connected)
└─────────────────┘
```

## Loading Agents

### From Templates (Currently Available)
```python
from agent_templates import create_agent_from_template
from agent_system import Agent

# Create Liza
liza_core = create_agent_from_template("liza")
liza = Agent(liza_core)

# Get a response
response = await liza.process_input("I'm stuck on this task")
```

### From Hash Documents (When Available)
```python
# Load from hash doc + unconscious context
await manager.load_agent_from_files(
    "artifacts/agents/liza_hash.json",
    "artifacts/agents/liza_unconscious.txt"
)
```

## Agent Integration Points

1. **Terminal Commands** - Agents can respond to terminal inputs
2. **Surveillance Reports** - Agents file reports on each other
3. **Mentorship Sessions** - Green/Blue agents provide guidance
4. **Peer Interactions** - Orange/Yellow agents share experiences
5. **Evaluation Feedback** - Blue+ agents assess performance

## Creating New Agents

1. Define personality in `agent_templates.py`
2. Set appropriate clearance level (R→O→Y→G→B→I→V→UV)
3. Create behavioral patterns (0.0-1.0 scale)
4. Add speech patterns for different contexts
5. Define knowledge domains

## PocketFlow Integration (TODO)

When connected, agents will:
- Use local LLMs for dynamic responses
- Maintain conversation context
- Learn from interactions
- Generate personalized feedback

## Agent Behavior Guidelines

- **Maintain character** - Each agent has consistent personality
- **Respect clearance** - Agents can't exceed their authority
- **Educational focus** - Remember the real purpose
- **Dystopian theme** - Corporate speak, but obviously satirical

## Example Interactions

### Liza (Mentor)
```
User: "I don't understand this algorithm"
Liza: "Hey there! Have you tried breaking it down into smaller steps? 
      Sometimes the Algorithm wants us to overthink things. Let's simplify!"
```

### Vi (Peer)
```
User: "This surveillance report system is confusing"
Vi: "I feel you! What worked for me was just copying what others did at first. 
    We're all in this together, right?"
```

### Compliance Officer Zhang
```
User: "I forgot to clock in this morning"
Zhang: "That seems irregular. Your file has been updated. 
       The Algorithm remembers all productivity gaps."
```

---

*"The agents are here to help. Your compliance is... appreciated."*