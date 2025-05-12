#include <iostream>
#include <string>
#include "LinkedList.h"

// CSC249 - Data Structures
// Module 3 - Linear Data Structures
// Linked List Demo

int main() {
    std::cout << "=== Integer Linked List Demo ===" << std::endl;
    
    // Create a linked list of integers
    LinkedList<int> numbers;
    
    // Test append
    std::cout << "\nAppending values 10, 20, 30:" << std::endl;
    numbers.append(10);
    numbers.append(20);
    numbers.append(30);
    numbers.display();
    
    // Test prepend
    std::cout << "\nPrepending value 5:" << std::endl;
    numbers.prepend(5);
    numbers.display();
    
    // Test insertAt
    std::cout << "\nInserting 15 at index 2:" << std::endl;
    numbers.insertAt(2, 15);
    numbers.display();
    
    // Test size and at
    std::cout << "\nList size: " << numbers.getSize() << std::endl;
    std::cout << "Value at index 2: " << numbers.at(2) << std::endl;
    
    // Test indexOf and contains
    std::cout << "\nIndex of 15: " << numbers.indexOf(15) << std::endl;
    std::cout << "Contains 25? " << (numbers.contains(25) ? "Yes" : "No") << std::endl;
    std::cout << "Contains 30? " << (numbers.contains(30) ? "Yes" : "No") << std::endl;
    
    // Test removal methods
    std::cout << "\nRemoving first element:" << std::endl;
    numbers.removeFirst();
    numbers.display();
    
    std::cout << "Removing element at index 1:" << std::endl;
    numbers.removeAt(1);
    numbers.display();
    
    std::cout << "Removing last element:" << std::endl;
    numbers.removeLast();
    numbers.display();
    
    // Test clear
    std::cout << "\nClearing list..." << std::endl;
    numbers.clear();
    std::cout << "List empty? " << (numbers.isEmpty() ? "Yes" : "No") << std::endl;
    
    // Test with strings
    std::cout << "\n=== String Linked List Demo ===" << std::endl;
    LinkedList<std::string> fruits;
    
    fruits.append("Apple");
    fruits.append("Banana");
    fruits.append("Cherry");
    fruits.display();
    
    std::cout << "\nInserting 'Orange' at index 1:" << std::endl;
    fruits.insertAt(1, "Orange");
    fruits.display();
    
    // Test copy constructor
    std::cout << "\n=== Copy Constructor Test ===" << std::endl;
    LinkedList<std::string> fruitsCopy = fruits;
    std::cout << "Original list:" << std::endl;
    fruits.display();
    std::cout << "Copied list:" << std::endl;
    fruitsCopy.display();
    
    std::cout << "\nModifying original (removing 'Cherry'):" << std::endl;
    fruits.removeAt(fruits.indexOf("Cherry"));
    std::cout << "Original list:" << std::endl;
    fruits.display();
    std::cout << "Copied list (should be unchanged):" << std::endl;
    fruitsCopy.display();
    
    // Test assignment operator
    std::cout << "\n=== Assignment Operator Test ===" << std::endl;
    LinkedList<std::string> moreStrings;
    moreStrings.append("Test");
    moreStrings = fruits;
    std::cout << "Assigned list:" << std::endl;
    moreStrings.display();
    
    std::cout << "\nEnd of linked list demonstration" << std::endl;
    return 0;
}