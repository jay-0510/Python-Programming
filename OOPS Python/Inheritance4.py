# HYBRID INHERITANCE --

# A hybrid inheritance model is a combination of both single and multiple inheritance.
# Multiple inheritance is used to inherit the properties of Multiple base class into single derived class.
# Single Inheritance is used to inherit the properties of the derived class into sub derived class.


# syntax :
# class DerivedClass(Base1, Base2)

# Class BaseClass1 :
# ------

# Class BaseClass2 :
# ------

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_details(self):
        print("Name:", self.name)
        print("Age:", self.age)


class Person(Human):
    def __init__(self, name, age, address):
        Human.__init__(self, name, age)
        self.address = address

    def show_details(self):
        Human.show_details(self)
        print("Address:", self.address)


class Program:
    def __init__(self, program_name, duration):
        self.program_name = program_name
        self.duration = duration

    def show_details(self):
        print("Program Name:", self.program_name)
        print("Duration:", self.duration)


class Student(Person):
    def __init__(self, name, age, address, program):
        Person.__init__(self, name, age, address)
        self.program = program

    def show_details(self):
        Person.show_details(self)
        self.program.show_details()


program = Program("Computer Science", 4)
student = Student("Jay Patel", 20, "Glassboro, New Jersey USA", program)
student.show_details()
