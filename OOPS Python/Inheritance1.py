# SINGLE INHERITANCE ---

# Class inherits properties & behaviour from a single parent class.
# Simplest & most common form of inheritance.

# syntax: ---
# class childclass (Parentclass) :

class Football:
    def func_1(self):
        print("Cristiano Ronaldo is best footballer")

# now, we will create the Derived class


class Player(Football):
    def func_2(self):
        print("Lionel Messi is second best")


# Driver's code
object = Player()
object.func_1()
object.func_2()
