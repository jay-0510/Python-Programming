class Cricketer:
    # Blueprint for every cricketer
    # Instance attributes - unique to each object
    def __init__(self, name, matches, runs):
        self.name = name
        self.matches = matches
        self.runs = runs

    # Instance method - uses self to access object's own data
    def cric_avg(self):
        if not self.runs:        # edge case - empty list crash rokta hai
            return 0
        return sum(self.runs) / len(self.runs)

    # display_profile - parent version, prints basic cricketer info
    def display_profile(self):
        print("Name    :", self.name)
        print("Matches :", self.matches)
        print("Runs    :", self.runs)
        # apna hi method call kar raha hai
        print("Average :", self.cric_avg())

    # Magic method - print(object) karo toh automatically yeh chalta hai
    def __str__(self):
        return f"Cricketer : {self.name} | Average : {self.cric_avg()} | Matches : {self.matches}"


class AllRounder(Cricketer):
    # Inheritance - Cricketer ki saari cheezein free mein milti hain
    def __init__(self, name, matches, runs, wickets):
        super().__init__(name, matches, runs)  # parent ka kaam parent kare
        self.wickets = wickets                 # sirf apna extra attribute

    # Method Overriding - same name, AllRounder ka apna version
    # Polymorphism - ek method name, alag alag behaviour by object type
    def display_profile(self):
        super().display_profile()          # parent ka display_profile() chala
        print("Wickets :", self.wickets)   # uske baad wickets add karo


class Team:
    # Container class - NO inheritance, just holds list of players
    # "Has a" relationship, not "Is a" relationship
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []          # empty list, players baad mein aayenge

    def add_player(self, player):
        self.players.append(player)    # list mein player add karo

    def top_score(self):
        if not self.players:
            return None
        # max() + lambda - har player ka avg compare karke sabse bada dhundo
        return max(self.players, key=lambda player: player.cric_avg())

    def team_average(self):
        if not self.players:
            return 0
        # Generator expression - har player ka avg nikalo, sum karo, divide karo
        total = sum(player.cric_avg() for player in self.players)
        return total / len(self.players)

    def display_squad(self):
        for player in self.players:
            player.display_profile()   # Polymorphism in action
            print()                    # blank line between players


# Object creation - har baar __init__ automatically runs
cric1 = Cricketer("Rohit Sharma", 45, [
                  82, 53, 120, 83, 67, 90, 55, 110, 23, 78])
cric1.display_profile()

cric2 = Cricketer("MS Dhoni", 0, [])
cric2.display_profile()

ar1 = AllRounder("Hardik Pandya", 8, [55, 30, 70, 20, 45, 60, 35, 40], 12)
ar1.display_profile()

india = Team("India")
india.add_player(cric1)
india.add_player(cric2)
india.add_player(ar1)

india.display_squad()
print("Top Scorer:", india.top_score().name)
print("Team Average:", india.team_average())
print(india.top_score())
