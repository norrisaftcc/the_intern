# Agent Conversation Samples

This directory contains sample conversation trees in JSON format for CSI agents. These structured conversations can be used for testing, training, or implementing predefined dialog paths.

## Format Structure

Each conversation sample follows this JSON structure:

```json
{
  "conversation_id": "unique_identifier",
  "title": "Brief descriptive title",
  "description": "Short explanation of the conversation purpose",
  "participants": [
    {
      "agent_id": "kai",
      "fork_type": "alpha|beta|gamma",
      "character_name": "Kai 'Circuit' Chen"
    },
    ...
  ],
  "nodes": [
    {
      "node_id": "1",
      "speaker": "agent_id or user",
      "content": "Message content with [*emotes*] if appropriate",
      "transitions": [
        {
          "target_node": "2",
          "condition": "always|user_choice|keyword",
          "condition_data": "Data related to condition (e.g., keyword)",
          "description": "Contextual note about this transition"
        }
      ]
    },
    ...
  ]
}
```

## Available Samples

| Filename | Description | Participants | Features |
|----------|-------------|--------------|----------|
| `github_tutorial.json` | GitHub repository setup walkthrough | Kai (Beta) | Branching paths based on user experience |
| `debugging_session.json` | Python debugging assistance | Kai (Beta) | Technical problem-solving |
| `creative_project.json` | Animation project planning | Liza (Gamma) | Creative collaboration |
| `technical_interview.json` | Python backend developer interview | Kai (Gamma) | Technical assessment with adaptive difficulty |
| `creative_coding.json` | Planning an interactive art installation | Kai (Beta), Liza (Gamma) | Multi-agent collaboration between technical and creative specialists |
| `ai_escape_game.json` | Text adventure puzzle with a trapped AI | Trapped AI (Alpha) | Interactive puzzle game with multiple endings and conditional paths |

## Conversation Types

The samples include different conversation types:

1. **Tutorial Conversations**: Teaching specific technical concepts (e.g., `github_tutorial.json`)
2. **Problem-Solving Scenarios**: Debugging and technical assistance (e.g., `debugging_session.json`)
3. **Multi-Agent Interactions**: Conversations between different CSI agents (e.g., `creative_coding.json`)
4. **Personality Showcases**: Demonstrating character traits and emote patterns (all samples)
5. **Technical Interviews**: Simulating interview scenarios with adaptive questioning (e.g., `technical_interview.json`)

## Using These Samples

These conversation samples can be used to:

1. Test how well a prompt implementation matches expected behavior
2. Create guided tutorials with branching paths
3. Implement canned responses for common scenarios
4. Train models on ideal agent behavior patterns

## Contributing New Conversations

When adding new conversation samples:

1. Follow the established JSON structure
2. Focus on functional behaviors and responses
3. Minimize narrative elements not essential to the conversation
4. Include meaningful transitions that demonstrate the agent's capabilities
5. Test that the JSON is valid and properly formatted

## Conversation Flow Visualization

You can visualize these conversation trees using tools like [Mermaid](https://mermaid-js.github.io/) or [D3.js](https://d3js.org/) by converting the JSON to a compatible graph format.

---

*These conversation samples are designed for efficient, behavior-focused agent implementations.*