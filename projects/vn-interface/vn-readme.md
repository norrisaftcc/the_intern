# Visual Novel Style Avatar Interface

## Overview

This component implements a visual novel style interface for educational content delivery, combining traditional VN elements with modern web interactivity. It's designed to create an engaging learning environment where technical concepts can be demonstrated through character interactions and live code examples.

## Features

### Avatar System
- Dynamic avatar display that responds to character emotions and actions
- Support for multiple pose states (thinking, excited, teaching, etc.)
- Smooth transitions between different emotional states
- Positioned prominently in the conversation view

### Emote System
- Real-time emote display in the sidebar
- Color-coded entries based on character identity
- Timestamp tracking for all actions
- Support for multiple character emotes
- Format: [*action description*]

### Message Handling
- Integrated message input system
- Automatic emote extraction from messages
- Support for both dialogue and action text
- Real-time message processing and display

## Usage

### Basic Implementation
```jsx
import VNAvatarInterface from './components/VNAvatarInterface';

function App() {
  return <VNAvatarInterface />;
}
```

### Adding Character Actions
Characters can perform actions using the emote syntax:
```javascript
// Example message with emote
"[*adjusts glasses thoughtfully*] Let me explain this concept..."
```

### Customizing Themes
Each character can have their own color theme:
```javascript
const themes = {
  characterName: {
    primary: '#HEX_COLOR',
    background: '#HEX_COLOR_WITH_OPACITY'
  }
};
```

## Extending the Interface

### Adding New Avatar States
1. Add new image paths to the avatarStates object
2. Add corresponding state detection in the processMessage function
3. Create new trigger phrases in your emotes

### Creating New Characters
1. Add a new theme color scheme
2. Create the character's avatar states
3. Add any character-specific emote processing rules

## Integration with Educational Content

The interface is designed to support various types of educational content:

1. Code Demonstrations
   - Embed live code examples
   - Show real-time execution results
   - Provide interactive coding exercises

2. Technical Explanations
   - Use avatar poses to emphasize key points
   - Employ emotes to show problem-solving processes
   - Integrate diagrams and visualizations

3. Interactive Tutorials
   - Guide students through complex concepts
   - Provide immediate feedback on exercises
   - Create engaging learning scenarios

## Future Enhancements

1. Animation Support
   - Smooth transitions between avatar states
   - Animated emote effects
   - Dynamic background changes

2. Audio Integration
   - Voice acting support
   - Sound effects for actions
   - Background music options

3. Interactive Elements
   - Clickable areas on avatars
   - Interactive code snippets
   - Student response tracking

## Contributing

When adding new features or modifications:
1. Maintain the existing emote format for consistency
2. Document any new avatar states or themes
3. Test with various message types and actions
4. Ensure responsive design principles are followed

## Technical Notes

- Built with React and Tailwind CSS
- Uses shadcn/ui components for consistent styling
- Requires modern browser support for optimal performance
- Follows responsive design principles for various screen sizes

## Getting Started

To set up the project environment, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/norrisaftcc/the_intern.git
   cd the_intern
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project.
   - Add any necessary environment variables as specified in the project documentation.

5. **Run the application**:
   ```bash
   npm start
   ```

6. **Access the application**:
   - Open your web browser and go to `http://localhost:3000` to access the project interface.

---

*Note: This interface is part of the Creative Solutions Investigation (CSI) project, designed to create engaging educational experiences for programming students.*
