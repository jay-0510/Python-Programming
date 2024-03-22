# walrus operator :=

# := SYNTAX
# new to Python 3.8
# assignment expression aka walrus operator
# assigns values to variables as part of a larger expression
# This can be useful when you need to use a value multiple times in a loop, but don't want to repeat the calculation.


# happy = True
# print(happy)

# print(happy := True)

# foods = list()
# while True:
#   food = input("What food do you like?: ")
#       if food == "quit":
#           break
#   foods.append(food)

foods = list()
while (food := input("What food do you like?: ")) != "quit":
    foods.append(food)


# Walrus Operator in an if statement:
names = ["Ronaldo", "Messi", "Neymar"]

if (name := input("Enter a name: ")) in names:
    print(f"Hello, {name}!")
else:
    print("Name not found.")
