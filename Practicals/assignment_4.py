# Solution - 1 -- Create BankAccount class with deposit, withdraw and check balance

from abc import ABC, abstractmethod


class BankAccount:
    # Initializes the standard identity and starting funds for each account.
    def __init__(self, account_number, owner_name, balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

# Adding money
    # Increases the account balance by the deposited amount.
    def deposit(self, amount):
        self.balance += amount
        print("Deposited: ", amount)

# Withdrawing money
    # Prevents overdrafts by checking if the account actually has enough money.
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print("Withdrawn: ", amount)
        else:
            print("Insufficient Balance")

# Showing Balance
    def check_balance(self):
        print("Balance =", self.balance)


# Object Creation
acc1 = BankAccount(101, "Jay", 10000)
acc1.deposit(20000)
acc1.withdraw(1000)
acc1.check_balance()


# Solution - 2 -- Book class with reviews

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
# store reviews
        # an empty list to store multiple reviews for this specific book.
        self.reviews = []

# Adding review
    def add_review(self, review):
        # Appends a new review string into the self.reviews list.
        self.reviews.append(review)

# Counting the reviews
    def count_reviews(self):
        # len() to find and return the total number of reviews stored.
        return len(self.reviews)

# Display reviews
    def show_reviews(self):
        print(self.reviews)


book1 = Book("Harry Potter", "Lovely")
book1.add_review("Best")
book1.add_review("Must read book")
print(book1.count_reviews())

# Solution - 3 -- Student class using Encapsulation


class Student:
    def __init__(self, name, roll_no, marks):
        # The single underscore (_) means these variables are "protected" (private).
        self._name = name
        self._roll_no = roll_no
        self._marks = marks

# Getter
    def get_marks(self):
        # Safe way to read the hidden _marks variable from outside the class.
        return self._marks

# Setter
    # Acts as a gatekeeper. It validates data before updating the variable.
    def set_marks(self, marks):
        if marks >= 0:  # validation
            self._marks = marks
        else:
            print("Invalid Marks")


stu1 = Student("jay", 10, 90)
print(stu1.get_marks())
# Changes marks safely using the setter, ensuring negative numbers cannot be entered.
stu1.set_marks(95)
print(stu1.get_marks())

# Solution 4 -- Shape Class and Overriding
# Method Overriding - Parent method replaced by child method


class Shape:
    def area(self):  # generic template method that child classes will replace.
        print("Area Method")


class Circle (Shape):
    # Overrides the parent method to calculate area specifically for a circle.
    def area(self):
        r = 5
        print(3.14 * r * r)


class Rectangle (Shape):
    # Overrides the parent method to calculate area specifically for a rectangle.
    def area(self):
        l = 4
        b = 3
        print(l * b)


class Triangle (Shape):
    def area(self):  # Overrides the parent method to calculate area specifically for a triangle
        b = 4
        h = 5
        print(0.5 * b * h)


c = Circle()  # creates circle object
c.area()  # Run's circlespecific area method,completely ignore generic method

# Solution - 5 -- Vehicle Inheritance


class Vehicle:
    def __init__(self, brand, model):  # Core properties for all vehicles share
        self.brand = brand
        self.model = model


class Car(Vehicle):
    def __init__(self, brand, model, seats):
        super().__init__(brand, model)  # Super () - Calls parent constructor
        self.seats = seats  # unique property specifically for cars.


class Bike:
    def __init__(self, brand, model, engine_cc):
        super().__init__(brand, model)
        self.engine_cc = engine_cc


car1 = Car("BMW", "X1", 5)
print(car1.brand)

# Solution - 6 -- Employee Abstraction


class Employee(ABC):
    # Declares a rule. Every child class MUST create its own 'calculate_salary'.
    @abstractmethod   # Forces rule to implement by child class
    def calculate_salary(self):
        pass


class Intern(Employee):
    def calculate_salary(self):  # fulfills the rule of salary for interns
        print("15000")


class FullTimeEmployee(Employee):
    def calculate_salary(self):  # fulfills the rule of salary for full time worker
        print("500000")


# Creates an intern object and return salary.
obj = Intern()
obj.calculate_salary()

# Solution 7 -- Constructor Overloading using default parameter
# Python doesn't support direct constructor overloading


class Person:
    def __init__(self, name, age=None, address=None):
        self.name = name
        self.age = age
        self.address = address


p1 = Person("Jay")
p2 = Person("Jay", 22)
p3 = Person("Jay", 22, "Anand")

# Solution - 8 -- Class Variable Player_count


class Player:

    # Class Variable - Shared by all players. Tracks total players globally across the game.
    player_count = 0

    def __init__(self, name, level):
        # Unique to each individual player (Instance variables).
        self.name = name
        self.level = level

    # Increase Count
        # Accesses the class directly to increase the global counter on every new player.
        Player.player_count += 1


# Unique data is kept separate for each player instance.
p1 = Player("Jay", 10)
p2 = Player("Ronaldo", 7)

# Prints 2 because the global counter updated automatically twice.
print(Player.player_count)

# Solution - 9 - Multipe Inheritance


class Herbivore:
    def eat_grass(self):
        print("Eats Grass")


class Carnivore:
    def eat_meat(self):
        print("Eats Meat")


class Omnivore:
    def eat_both(self):
        print("Eat Both")


class Bear(Herbivore, Carnivore, Omnivore):  # Bear inherits multiple classes.
    pass


b = Bear()  # Creates bear object
b.eat_grass()  # Bear successfully uses method from different parent classes.
b.eat_meat()
b.eat_both()
