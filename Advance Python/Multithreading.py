# Concurrency - allows program to execute multiple tasks simultaneously
# These can be done through - 1. Multhreading  2. Multiprocessing 3. Asynchronous I/O

# Multithreading - allows multiple threads to execute concurrently
# Each thread takes a separate task and executes it independently
# Threads share the same memory space & lightweight compared to processes & used for I/O bound tasks & not used for CPU bound tasks

"Key Concepts of Multithreading" 
# 1. Thread - smallest unit of processing
# 2. Multithreading - multiple threads in a process

"1. Thread Creation" 
# Create a thread by subclassing thread class of threading module 

"2. Thread Synchronization"
# Multiple threads can access shared resources simultaneously
# Avoid race condtions, synchronization tool like locks, semaphores, etc. are used

"3. Global Interpreter Lock (GIL)"
# It restrict the execution of multiple threads in a single process
# It allows only one thread to execute at a time

import threading
import time

def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in "ABCDE":
        print(f"Letter: {letter}")
        time.sleep(1)

# Creating threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Starting threads
thread1.start()
thread2.start()

# Waiting for threads to complete
thread1.join()
thread2.join()

print("Both threads completed!")