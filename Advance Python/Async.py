# Concurrency - allows program to execute multiple tasks simultaneously
# These can be done through - 1. Multhreading  2. Multiprocessing 3. Asynchronous I/O

" Async I/O Basics "
# enables asynchronous I/O operations using coroutines and event loops
# Ideal for I/O bound tasks like web scraping, etc.

" Key Cooncepts of Async I/O "
" 1. Coroutines "
# functions that can pause and resume execution at any point
# (A function defined with async def and capable of being paused and resumed using await.)

" 2. Event Loop "
# A mechanism that schedules and runs multiple asynchronous tasks.

" 3. Concurrency with Async I/O "
# Async I/O allows multiple tasks to run concurrently and wait for I/O operations to complete

import asyncio

async def fetch_data(url):
    print(f"Fetching data from {url}")
    await asyncio.sleep(2)  # Simulate network delay
    print(f"Finished fetching data from {url}")

async def main():
    urls = ["https://example.com", "https://python.org", "https://openai.com"]
    
    # Run all coroutines concurrently
    await asyncio.gather(*[fetch_data(url) for url in urls])

# Running the event loop
asyncio.run(main())