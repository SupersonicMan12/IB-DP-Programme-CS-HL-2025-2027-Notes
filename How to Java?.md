## What Java Is

- High-level, object-oriented programming language
- Compiled to **bytecode** and executed by the **JVM** (platform-independent)
- Strongly typed (variable types must be declared)

## Basic Program Structure

```java
public class Main {
    public static void main(String[] args) {
        // code runs here
    }
}
```
- `class` defines a blueprint (for objects)
- `main` is the entry point of the program
## Variables and Data Types

### Primitive types

- `int`
    
- `double`
    
- `boolean`
    
- `char`
    
- `long`
    
- `float`
    
- `short`
### Reference types

- `String`, arrays, objects
    

```java
int x = 5;
double y = 3.14;
boolean ok = true;
String s = "Hello";
```

---

## Operators

- Arithmetic: `+ - * / %`
    
- Comparison: `== != < > <= >=`
    
- Logical: `&& || !`
    
- Assignment: `= += -=`
    

---

## Control Structures

### Conditionals

```java
if (x > 0) { }
else if (x == 0) { }
else { }
```

### Loops

```java
for (int i = 0; i < n; i++) { }
while (condition) { }
```

---

## Methods

- Reusable blocks of code
    

```java
static int add(int a, int b) {
    return a + b;
}
```

- Parameters are passed **by value**
    
- `void` methods return nothing
    

---

## Objects and Classes

```java
class Person {
    String name;
    int age;

    Person(String n, int a) {
        name = n;
        age = a;
    }
}
```

- Object = instance of a class
    
- **Encapsulation**: `private` fields, public methods
    
- Constructors initialize objects
    

---

## Arrays

- Fixed size, same data type
    

```java
int[] arr = new int[5];
int[] nums = {1, 2, 3};
```

- Access with `arr[i]`
    
- Size with `arr.length`
    

### 2D Arrays

```java
int[][] grid = new int[3][4];
```

---

## ArrayList

- Dynamic-size array
    

```java
ArrayList<Integer> list = new ArrayList<>();
list.add(5);
list.get(0);
list.size();
int loc = list.indexOf(5);
list.remove(loc);
```

---

## Stacks

- **LIFO (Last In, First Out)**
    

```java
Stack<Integer> st = new Stack<>();
st.push(1);
st.pop();
st.peek();
st.isEmpty();
```

Uses:

- Undo operations
    
- Reversing data
    
- Expression evaluation
    

---

## Queues

- **FIFO (First In, First Out)**
    

```java
Queue<Integer> q = new LinkedList<>();
q.add(1);
q.remove();
q.peek();
```

Uses:

- Scheduling
    
- Buffering
    
- Breadth-first processing
    

---
### USE ARRAY TO IMPLEMENT QUEUE + STACK!