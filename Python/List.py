# Lists are ordered collection of data items.
# They store multiple items in a single variable.
# List items are separated by commas and enclosed within square brackets [].
# Lists are changeable meaning we can alter them after creation.

lst1 = ["Mbaape", "Ronaldo", "Neymar"]
lst2 = ["Virat", "Dhoni", "ABD"]
print(lst1)
print(lst2)

# LIST INDEX
"The first item has index [0], second item has index [1], third item has index [2] and so on."


# Negative Indexing:
colors = ["pele", "messi", "Bruno", "pogba", "pepe"]
#          [-5]    [-4]    [-3]     [-2]      [-1]
print(colors[-1])
print(colors[-3])
print(colors[-5])


# RANGE OF INDEX:
# You can print a range of list items by specifying where you want to start, where do you want to end and if you want to skip elements in between the range.


# syntax :
"listName[start : end : jumpIndex]"

animals = ["cat", "dog", "bat", "mouse",
           "pig", "horse", "donkey", "goat", "cow"]
print(animals[3:7])  # using positive indexes
print(animals[-7:-2])  # using negative indexes'
"When no end index is provided, the interpreter prints all the values till the end."


# LIST COMPREHENSION :
"List comprehensions are used for creating new lists from other iterables like lists, tuples, dictionaries, sets, and even in arrays and strings."

# Accept the item with small letter with o in the new list:
names = ["Ramos", "Foden", "Bruno", "Haaland", "kante"]
namesWith_O = [item for item in names if "o" in item]
print(namesWith_O)
