#36 KEYWORDS

#Keywords are used to define the syntax of the coding. 
#The keyword cannot be used as an identifier, function, or variable name. All the keywords in Python are written in lowercase except True and False.
#They help in identifying the meaning and purpose of a particular piece of code.

"Python keywords cannot be used as identifiers."
import keyword
# printing all keywords at once using "kwlist()"
print("The list of keywords is : ")
print(keyword.kwlist)



#TRUE FALSE & NONE 
print(False == 0) #False = 0 
print(True == 1) #True = 1
print(True + True + True)
print(True + False + False)
print(None == 0)  #None isn’t equal to 0 or an empty list ([]).Different from both , represent absence value.
                   #It's not zero, negative or positive; it doesn’t represent “false” or “no”. 
print(None == [])



#WITH -- wrap the execution of block of code within methods defined by context manager.
#used for better resource management and ensures that the file is properly closed after the block is executed.
with open('file_path', 'w') as file:
	file.write('hello world !')
 
 
#AS -- #used to create the alias for the module imported. i.e giving a new name to the imported module.
import math as jay
print(jay.factorial(10))



#PASS -- null statement in python.Nothing happens when this is encountered.prevent indentation errors and used as a placeholder.
n = 10
for i in range(n):
	pass


# IF, ELSE , ELIF STATEMENTS : control statement for decision making.
#IF - Truth expression forces control to go in “if” statement block.
#ELSE - False expression forces control to go in “else” statement block.
#Elif -- short for “else if“

i = 20
if (i == 10):
	print("i is 10")
elif (i == 20):
	print("i is 20")
else:
	print("i is not present")




#FOR, WHILE , BREAK , CONTINUE :
#FOR - used to control flow and for looping.
#WHILE - used to control flow and for repeating some task until certain condition becomes false.
#BREAK -  used when we want to stop executing loop completely.
#CONTINUE - used to skip the rest of the loop iteration and jump directly to next iteration.
for i in range(10):
	print(i, end=" ")
	if i == 6:
		break

print()
i = 0
while i < 10:
	if i == 6:
		i += 1
		continue
	else:
		print(i, end=" ")
	i += 1

#END!!!