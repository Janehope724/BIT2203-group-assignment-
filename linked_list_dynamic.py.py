class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

   
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        print(f"{data} pushed onto stack")

    
    def pop(self):
        if self.top is None:
            print("Stack Underflow! Nothing to pop")
            return None
        popped = self.top.data
        self.top = self.top.next
        print(f"{popped} popped from stack")
        return popped

    
    def peek(self):
        if self.top is None:
            print("Stack is empty")
            return None
        return self.top.data

    
    def display(self):
        if self.top is None:
            print("Stack is empty")
            return
        current = self.top
        print("Stack elements:", end=" ")
        while current:
            print(current.data, end=" ")
            current = current.next
        print()


stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
stack.display()

stack.pop()
stack.display()

print("Top element is:", stack.peek())
