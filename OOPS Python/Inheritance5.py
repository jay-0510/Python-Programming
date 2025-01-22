# HIERARCHICAL INHERITANCE ---

# Here, Multiple sub classes inherit from a single base class.
# ( single base class acts as a parent class for multiple subclasses )

class Football:
    def __init__(self, Player):
        self.Player = Player

    def show_details(self):
        print("Player:", self.Player)


class Portugal(Football):
    def __init__(self, Player, Club):
        Football.__init__(self, Player)
        self.Club = Club

    def show_details(self):
        Football.show_details(self)
        print("Team: Portugal")
        print("Club:", self.Club)


class France(Football):
    def __init__(self, Player, Club):
        Football.__init__(self, Player)
        self.Club = Club

    def show_details(self):
        Football.show_details(self)
        print("Team: France")
        print("Club:", self.Club)


Portugal = Portugal("Cristiano Ronaldo", "Real Madrid")
Portugal.show_details()
France = France("Kylian Mbappe", "PSG")
France.show_details()
