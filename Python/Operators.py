#ARITHMETIC OPERATORS : Used to perform basic mathematical operations like addition, subtraction, multiplication, and division.
a = 5
b = 7
add = a + b 

sub = a - b 

mul = a * b 

mod = a % b 

p = a ** b 
print(add) 
print(sub) 
print(mul) 
print(mod) 
print(p) 

print ("---------")

#Relational Operators = Comparision Operators
#COMPARISON OPERATORS: compares the values. It either returns True or False according to the condition.
a = 13
b = 33

print(a > b) 
print(a < b) 
print(a == b) 
print(a != b) 
print(a >= b) 
print(a <= b) 

print ("---------")


#LOGICAL OPERATORS: Used to combine conditional statements.
a = True
b = False
print(a and b) 
print(a or b) 
print(not a) 

print ("---------")


#BITWISE OPEATORS : bits and perform bit-by-bit operations. These are used to operate on binary numbers.
a = 10
b = 5
print(a & b) 
print(a | b) 
print(~a)
print(~b) 
print(a ^ b) 
print(a >> 2) 
print(a << 2) 
 

print ("---------")


#ASSIGNMENT OPERATORS: Used to assign values to the variables.
a = 100
b = a 
print(b) 
b += a 
print(b) 
b -= a 
print(b) 
b *= a 
print(b) 
b <<= a 
print(b)

print ("---------")


#IDENTITY OPERATORS: Used to check if two values are located on the same part of the memory. Two variables that are equal do not imply that they are identical. 
a = 10
b = 20
c = a 
a = b

print(a is not b) 
print(a is c)

print ("---------")


#MEMBERSHIP OPERATORS: used to test whether a value or variable is in a sequence.
x = 24
y = 20
list = [10, 20, 30, 40, 50] 

if (x not in list): 
	print("x is NOT present in given list") 
else: 
	print("x is present in given list") 

if (y in list): 
	print("y is present in given list") 
else: 
	print("y is NOT present in given list") 

print ("---------")


