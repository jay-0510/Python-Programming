# Class is bluprint or a template for creating the objects.
# The User defined objects are created using the class keyword

class Person:
    name = "Jay"
    occupation = "Software Developer"
    networth = 100000000000

    def info(self):
        print(f"{self.name} is a {self.occupation}")


a = Person()
b = Person()
c = Person()

a.name = "shubham"
a.occupation = "Accountant"

b.name = "Het"
b.occupation = "HR"

c.name = "Kavya"
c.occupation = "Manager"

# print(a.name, a.occupation)
a.info()
b.info()
c.info()


# SELF PARAMETER ----
# The self parameter is a reference to the current instance of the class, and is used to access variables that belongs to the class.
# provided as the extra parameter inside the method definition.
# self is not a keyword
# Self is nothing but a placeholder for the current object.


class Details:
    name = "RONALDO"
    age = 20

    def desc(self):
        print("My name is", self.name, "and I'm", self.age, "years old.")


obj1 = Details()
obj1.desc()
