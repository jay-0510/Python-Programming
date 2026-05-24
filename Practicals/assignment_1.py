# Solution - 1

name = input("Enter your name: ")  # Take name input
age = int(input("Enter your age: "))  # take the name input
print(f"Hello {name}, you are {age} years old")

# Solution 2
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

# Arithemetic operations
print("Sum = ", num1 + num2)
print("Difference = ", num1 - num2)
print("Product = ", num1 * num2)
print("Quotient = ", num1 / num2)

# Solution 3

num1 = int(input("Enter first integer: "))
num2 = int(input("Enter second integer: "))
num3 = float(input("Enter float value: "))

num1 = float(num1)  # Convert integers to float
num2 = float(num2)
Avg = (num1 + num2 + num3) / 3  # Calculate Average
print("Average =", Avg)

# Solution 4

value = input("Enter number as string: ")

int_value = int(value)  # Convert values
float_value = float(value)
str_value = str(value)

# Print values and types

print(int_value, type(int_value))
print(float_value, type(float_value))
print(str_value, type(str_value))

# Solution 5
x = 10 + 3 * 2 ** 2

print(x)

# Exponent first 2 ** 2 = 4
# Multiply second -- 3 * 4 = 12
# Addition last -- 10 + 12

# Soltuin 6 - Swapping
# Take input
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

# Swap values
a, b = b, a

print("a =", a)
print("b =", b)

# Solution 7 - Celsius to Fahrenheit

celsius = input("Enter temperature in Celsius: ")
celsius = float(celsius)

Fahreheit = (celsius * 9/5) + 32
print("Fahreheit: ", Fahreheit)

# Solution 8 -- Area of Circle

r = float(input("Enter radius: "))
area = 3.14 * r * r

print("Area =", area)

# Solution 9 -- Simple Interest
# Inputs
P = float(input("Principal: "))
R = float(input("Rate: "))
T = float(input("Time: "))

# Calculate SI
SI = (P * R * T) / 100

print("Simple Interest =", SI)

# Solution 10 --  Integer & Fractional Part
# Input decimal number
num = float(input("Enter decimal number: "))

# Integer part
integer_part = int(num)

# Fractional part
fractional_part = num - integer_part

print("Integer Part =", integer_part)
print("Fractional Part =", fractional_part)
