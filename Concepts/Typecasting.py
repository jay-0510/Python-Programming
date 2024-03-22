"The conversion of one data type into the other data type is known as type casting in python or type conversion in python."

#Two Types of Typecasting:

"1. Explicit typecasting"
#The conversion of one data type into another data type, done via developer or programmer's intervention or manually as per the requirement, is known as explicit type conversion.

string = "10"
number = 7
string_number = int(string) #throws an error if the string is not a valid integer
sum= number + string_number
print("The Sum of both the numbers is: ", sum)


"2.Implicit type casting:"
#According to the level, one data type is converted into other by the Python interpreter itself (automatically). This is called, implicit typecasting in python.
# Python automatically converts
# a to int
a = 7
print(type(a))
 
# Python automatically converts b to float
b = 3.0
print(type(b))
 
# Python automatically converts c to float as it is a float addition
c = a + b
print(c)
print(type(c))



#Extra Works:
a = "1"
# a = 1
b = "2"
# b = 2
print(int(a) + int(b))

# Implicit TypeCasting
c = 1.9
d = 8

print(c + d)