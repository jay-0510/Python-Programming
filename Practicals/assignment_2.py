# Solution - 1 - Salary Tax Calculator
salary = float(input("Enter salary: "))  # Salary Input

if salary < 30000:  # Check Tax_rate
    tax_rate = 5
elif salary <= 70000:
    tax_rate = 10
else:
    tax_rate = 25

print("Tax Rate= ", tax_rate, "%")

# Solution 2 -- Print even numbers between A and B


def print_even(a, b):
    for i in range(a, b+1):  # loops from a to b

        if i % 2 == 0:  # checks even number
            print(i)


print_even(2, 10)  # function call


# Solution 3 --Print Digits of numbers

def print_digits(n):

    n = str(n)  # Convert number to string
    for digit in n:  # Print n digit
        print(digit)


print_digits(312)  # Function call

# Solution 4 --  Counts digits in Number


def count_digits(n):

    # Convert number to string
    n = str(n)

    # Length gives digit count
    return len(n)


# Function call
print(count_digits(98765))


# Soution 5 -- Sum of digits
def sum_of_digits(n):

    total = 0

    # Convert to string

    n = str(n)
    for digit in n:
        total += int(digit)

    return total


print(sum_of_digits(1234))

# Solution 6 -- Numbers divisible by 3 and 5
for i in range(1, 101):

    if i % 3 == 0 and i % 5 == 0:
        print(i)

# Solution 7 -- Positive or Negative Quit
while True:

    # Take input
    value = input("Enter number or Quit: ")

    # Stop program
    if value == "Quit":
        break

    # Convert to integer
    num = int(value)

    # Check positive/negative
    if num >= 0:
        print("Positive")

    else:
        print("Negative")

# Solution 8 --- Simple calculator


def calculator(a, b, operation):

    # Addition
    if operation == "+":
        return a + b

    # Subtraction
    elif operation == "-":
        return a - b

    # Multiplication
    elif operation == "*":
        return a * b

    # Division
    elif operation == "/":
        return a / b

    else:
        return "Invalid Operation"


# Function calls
print(calculator(10, 5, "+"))
print(calculator(10, 5, "-"))
print(calculator(10, 5, "*"))
print(calculator(10, 5, "/"))


# Solution 9 --  Prime Number Check

def is_prime(n):

    if n < 2:
        return False

    # Checks divisibility
    for i in range(2, n):

        # If divisible not prime
        if n % i == 0:
            return False

    # Other wise Prime
    return True


# Function_call
print(is_prime(7))

# Solution 10 -- Number Guessing Game

secret = 7  # Secret Number

while True:

    guess = int(input("Guess the number: "))  # user guess

    if guess > secret:  # Condition for guess
        print("Too High")

    elif guess < secret:
        print("Too Low")

    else:
        print("Correct!!")
        break
