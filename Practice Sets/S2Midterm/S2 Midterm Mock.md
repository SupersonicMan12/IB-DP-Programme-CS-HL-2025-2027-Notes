## Section A \[25\]

1. Identify two differences between a wide area network (WAN) and a local area network (LAN). \[2\]
2. Outline the reason for compression when transmitting data. \[2\]
3. Outline the need for a translation process from high level language to machine code. \[2\]
4. Draw the truth table for the following logic circuit \[4\]![[Screenshot 2026-04-18 at 13.07.13.png]]
5. Calculate, showing your working in each case: \[2+2\]
	(a) the binary (base 2) value of the denary (base 10) number: 105 
	(b) the hexadecimal (base 16) value of the denary (base 10) number: 200
6. State three operating system resource management techniques. \[3\]
7. Answer: \[1+1\]
	(a) Identify one characteristic of a queue
	(b) Identify one application of a queue
8. Identify one function of a single-user operating system. \[1\]
9. Outline one reason for the use of standards in the construction of networks. \[2\]
10. Explain how cache memory affects system performance. \[3\]
# Section B 

#### Question 1 \[15\]
A teacher would like a simple program to store the names, marks and grades of students in a set of three parallel one-dimensional arrays called `NAME[]`, `MARK[]` and `GRADE[]`. The grade boundaries for individual grades are shown below:![[Screenshot 2026-04-18 at 13.19.41.png]]
	a) Identify two components in a conditional statement \[2\]
	b) Construct an algorithm using pseudocode to take the marks that have been stored in `MARK[]`, convert them into the appropriate grade and store the calculated grades in `GRADE[]`. \[5\]
	c) Outline how the name, mark and grade in the three arrays correspond to the same student \[2\]
	d) Construct an algorithm using psuedocode to output the names and grades of all students who achieve a grade of Merit or Distinction. \[3\]
	e) Explain how you would change your algorithm in part d) to allow a user to choose a grade and output the names and marks of the students who have achieved this grade \[3\]	

#### Question 2 \[15\]
Cars have many automated features to improve the driving experience. One example is the use of headlights that automatically switch on and off. 

a) State one input device used by the automated headlights. \[1\] 

Some cars have adaptive cruise control. This uses RADAR technology and a processor to ensure the car stays the same distance away from the car in front. 

b) Explain how the interaction between the inputs, processing and the outputs of the feedback loop ensure the car stays the same distance away from the car in front. \[6\] 

A system with many functions operating independently could be managed using either centralized or decentralized processing. 

c) Discuss the use of centralized and decentralized processing in the context of control systems such as those involved in the operation of motor vehicles. \[5\] 

As vehicles become fully autonomous (self-driving), ethical considerations must be taken into account when designing software. 

d) Explain one ethical concern that must be considered in the development of autonomous vehicles \[3\]

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

Source: 2022 May SL + HL