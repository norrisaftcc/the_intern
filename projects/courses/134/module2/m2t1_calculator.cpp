#include <iostream>

// CSC 134
// M2T1 - Simple Calculator
// Student Name
// Current Date

int main() {
    // Declare variables
    double num1, num2;
    double sum, difference, product, quotient;
    
    // Get user input
    std::cout << "Simple Calculator Program" << std::endl;
    std::cout << "Please enter the first number: ";
    std::cin >> num1;
    
    std::cout << "Please enter the second number: ";
    std::cin >> num2;
    
    // Perform calculations
    sum = num1 + num2;
    difference = num1 - num2;
    product = num1 * num2;
    
    // Check for division by zero
    if (num2 != 0) {
        quotient = num1 / num2;
    }
    
    // Display results
    std::cout << "\nResults:" << std::endl;
    std::cout << num1 << " + " << num2 << " = " << sum << std::endl;
    std::cout << num1 << " - " << num2 << " = " << difference << std::endl;
    std::cout << num1 << " * " << num2 << " = " << product << std::endl;
    
    if (num2 != 0) {
        std::cout << num1 << " / " << num2 << " = " << quotient << std::endl;
    } else {
        std::cout << "Cannot divide by zero." << std::endl;
    }
    
    return 0;
}