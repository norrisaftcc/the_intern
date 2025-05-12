# Module 1: Introduction and Review

## Topics
- Course overview and expectations
- Review of C++ fundamentals
- Object-oriented programming review
- Algorithm efficiency introduction

## Lab Activities
- C++ review exercises
- Simple class implementation

## Assessment
- C++ proficiency assessment
- Algorithm analysis exercises

## Learning Objectives
After completing this module, students will be able to:
- Demonstrate proficiency in core C++ concepts
- Implement and use classes in C++
- Explain basic concepts of algorithmic efficiency
- Set up their development environment for data structures work
- Write well-structured C++ programs using OOP principles

## Resources
- Lecture slides (see lecture_slides.pdf)
- C++ review materials
- OOP cheat sheet
- Sample class implementations
- Algorithm efficiency primer

## Assignments
### m1t1_cpp_review
Complete a series of short programming exercises to review fundamental C++ concepts:
- Control structures
- Functions and parameter passing
- Arrays and pointers
- Basic file I/O
- Simple classes

### m1lab1_student_class
Implement a `Student` class with:
- Private data members for student ID, name, and GPA
- Public methods for accessing and modifying data
- Constructor and destructor
- A static method to track the number of students
- A method to display student information

### m1hw1_algorithm_analysis
Analyze the time and space complexity of provided code segments and write a brief explanation of your analysis.

## Sample Code
```cpp
// Example Student class header
class Student {
private:
    int id;
    std::string name;
    double gpa;
    static int totalStudents;

public:
    // Constructor
    Student(int studentId, std::string studentName, double studentGpa);
    
    // Destructor
    ~Student();
    
    // Accessor methods
    int getId() const;
    std::string getName() const;
    double getGpa() const;
    
    // Mutator methods
    void setName(std::string newName);
    void setGpa(double newGpa);
    
    // Other methods
    void displayInfo() const;
    static int getTotalStudents();
};
```

## Due Dates
- M1T1 (C++ Review): [Due Date]
- M1LAB1 (Student Class): [Due Date]
- M1HW1 (Algorithm Analysis): [Due Date]