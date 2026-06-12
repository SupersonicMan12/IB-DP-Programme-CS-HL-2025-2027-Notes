# BE SUPER AWARE OF HOW MANY POINTS ARE BEING AWARDED
## Section A \[25\]

1. Identify two differences between a wide area network (WAN) and a local area network (LAN). \[2\]

Any two of:
- WAN works over a larger geographical area, while LAN is confined to a specific building or area 
- LAN is connected through private infrastructure, while WAN needs to go through public nodes
- LAN is more secure than WAN
- LAN is typically cheaper to implement / maintain
- LAN has higher bandwidth
- WAN requires more hardware to connect different networks

2. Outline the reason for compression when transmitting data. \[2\]

The reason for compression when transmitting data is to save transfer time.
This is because compression decreases the file size or number of bits so they are faster to transfer.

Alternatives: save cloud storage, use less bandwidth. 1 point for answer (first sentence), 1 point for explanation (second sentence).

3. Outline the need for a translation process from high level language to machine code. \[2\]
4. Draw the truth table for the following logic circuit \[4\]![[Screenshot 2026-04-18 at 13.07.13.png]]![[Screenshot 2026-04-18 at 14.11.43.png|608]]
1 mark for every two correct rows.

5. Calculate, showing your working in each case: \[2+2\]
	(a) the binary (base 2) value of the denary (base 10) number: 105 
	(b) the hexadecimal (base 16) value of the denary (base 10) number: 200

(0)1101001; C8

6. State three operating system resource management techniques. \[3\]

Scheduling, multitasking, virtual memory, paging, interrupt, polling, policies.

7. Answer: \[1+1\]
	(a) Identify one characteristic of a queue
	(b) Identify one application of a queue

a) a queue is a linear data structure; maintains the first-in first-out principle; elements only at one end (any one gives full)
b) Print queue, CPU task scheduling, playlist queue, interrupt queues etc. (any one gives full)

8. Identify one function of a single-user operating system. \[1\]

!! Function means feature of OS, not why we use it !!
Functions: memory management or processor management.

9. Outline one reason for the use of standards in the construction of networks. \[2\]

Ensure compatibility between nodes on the network (1) through the use of common techniques/protocols/language (1).

10. Explain how cache memory affects system performance. \[3\]

Cache is high speed memory OR located between CPU and RAM (1)
Frequently used data / instructions are stored here (1)
Allows for faster retrieval / access time by searching here first, making it faster (1)
# Section B 

#### Question 1 \[15\]
A teacher would like a simple program to store the names, marks and grades of students in a set of three parallel one-dimensional arrays called `NAME[]`, `MARK[]` and `GRADE[]`. The grade boundaries for individual grades are shown below:![[Screenshot 2026-04-18 at 13.19.41.png]]
The class has 30 students.
	a) Identify two components in a conditional statement \[2\]
	b) Construct an algorithm using pseudocode to take the marks that have been stored in `MARK[]`, convert them into the appropriate grade and store the calculated grades in `GRADE[]`. \[5\]
	c) Outline how the name, mark and grade in the three arrays correspond to the same student \[2\]
	d) Construct an algorithm using psuedocode to output the names and grades of all students who achieve a grade of Merit or Distinction. \[3\]
	e) Explain how you would change your algorithm in part d) to allow a user to choose a grade and output the names and marks of the students who have achieved this grade \[3\]	

a) any two of: if, then, else, test, condition, action, consequence, alternative action and consequence
b) 1 point for correct loop of 30 elements / all students; 1 point for correct use of indexes in both arrays mark and grade; 1 point for each if statement with correct condition and grade assignment up to 4
This means that you can get 5 while messing up 1 point because 1+1+4 = 6 > 5
c) These arrays are **parallel** because they have the same length (1) and the same array index corresponds to the information about the same student (1)
d)  1 for correct loop 1 for correct if 1 for correct output
e) 1 for input statement before loop 1 for changing conditional statement 1 for outputting the name and marks correctly
#### Question 2 \[15\]
Cars have many automated features to improve the driving experience. One example is the use of headlights that automatically switch on and off. 

a) State one input device used by the automated headlights. \[1\] 

Some cars have adaptive cruise control. This uses RADAR technology and a processor to ensure the car stays the same distance away from the car in front. 

b) Explain how the interaction between the inputs, processing and the outputs of the feedback loop ensure the car stays the same distance away from the car in front. \[6\] 

A system with many functions operating independently could be managed using either centralized or decentralized processing. 

c) Discuss the use of centralized and decentralized processing in the context of control systems such as those involved in the operation of motor vehicles. \[5\] 

As vehicles become fully autonomous (self-driving), ethical considerations must be taken into account when designing software. 

d) Explain one ethical concern that must be considered in the development of autonomous vehicles \[3\]

a) light sensor or photoelectric sensor.
b) Notice "same distance". Watch carefully:
1. Sensor continuously collects data related to the distance between two vehicles.
2. This data is converted from analog to digital and sent to processor
3. Processor has access to pre-set data
4. Processor compares input with pre-set data
5. If the vehicle is too close, the processor sends a signal to apply the breaks or a warning to the driver to apply break
6. If the car has fallen back from the car in front, the processor sends a signal to apply acceleration or signal to the driver to re-accelerate
7. The process is constantly looped, as the sensor continues taking in the feedback from the processor's previous decision.
Make sure your answer has at least at least 6 distinct points, best in chronology.
c) Two points for centralized: different features of a car controlled by same processor; features are less likely to interfere with each other. Two points for decentralized: each feature has its own processor; enables independent and faster functioning. One point for conclusion or comparison: centralized is more complex; more expensive; takes longer time
d) Choose one topic and elaborate with three sentences: trolley problem, who takes responsibility, data privacy.

### Question 3 \[15\]

Reverse Polish notation (RPN) is a method used to represent mathematical expressions so they can be evaluated without the need for parentheses. 

An expression written in this form is known as postfix notation, whereas an expression written the traditional way is known as infix notation.  For example: 

Infix notation: `(8 – 5) * 7` 
Postfix notation: `8 5 – 7 *`

Both the infix and postfix expressions have the same result: 21 

RPN expressions are evaluated from left to right as follows:
- Each character is checked,
	- if it is a digit, it is pushed onto a stack. 
	- if it is a mathematical operator, the last two digits are popped from the stack and evaluated as though the current operator was between them. The result of this operation is then pushed back onto the stack. 
- The process is repeated until all the characters in the RPN expression have been used.
- The value left in the stack is the result of the expression. 

A collection named RPN already stores an expression formatted in Reverse Polish notation. The algorithm reads the values from the collection and, using a stack data structure, evaluates it.

a)  Copy and complete the trace table for the algorithm using the RPN collection data:
![[Screenshot 2026-04-18 at 14.03.41.png]]
b) Explain why a stack is used in the process of evaluating the expression in the algorithm. \[3\]

An alternative data structure in which the expression used in part (a) may be stored is a binary tree. If the tree is traversed using postorder tree traversal, the output is formatted in RPN.
![[Screenshot 2026-04-18 at 14.04.31.png]]
c) Outline the steps involved in traversing the given tree using postorder tree traversal. \[4\]
d) State the output from the given tree using inorder tree traversal. \[2\]

a) 1 point for correct VALUE, 1 point for each of +-\*/ , 1 point for 21. the trace table may differ from:
![[Screenshot 2026-04-18 at 14.31.45.png]]
b) Stack is first in last out (1). Order is properly preserved between operands (1), give an example like 25-16=9 (1)
c) Start from root node; if root is null, return immediately; traverse left; traverse right; visit root. We haven't covered binary trees so its fine if it wasn't obvious.
d) (5+2) * (25-16) / 3

Source: 2022 May SL + HL