#LIST.SORT()
"This method sorts the list in ascending order. The original list is updated"
players = ["Ronaldo", "modric", "kroos", "marcelo"]
players.sort()
print(players)

#if want to print in descending order; then REVERSE=TRUE
footballers = ["Mbaape", "Rashford", "Silva", "Zidane"]
footballers .sort(reverse=True)
print(footballers )

#REVERSE():
"This method reverses the order of the list."

#INDEX():
'This method returns the index of the first occurrence of the list item.'

#COUNT():
'Returns the count of the number of items with the given value.'

#COPY():
'Returns copy of the list. This can be done to perform operations on the list without modifying the original list.'

#APPEND():
'This method appends items to the end of the existing list.'
colors = ["voilet", "indigo", "blue"]
colors.append("green")
print(colors)

#CONCATENATING THE LIST:
CARS = ["Mercedes", "BMW", "Bugaati", "Mustang"]
CARS2 = ["Ferrari", "Fortuner", "Thar"]
print(CARS + CARS2)




#INSERT()
'This method inserts an item at the given index. User has to specify index and the item to be inserted within the insert() method.'
marvels = ["superman", "batman", "hulk", "THOR"]
#           [0]        [1]      [2]
marvels.insert(1, "spiderman")   
print(marvels)



#EXTEND()
'This method adds an entire list or any other collection datatype (set, tuple, dictionary) to the existing list.'
#add a list to a list
colors = ["voilet", "indigo", "blue"]
rainbow = ["green", "yellow", "orange", "red"]
colors.extend(rainbow)
print(colors)

