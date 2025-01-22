#Python Program to print list of numbers using range and for loop
def print_numbers(n):
    print("List of numbers from 1 to " + str(n) + ":")
    for i in range(1, n + 1):
        print(i, end=" ")

print_numbers(10)




#Python Program to print first n prime numbers
def print_first_n_primes(n):
    primes = []
    num = 2

    while len(primes) < n:
        if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
            primes.append(num)
        num += 1

    print(f"The first {n} prime numbers are: {primes}")
print_first_n_primes(10)


#python program to multiply matrices
import numpy as np # type: ignore
def multiply_matrices(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result

# Example matrices
matrix1 = np.array([[1, 2, 3],
                    [4, 5, 6]])

matrix2 = np.array([[7, 8],
                    [9, 10],
                    [11, 12]])

# Multiply matrices
result_matrix = multiply_matrices(matrix1, matrix2)
# Print the result
print("Matrix 1:")
print(matrix1)

print("\nMatrix 2:")
print(matrix2)

print("\nResultant Matrix:")
print(result_matrix)


