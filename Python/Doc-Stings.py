'DOCSTRING IN PYTHON '
#Python docstrings are the string literals that appear right after the definition of a function, method, class, or module.

def square(n):
    '''Takes in a number n, returns the square of n'''
    print(n**2)
square(5)

#'''Takes in a number n, returns the square of n''' is a docstring which will not appear in output



'''Python COMMENTS & Python DOCSTRING'''
'COMMENTS';
#Comments are descriptions that help programmers better understand the intent and functionality of the program. They are completely ignored by the Python interpreter.

'Doctrings';
#As mentioned above, Python docstrings are strings used right after the definition of a function, method, class, or module (like in Example 1). They are used to document our code.

def square(n):
    '''Takes in a number n, returns the square of n'''
    return n**2

print(square.__doc__)