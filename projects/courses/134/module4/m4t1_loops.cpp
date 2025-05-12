#include <iostream>

// CSC 134
// M4T1 - Loops
// Student Name
// Current Date

int main() {
    // For loop example - Counting from 1 to 10
    std::cout << "For Loop Example - Counting from 1 to 10:" << std::endl;
    for (int i = 1; i <= 10; i++) {
        std::cout << i << " ";
    }
    std::cout << std::endl << std::endl;
    
    // While loop example - Countdown from 10 to 1
    std::cout << "While Loop Example - Countdown from 10 to 1:" << std::endl;
    int countdown = 10;
    while (countdown > 0) {
        std::cout << countdown << " ";
        countdown--;
    }
    std::cout << "Blastoff!" << std::endl << std::endl;
    
    // Do-while loop example - Input validation
    std::cout << "Do-While Loop Example - Input Validation:" << std::endl;
    int userInput;
    do {
        std::cout << "Enter a number between 1 and 10: ";
        std::cin >> userInput;
        
        if (userInput < 1 || userInput > 10) {
            std::cout << "Invalid input. Please try again." << std::endl;
        }
    } while (userInput < 1 || userInput > 10);
    
    std::cout << "You entered: " << userInput << std::endl << std::endl;
    
    // Nested loop example - Multiplication table
    std::cout << "Nested Loop Example - Multiplication Table (5x5):" << std::endl;
    for (int row = 1; row <= 5; row++) {
        for (int col = 1; col <= 5; col++) {
            std::cout << row * col << "\t";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
    
    // Loop with break statement
    std::cout << "Loop with Break Statement:" << std::endl;
    for (int i = 1; i <= 20; i++) {
        if (i == 13) {
            std::cout << "Breaking at 13..." << std::endl;
            break;
        }
        std::cout << i << " ";
    }
    std::cout << std::endl << std::endl;
    
    // Loop with continue statement
    std::cout << "Loop with Continue Statement (skipping odd numbers):" << std::endl;
    for (int i = 1; i <= 10; i++) {
        if (i % 2 != 0) {
            continue;
        }
        std::cout << i << " ";
    }
    std::cout << std::endl;
    
    return 0;
}