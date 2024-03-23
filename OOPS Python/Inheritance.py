# When a class derives from another class, The class will inherit all the public & Protected properties & methods from the parent class.
# In addition, it can have its own properties & methods....


class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def showDetails(self):
        print(f"The name of Employee: {self.id} is {self.name}")


class Programmer(Employee):
    def showLanguage(self):
        print("The default langauge is Python")


e1 = Employee("Jay Patel", 400)
e1.showDetails()
e2 = Programmer("Jatin Patel", 401)
e2.showDetails()
e2.showLanguage()
