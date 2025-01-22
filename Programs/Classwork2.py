#Class Work -2 
#nested if condition 
#input three integer numbers
a = int(input("Enter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))

# conditions to find largest
if a > b:
    if a > c:
        g = a
    else:
        g = c
else:
    if b > c:
        g = b
    else:
        g = c

# print the largest number
print("Greater  = ", g)


coordinate = (2,4)
print(type(coordinate))

person = {'name': 'jay', 'age': '20'}
print(type(person))