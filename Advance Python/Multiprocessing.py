# Concurrency - allows program to execute multiple tasks simultaneously
# These can be done through - 1. Multhreading  2. Multiprocessing 3. Asynchronous I/O

" Multiprocessing "
# involves creating multiple processes to run independently, each with own tasks
# Ideal for CPU bound tasks like mathematical computations, etc.

"Key Concepts of Multiprocessing"
"1. Process Creation "
# Processes are created using the Process class in the multiprocessing module.

"2. Inter Process Communication (IPC)"
# Processes do not share memory, so data must be shared using pipes, queues, or shared memory

"3. Pool Class" "pool of workers"
# Use Pool to manage multiple processes efficiently.

import multiprocessing
import time

def square_number(n):
    print(f"Square of {n}: {n ** 2}")
    time.sleep(1)

# Creating multiple processes
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    processes = []
    
    for num in numbers:
        process = multiprocessing.Process(target=square_number, args=(num,))
        processes.append(process)
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All processes completed!")
