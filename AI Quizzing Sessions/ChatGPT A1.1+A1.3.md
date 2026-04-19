1. Name the five CPU registers in your notes and state one function of each.  
Program Counter (PC) - stores address of next instruction
MAR - temporarily takes the program counter's address to fetch
MDR - temporarily intakes the fetched content
Instruction register (IR) - takes the fetched content and converts it to exact machine instructions
2. In the fetch stage, what roles do the PC, MAR, MDR, and IR each play?  skip
3. What is the difference between pipelining and parallelism?  
Pipelining refers to doing different stages of a program at the same time; parallelism refers to the hardware mechanism of having multiple processors
4. Give two design differences between a CPU and a GPU, and one suitable application for a GPU.  
CPU is for complex, specific tasks; GPU is for a large series of tasks that are simple and repetitive in nature, allowing for large amounts of parallelism.
5. Put these in order from closest to farthest from the CPU: RAM, L1, L3, secondary storage, L2.  
L1, L2, L3, RAM, secondary storage
6. What is the difference between SRAM and DRAM, and which is mainly used for cache?  
Static Ram is slower than Dynamic Ram, cache is dynamic ram and is more expensive
7. Define cache hit and cache miss, and explain how a larger cache affects performance.  
Cache hit is when the fetched instruction is within cache, and cache hits allow the program execution to be faster by decreasing fetching time; cache miss means the fetched instruction is in RAM or beyond, meaning fetch time is considerably longer; larger cache allows for more program instructions to be stored in cache, greatly increasing probability of cache hit and increasing execution time.
8. What is the main purpose of an operating system in one word, according to your notes? Then give three examples of what that leads the OS to do.  
Abstraction. Examples:
- Graphical User Interface - that literally presents the machine in an abstract and humanly way
- Virtualization - simulates and abstracts the computer operating system mechanisms
- Multitasking - hides the complex processes of multitasking under smooth and seamless user experience.

9. What is a process? Then distinguish multiprogramming from multitasking.  

A process is a program in execution. A task is a smaller part of process. Multiprogramming means the efficient utilization of CPU time between doing the different processes, while multitasking is more about ensuring a smooth user experience by smoothly handling the switching of smaller tasks.

10. What is virtual memory? What is swapping? What is thrashing?  

Virtual memory is opening a RAM in the secondary storage, swapping refers to switching data between RAM and secondary; thrashing is when swapping occurs too frequently in a way that decreases efficiency.

11. Compare paging and segmentation in one or two lines.  

Paging is the creation of data blocks to organize information while segmentation is the process of breaking up the data. One is architectural and the other is executional.

12. Distinguish buffering, caching, and spooling with one example each.

Buffering means coping with large amounts of input, such as when the CPU takes in large amounts of information; caching is to store the most frequent data in cache; spooling is the queuing of processes, as seen in printers

13. Compare first-come first-served, round robin, and priority scheduling.  skip

14. What is the difference between time sharing and time slicing?  

Time sharing executed through the means of time slicing. Time sharing refers to the simultaneity in the sharing of time between tasks or processes; time slicing is the specific segmentation of time. 

15. Polling or interrupts: which would usually be better for a keyboard, and why?  

Keyboard is interrupt because it is based on the expectation of stimulus; polling would also mean delay

16. In multitasking, what are deadlock, livelock, and resource contention?  

in multitasking, deadlock refers to two processes needing each other's resource, livelock refers to two processes both waiting to use a resource, resource contention is shown in both instances.

17. State two OS functions needed for multitasking, from your notes.  

Memory allocation: through swapping, the OS allows multiple tasks to run at once
Processor allocation: through slicing of time, scheduling, the OS allows multiple tasks to run at once.

18. What is the difference between an open-loop and a closed-loop control system? Give one real-world example of each.  

Closed-loop means feedback affects future processing. Open-loop means not. Closed is for example a greenhouse that dynamically adjusts to the status of the plants; open is a vending machine

19. In control systems, what do sensors/transducers do?  

convert analog data to digital so for the processor to handle

20. IB-style mini 3-marker: Explain why a virtual machine is a useful example of abstraction when testing software on different platforms. skip


# this is uncorrected, a lot are wrong.