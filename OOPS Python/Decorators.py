# PYTHON DECORATORS : -----

#  A decorator is a function that takes another function, returns a new function that modifies the behaviour of original function.
#  Decorators are a powerful & Versatile tool , allows to modify the behaviour & methods.
# Its a way to extend the functionality of a function or method without modifying its source code.


# Syntax :
# @decorator_name(arguments)
#  def my_name () :
#     pass


# Used to add functionality to function & method, such as logging, memorization & acccess control.


def greet(fx):
    def mfx(*args, **kwargs):
        print("Good Morning")
        fx(*args, **kwargs)
        print("Thanks for using this function")
    return mfx


@greet
def hello():
    print("Hello world")


@greet
def add(a, b):
    print(a+b)


# greet(hello)()
hello()
# greet(add)(1, 2)
add(1, 2)

#END!!!!