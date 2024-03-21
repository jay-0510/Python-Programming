#Functions:
"A function is a block of code that performs a specific task whenever it is called. In bigger programs, where we have large amounts of code, it is advisable to create or use existing functions that make the program flow organized and neat."

#Built In Functions:
#These functions are defined and pre-coded in python. Some examples of built-in functions are as follows:
"min(), max(), len(), sum(), type(), range(), dict(), list(), tuple(), set(), print(),"

#USER DEFINED FUNCTIONS:
#We can create functions to perform specific tasks as per our needs. Such functions are called user-defined functions.

#Redundancy - DECREASES 
#Reusability - INCREASES 

def name(fname, lname):
  print("Hello,", fname, lname)
name("Prachi", "Patel")



def calculateGmean(a, b):
  mean = (a * b) / (a + b)
  print(mean)
def isGreater(a, b):
  if (a > b):
    print("First number is greater")
  else:
    print("Second number is greater or equal")


def isLesser(a, b):
  pass
a = 9
b = 8
isGreater(a, b)
calculateGmean(a, b)





# the use of user-defined functions
def add_numbers(x,y):
   sum = x + y
   return sum
num1 = 5
num2 = 6
print("The sum is", add_numbers(num1, num2))

#Multiply the function (number)
def multiply_numbers(a,b):
  product = a * b
  return product
n1 = 5
n2 = 6
print("The product is", multiply_numbers(n1, n2))