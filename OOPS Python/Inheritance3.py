# MULTI-LEVEL INHERITANCE ---

# Derived class inherits from another derived class.
# Allows to build hierarchy of classes where one class build upon another, leading to more specialized class.

# syntax :
# class BaseClass :
# Bass classMode

# Class DerivedClass1 (BaseClass):
# Derived Class1 code

# Class DerivedClass2 (derivedClass) :
# Derived Class2

class Football:
    def __init__(self, Player, Team):
        self.Player = Player
        self.Team = Team

    def show_details(self):
        print(f"Player: {self.Player}")
        print(f"Team: {self.Team}")


class Portugal(Football):
    def __init__(self, Player, Club):
        Football.__init__(self, Player, Team="Portugal")
        self.Club = Club

    def show_details(self):
        Football.show_details(self)
        print(f"Club: {self.Club}")


class CR7(Portugal):
    def __init__(self, Player2, color):
        Portugal.__init__(self, Player2, Club="Real Madrid")
        self.color = color

    def show_details(self):
        Portugal.show_details(self)
        print(f"Color: {self.color}")


o = Portugal("Cristaino Ronaldo", "Real Madrid")
o.show_details()
