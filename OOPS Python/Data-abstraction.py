# Data-Abstraction -----

# performs data hiding by adding the double underscore(__) as a prefix to the attribute which is to be hidden.
# After this, the attribute will not be visible outside of the class through the object.

# SYNTAX ----
# from abc import ABC
# class ClassName(ABC):

# Python program demonstrate
# abstract base class work
from abc import ABC, abstractmethod


class Car(ABC):
    def model(self):
        pass


class Lambo(Car):
    def model(self):
        print("Lamborghini Urus - 4Crore")


class Mercedes(Car):
    def model(self):
        print("Mercedes 4matic suv - 3Crore")


class BMW(Car):
    def model(self):
        print("BMW M5 - 2Crore")


class Porsche(Car):
    def model(self):
        print("Porsche Taycan - 2.5Crore")


# Driver code
x = Lambo()
x.model()

y = BMW()
y.model()

z = Mercedes()
z.model()

q = Porsche()
q.model()

#CARS!!! END !!!