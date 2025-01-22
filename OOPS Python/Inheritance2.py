#  MULTIPLE INHERITANCE ----

# Allows a class to inherit attributes & methods from multiple parent classes.
# Useful in a situation where a class neeed to inherit functional from multiple sources.

# Syntax :
# class childclass ( Parentclass1, Parentclass2, Parentclass3 ):

class Employee:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(f"The name is {self.name}")


class Dancer:
    def __init__(self, dance):
        self.dance = dance

    def show(self):
        print(f"The dance is {self.dance}")


class DancerEmployee(Employee, Dancer):
    def __init__(self, dance, name):
        self.dance = dance
        self.name = name


o = DancerEmployee("Dhrishi", "Disha")
print(o.name)
print(o.dance)
o.show()
print(DancerEmployee.mro())
