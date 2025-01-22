"The enumerate function is a built-in function in Python that allows you to loop over a sequence (such as a list, tuple, or string) and get the index and value of each element in the sequence at the same time. "

# Loop over a list and print the index and value of each element
Player = ['Ronaldo', 'Messi', 'Mbappe']
for index, fruit in enumerate(Player):
    print(index, Player)
'The enumerate function returns a tuple containing the index and value of each element in the sequence. You can use the for loop to unpack these tuples and assign them to variables.'

# CHANGING STARTING OF INDEX:
# Loop over a list and print the index (starting at 1) and value of each element
fruits = ['apple', 'banana', 'mango']
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

# Real Example :
marks = [12, 56, 32, 98, 45, 1, 4]

# index = 0
# for mark in marks:
#   print(mark)
#   if(index == 3):
#     print("Master, awesome!")
#   index +=1

for index, mark in enumerate(marks, start=1):
    print(mark)
    if (index == 3):
        print("Jay, awesome!")
