# Joining Sets:
'Sets in python more or less work in the same way as sets in mathematics. We can perform operations like union and intersection on the sets just like in mathematics.'


# UNION() & UPDATE ():
'The union() and update() methods prints all items that are present in the two sets.'
'The union() method returns a new set whereas update() method adds item into the existing set from another set.'

players = {"Messi", "Mbaape", "Neymar", "Ronaldo"}
players2 = {"Maradona", "Zidane", "Kaka", "Pele"}
players3 = players.union(players2)
print(players3)

cities = {"Tokyo", "Madrid", "Barcelona", "Paris"}
cities2 = {"Tokyo", "Seoul", "NYC", "Madrid"}
cities.update(cities2)
print(cities)


# INTERSECTION() & INTERSECTION_UPDATE()
'The intersection() and intersection_update() methods prints only items that are similar to both the sets. The intersection() method returns a new set whereas intersection_update() method updates into the existing set from another set.'

cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Tokyo", "Seoul", "Kabul", "Madrid"}
cities.intersection_update(cities2)
print(cities)


# DIFFERENCE() & DIFFERENCE_UPDATE()
'The difference() and difference_update() methods prints only items that are only present in the original set and not in both the sets. The difference() method returns a new set whereas difference_update() method updates into the existing set from another set.'
cities = {"Tokyo", "Madrid", "Berlin", "Delhi"}
cities2 = {"Seoul", "Kabul", "Delhi"}
print(cities.difference(cities2))
