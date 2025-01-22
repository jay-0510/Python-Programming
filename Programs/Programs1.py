#1 -- Python function that prints out the pascal triangle 
def generate_pascals_triangle(num_rows):
    triangle = []

    for i in range(num_rows):
        row = [1] * (i + 1)

        # Calculating values for the current row
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]

        triangle.append(row)

    # Printing the Pascal's Triangle
    for row in triangle:
        print(" ".join(map(str, row)).center(num_rows * 2))

# Example usage
num_rows_to_generate = 5
generate_pascals_triangle(num_rows_to_generate)
#This function, generate_pascals_triangle, takes an argument num_rows and prints Pascal's Triangle up to the specified number of rows.


print ("--------------")


#2 - Python function to check whether a string is a pangram or not
def is_pangram(input_string):
    alphabet_set = set("abcdefghijklmnopqrstuvwxyz")
    input_set = set(input_string.lower())

    return alphabet_set.issubset(input_set)

# Example usage
test_string = "The quick brown fox jumps over the lazy dog"
result = is_pangram(test_string)

if result:
    print(f'"{test_string}" is a pangram.')
else:
    print(f'"{test_string}" is not a pangram.')


print ("--------------")


#3 - Python Program seprated sequence words as input and prints the words in a hyphen function seprated sequence.
def sort_words(input_string):
    words = input_string.split('-')
    sorted_words = sorted(words)
    sorted_sequence = '-'.join(sorted_words)
    
    return sorted_sequence
input_sequence = input("Enter a hyphen-separated sequence of words: ")
sorted_sequence = sort_words(input_sequence)
print("Sorted sequence:", sorted_sequence)


print ("--------------")


#4 -- Write a python program to access a function inside a function
def outer_function():
    def inner_function():
        print("Hello from the inner function!")

    inner_function()  # Call the inner function
outer_function()


print ("--------------")


#5 -- Python Program to detect the number of local variables declared in python 
def my_function():
    x = 1
    y = 2
    z = 3
    w = 4

    local_vars = locals()
    num_local_vars = len(local_vars)
    print(f"Number of local variables: {num_local_vars}")
my_function()


print ("--------------")


#6 -- Python code that invokes after a specified period of time
import time
def square(num):
     return num * num

number = 5
result = 0
print('-----')
# Wait for 2 seconds
time.sleep(2)

result = square(number)
print(result)


print ("--------------")