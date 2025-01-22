#Tuples are immutable, hence if you want to add, remove or change tuple items, then first you must convert the tuple to a list. Then perform operation on that list and convert it back to tuple.
countries = ("Spain", "Italy", "India", "England", "Germany")
temp = list(countries)
temp.append("Russia")  #add item
temp.pop(3)  #remove item
temp[2] = "Finland"  #change item
countries = tuple(temp)
print(countries)

#METHODS OF TUPLES:
"count() Method"
"The count() method of Tuple returns the number of times the given element appears in the tuple."

# Index Method:
#The Index() method returns the first occurrence of the given element from the tuple.
