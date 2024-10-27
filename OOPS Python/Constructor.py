# Special Method in a class used to create & Initialize an object of class.
# Constructor is invoked automatically when an object of a class is created.
# Unique function gets called automatically.

# syntax:
# def __init__(self,param1,param2):

# PARAMETRIZED CONSTRUCTORS:
# This constructor accepts arguments along with self
# These arguments can be used isnide a class to assign the values to the data members.
class Details:
    def __init__(self, animal, group):
        self.animal = animal
        self.group = group


obj1 = Details("Crab", "Crustaceans")
print(obj1.animal, "belongs to the", obj1.group, "group.")

# Default Constructor ----
# Constructor doesnt accept any argument fro the object & has only one argument..... self in the constructor


class Details:
    def __init__(self):
        print("animal Crab belongs to Crustaceans group")


obj1 = Details()


# General Example
class Person:

    def __init__(self, name, occ):
        print("Hey I am a person")
        self.name = name
        self.occ = occ

    def info(self):
        print(f"{self.name} is a {self.occ}")


a = Person("Jay", "Developer")
b = Person("Rohan", "HR")
a.info()
b.info()
# print(a.name)
# a.name = "Rohan"
# a.occ = "HR"
# a.info()
