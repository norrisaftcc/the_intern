#include <iostream>
#include <string>

// CSC 134
// M3T1 - Decisions and Branching
// Student Name
// Current Date

int main() {
    // Declare variables
    double purchaseAmount;
    std::string couponCode;
    double discount = 0.0;
    double totalAmount;
    
    // Get purchase information
    std::cout << "Welcome to the Discount Calculator" << std::endl;
    std::cout << "Enter the purchase amount: $";
    std::cin >> purchaseAmount;
    
    // Clear input buffer
    std::cin.ignore();
    
    std::cout << "Do you have a coupon code? (Enter code or 'none'): ";
    std::getline(std::cin, couponCode);
    
    // Apply discount based on purchase amount
    if (purchaseAmount >= 100) {
        discount += 0.10; // 10% discount for purchases $100 or more
        std::cout << "You get a 10% discount for spending $100 or more!" << std::endl;
    }
    
    // Apply additional discount based on coupon code
    if (couponCode == "SAVE20") {
        discount += 0.20; // Additional 20% discount
        std::cout << "Coupon code SAVE20 applied: 20% additional discount!" << std::endl;
    } else if (couponCode == "SAVE10") {
        discount += 0.10; // Additional 10% discount
        std::cout << "Coupon code SAVE10 applied: 10% additional discount!" << std::endl;
    } else if (couponCode != "none") {
        std::cout << "Invalid coupon code." << std::endl;
    }
    
    // Calculate total
    totalAmount = purchaseAmount * (1 - discount);
    
    // Display results
    std::cout << "\nPurchase Summary:" << std::endl;
    std::cout << "Purchase amount: $" << purchaseAmount << std::endl;
    std::cout << "Discount: " << (discount * 100) << "%" << std::endl;
    std::cout << "Final amount: $" << totalAmount << std::endl;
    
    // Display special message for big spenders
    if (purchaseAmount >= 200) {
        std::cout << "\nThank you for your large purchase!" << std::endl;
    }
    
    return 0;
}