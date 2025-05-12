#ifndef LINKED_LIST_H
#define LINKED_LIST_H

#include <iostream>
#include <stdexcept>

/**
 * Singly Linked List implementation
 * CSC249 - Data Structures
 * Module 3
 */
template <typename T>
class LinkedList {
private:
    // Node structure
    struct Node {
        T data;
        Node* next;
        
        // Constructor
        Node(const T& value, Node* nextNode = nullptr) : 
            data(value), next(nextNode) {}
    };
    
    Node* head;      // Pointer to the first node
    Node* tail;      // Pointer to the last node
    int size;        // Number of elements in the list
    
public:
    // Constructor
    LinkedList() : head(nullptr), tail(nullptr), size(0) {}
    
    // Destructor
    ~LinkedList() {
        clear();
    }
    
    // Copy constructor
    LinkedList(const LinkedList<T>& other) : head(nullptr), tail(nullptr), size(0) {
        Node* current = other.head;
        while (current) {
            append(current->data);
            current = current->next;
        }
    }
    
    // Assignment operator
    LinkedList<T>& operator=(const LinkedList<T>& other) {
        if (this != &other) {
            clear();
            Node* current = other.head;
            while (current) {
                append(current->data);
                current = current->next;
            }
        }
        return *this;
    }
    
    // Clear the list
    void clear() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
        tail = nullptr;
        size = 0;
    }
    
    // Check if the list is empty
    bool isEmpty() const {
        return size == 0;
    }
    
    // Get the size of the list
    int getSize() const {
        return size;
    }
    
    // Add element to the front of the list
    void prepend(const T& value) {
        head = new Node(value, head);
        if (!tail) {
            tail = head;
        }
        size++;
    }
    
    // Add element to the end of the list
    void append(const T& value) {
        Node* newNode = new Node(value);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        size++;
    }
    
    // Insert element at specified index
    void insertAt(int index, const T& value) {
        if (index < 0 || index > size) {
            throw std::out_of_range("Index out of range");
        }
        
        if (index == 0) {
            prepend(value);
        } else if (index == size) {
            append(value);
        } else {
            Node* current = head;
            for (int i = 0; i < index - 1; i++) {
                current = current->next;
            }
            current->next = new Node(value, current->next);
            size++;
        }
    }
    
    // Remove first element
    void removeFirst() {
        if (isEmpty()) {
            throw std::runtime_error("Cannot remove from empty list");
        }
        
        Node* temp = head;
        head = head->next;
        delete temp;
        
        if (!head) {
            tail = nullptr;
        }
        
        size--;
    }
    
    // Remove last element
    void removeLast() {
        if (isEmpty()) {
            throw std::runtime_error("Cannot remove from empty list");
        }
        
        if (head == tail) {
            delete head;
            head = tail = nullptr;
        } else {
            Node* current = head;
            while (current->next != tail) {
                current = current->next;
            }
            
            delete tail;
            tail = current;
            tail->next = nullptr;
        }
        
        size--;
    }
    
    // Remove element at specified index
    void removeAt(int index) {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of range");
        }
        
        if (index == 0) {
            removeFirst();
        } else if (index == size - 1) {
            removeLast();
        } else {
            Node* current = head;
            for (int i = 0; i < index - 1; i++) {
                current = current->next;
            }
            
            Node* temp = current->next;
            current->next = temp->next;
            delete temp;
            size--;
        }
    }
    
    // Get element at specified index (without removing)
    T& at(int index) {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of range");
        }
        
        Node* current = head;
        for (int i = 0; i < index; i++) {
            current = current->next;
        }
        
        return current->data;
    }
    
    // Search for a value and return its index (or -1 if not found)
    int indexOf(const T& value) const {
        Node* current = head;
        int index = 0;
        
        while (current) {
            if (current->data == value) {
                return index;
            }
            current = current->next;
            index++;
        }
        
        return -1;  // Value not found
    }
    
    // Check if the list contains a value
    bool contains(const T& value) const {
        return indexOf(value) != -1;
    }
    
    // Print the list
    void display() const {
        Node* current = head;
        std::cout << "[";
        
        while (current) {
            std::cout << current->data;
            if (current->next) {
                std::cout << ", ";
            }
            current = current->next;
        }
        
        std::cout << "]" << std::endl;
    }
};

#endif // LINKED_LIST_H