# IB DP Computer Science — Theme B and Paper 2 (first assessment 2027)

Extracted from the *Computer science guide* (first assessment 2027). Use it to check that every
skill a question needs is on the syllabus. If it isn't listed here, don't require it.

## Assessment facts that affect question design

| | SL | HL |
|---|---|---|
| Paper 2 duration | 1 h 15 min | 2 h |
| Paper 2 marks | 50 | 80 |
| Paper 2 weighting | 35% | 40% |

- Paper 2 has extended-response questions on theme B (computational thinking and problem-solving). All questions are compulsory.
- One question focuses on algorithmic thinking without needing to read or write code. On HL, two SL questions are repeated and the other questions cover HL-only topics.
- There are two versions of paper 2: **Option A — Java** and **Option B — Python**. Questions after the first use the same context and assess the same skills. Students answer only their own language.
- Python built-ins such as `sort`, `pop`, `len`, `max` and `min` are allowed in general, but **specific questions may prohibit specific built-in functions, and the paper says so clearly**. There is no published list.
- Syntax: small errors may get no penalty, and a repeated error type is penalized at most once. Errors that change execution (for example `=` for `==`, or Python indentation that changes structure) may be penalized. Marking focuses on whether the code meets the requirement.
- Roughly 1.5 minutes per mark (80 marks / 120 minutes).

## B1 Computational thinking
- **B1.1.1** Construct a problem specification: problem statement, constraints and limitations, objectives and goals, input/output specifications, evaluation criteria.
- **B1.1.2** Describe the fundamental concepts of computational thinking: abstraction, algorithmic design, decomposition, pattern recognition.
- **B1.1.3** Explain how computational thinking is applied to solve problems (it does not have to involve programming).
- **B1.1.4** Trace flowcharts for a range of programming algorithms. Standard symbols: connector, decision, flowline, input/output, process, start/end.

## B2 Programming (SL 40 h, HL 42 h)
### B2.1 Programming fundamentals
- **B2.1.1** Construct and trace programs using global and local variables of various data types (Boolean, char, decimal, integer, string).
- **B2.1.2** Construct programs that extract and manipulate substrings (altering, concatenating, replacing).
- **B2.1.3** Describe common exception handling: unexpected inputs, resource unavailability, logic errors; try/catch (Java), try/except (Python), finally.
- **B2.1.4** Construct and use debugging techniques: trace tables, breakpoints, print statements, step-by-step execution.

### B2.2 Data structures
- **B2.2.1** Compare static and dynamic data structures (memory allocation, resizing, speed, memory, flexibility).
- **B2.2.2** Construct programs that apply arrays and Lists: 1D and 2D arrays and ArrayLists (Java); 1D and 2D lists (Python); add, remove and traverse elements in a dynamic list.
- **B2.2.3** Stack (LIFO): push, pop, peek, isEmpty; performance and memory; choosing a stack for a problem.
- **B2.2.4** Queue (FIFO): enqueue, dequeue, front, isEmpty; performance and memory; choosing a queue for a problem.

### B2.3 Programming constructs
- **B2.3.1** Correct sequencing of instructions; avoiding infinite loops, deadlock and incorrect output.
- **B2.3.2** Selection: if / else / else if (Java), elif (Python), with Boolean operators (AND, OR, NOT) and relational operators.
- **B2.3.3** Looping: counted and conditional loops, with conditions inside loops.
- **B2.3.4** Functions and modularization: reusable code, scope (local vs global), benefits of modularization.

### B2.4 Programming algorithms
- **B2.4.1** Describe efficiency using Big O: time and space complexity; choosing algorithms for scalability.
- **B2.4.2** Construct and trace **linear search and binary search**; efficiency differences; choosing a search technique.
- **B2.4.3** Construct and trace **bubble sort and selection sort**; time and space complexity; pros and cons on different data sets.
- **B2.4.4** (HL) Explain recursion: advantages and limitations; quicksort; fractals, binary-tree traversal, sorting.
- **B2.4.5** (HL) Construct and trace recursive algorithms. **Simple, non-branching recursive algorithms in programming only.**

### B2.5 File processing
- **B2.5.1** Construct code for text files: open in read/write/append modes, read, write, append, close. Java: Scanner, FileWriter, BufferedReader. Python: open(), read(), readline(), write(), close().

## B3 Object-oriented programming (SL 7 h, HL 23 h)
- **B3.1.1** Evaluate the fundamentals of OOP (classes, objects, inheritance, encapsulation, polymorphism).
- **B3.1.2** Design classes, methods and behaviour; UML class diagrams.
- **B3.1.3** Static vs non-static variables and methods.
- **B3.1.4** Define classes and instantiate objects; constructors.
- **B3.1.5** Encapsulation and information hiding; private/public; controlling access.
- **B3.2.1** (HL) Inheritance; access modifiers private/public/protected/default.
- **B3.2.2** (HL) Polymorphism: overriding (dynamic) and overloading (static).
- **B3.2.3** (HL) Abstraction; abstract classes.
- **B3.2.4** (HL) Composition and aggregation.
- **B3.2.5** (HL) Design patterns: singleton, factory, observer.

## B4 Abstract data types (HL only, 23 h)
- **B4.1.1** Properties and purpose of ADTs.
- **B4.1.2** Evaluate linked lists (singly, doubly, circular), with diagrams.
- **B4.1.3** Construct and apply linked lists: insertion, deletion, traversal, search.
- **B4.1.4** BSTs: insert, delete, traverse, search; sketch.
- **B4.1.5** Sets: union, intersection, difference, membership, subset/superset.
- **B4.1.6** Core ADT principles; hash tables (hashing, collisions, load factor); HashMap/HashSet (Java), dict/set (Python).

## What "no complex data structures" means for the hardest question
Build the challenge from **1D/2D arrays, loops, selection, methods, a class, Big O, linear/binary
search, bubble/selection sort, and simple non-branching recursion**. Stacks/queues are allowed if
the context really needs them. Avoid: hash maps as the key insight, trees, graphs, heaps, DP
tables beyond simple 1D/2D running totals, branching recursion, built-in sorting of objects, and
library algorithms.
