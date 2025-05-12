# Number Guessing Game Project

## Overview
In this project, you will create a fully-featured number guessing game that demonstrates your understanding of fundamental C++ programming concepts. The project will incorporate various programming techniques learned throughout the course, including input/output, control structures, functions, and basic file operations.

## Objectives
- Apply fundamental C++ programming concepts to a practical application
- Implement proper program organization and structure
- Create a user-friendly interface with input validation
- Practice file I/O for saving game statistics

## Requirements

### Core Features
Your number guessing game should include the following features:
1. Generate a random number for the player to guess
2. Track the number of attempts made
3. Provide feedback on each guess (too high, too low)
4. Allow multiple difficulty levels (different ranges)
5. Store and display high scores (fewest guesses)
6. Allow the player to play again without restarting the program
7. Implement basic statistics (average guesses, best score, etc.)

### Technical Requirements
- Use proper C++ coding style and naming conventions
- Implement appropriate error handling and input validation
- Organize code into functions for different tasks
- Include at least one custom header file
- Implement file I/O for persistent high scores
- Use at least one custom data structure (struct or class)

### Documentation
Your project must include:
1. Program header comment block with:
   - Program name and purpose
   - Your name and date
   - Course information
2. Function header comments explaining:
   - Purpose of each function
   - Parameters and return values
   - Any side effects
3. Inline comments for complex logic
4. README file with:
   - Installation instructions
   - Game rules and interface explanation
   - Features implemented

## Milestones
1. **Basic Game** (Week 6)
   - Random number generation
   - Basic guessing logic
   - Play again functionality

2. **Enhanced Features** (Week 9)
   - Difficulty levels
   - Input validation
   - Game statistics

3. **Final Version** (Week 12)
   - High score system with file I/O
   - Polished user interface
   - Complete documentation

## Evaluation Criteria
- Functionality (40%): Does the game work as described?
- Code Quality (25%): Is the code well-structured and organized?
- User Experience (15%): Is the game intuitive and user-friendly?
- Documentation (15%): Is the code properly documented?
- Creativity (5%): Any additional creative features?

## Getting Started
1. Review the random number generation examples from Module 2
2. Study the control structures from Modules 3 and 4
3. Refer to the file I/O examples from Module 9
4. Plan your program structure before coding

## Sample Code Structure

```cpp
// numberguess.h - Main game declarations
#ifndef NUMBERGUESS_H
#define NUMBERGUESS_H

// Structure to hold game settings
struct GameSettings {
    int minNumber;
    int maxNumber;
    std::string difficultyName;
};

// Structure to hold game statistics
struct GameStats {
    std::string playerName;
    int score;
    std::string difficulty;
    std::string date;
};

// Function declarations
void displayWelcome();
GameSettings selectDifficulty();
int playGame(GameSettings settings);
void saveScore(GameStats stats);
void displayHighScores();
// ... additional functions as needed

#endif
```

## Additional Resources
- Random number generation: Module 2 materials
- Input validation: Module 3 examples
- File I/O: Module 9 examples
- Sample project structure templates