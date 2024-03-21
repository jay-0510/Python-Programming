#DEF Function -- declare user defined functions.
def fun():
	print("Cristiano Ronaldo")
fun()


#CLASS Function --  declare user defined classes.
class Dog:
	attr1 = "mammal"
	attr2 = "dog"
	def fun(self):
		print("Its a", self.attr1)
		print("Its a", self.attr2)
Shuri = Dog()
print(Shuri.attr1)
Shuri.fun()


#LAMBDA -- used to make inline returning functions with no statements allowed internally. 
p = lambda x: x*x*x
print(p(7))


#RETURN -- used to return from the function.
#YIELD --  used like return statement but is used to return a generator.
# Return keyword
def fun():
	S = 0
	for i in range(10):
		S += i
	return S
print(fun())

# Yield Keyword
def fun():
	S = 0
	for i in range(10):
		S += i
		yield S

for i in fun():
	print(i)



#IMPORT -- used to include a particular module into current program.
#FROM --  used with import,used to import particular functionality from the module imported.
# import keyword
from math import factorial
import math
print(math.factorial(5))

# from keyword
print(factorial(5))


# del -- used to delete a reference to an object. Any variable or list value can be deleted using del.
my_variable1 = "Virat Kohli"
my_variable2 = "Rohit Sharma"
print(my_variable1)
print(my_variable2)
del my_variable1
del my_variable2
print(my_variable1) #NameError because the variables no longer exist.
print(my_variable2)



#GLOBAL -- used to define a variable inside the function to be of a global scope.
#NON- LOCAL - works similar to the global, but rather than global,  declares a variable to point to variable of outside enclosing function, in case of nested functions.
a = 15
b = 10
def add():
	c = a + b
	print(c)
add()
def fun():
	var1 = 10
	def gun():
		nonlocal var1
		var1 = var1 + 10
		print(var1)
	gun()
fun()


