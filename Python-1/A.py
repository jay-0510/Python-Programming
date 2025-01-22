# String
x = "Patel Jay"
print(x)
print ("Jay Patel!")
print (type(x))

# Integer 
y = 10
print(y)
print(type(y))

# FLoat 
a=10.3
b=12.1
c = a+b 
print(c)
print(type(c))

# Boolean Types
a = True 
b = False
print(type(a))
print(a)
print(b)
print(type(b))

# Complex
x= complex(3,5)
print(x)
print(type(x))

# List
friends =["Ronaldo","Messi", "Neymar", "Mbappe","Halland"]
print(friends)
print(friends[1])
print(friends[-1])
print(friends[0:])
print(friends[1:3])
friends[1]= "myself"
print(friends[1])

# Tuples

coordinates = (4, 5)
print(coordinates) 
print(coordinates[0])
print(coordinates[1])


# Range
x = range(5)
for n in x:
  print(n)
  
print ("---------")
x = range(3, 6)
for n in x:
  print(n)
  
  
# Dictionary 
print ("---------")

# Dictionaries
# converting the >> Jan >> Jannuary 
monthConverter = {
    "Jan":"January",
    "Feb":"February",
    "Mar":"March",
    "Apr":"April",
    "May":"May",
    "Jun":"June",
    "Jul":"July",
    "Aug":"August",
    "Sep":"September",
    "Oct":"October",
    "Nov":"November",
    "Dec":"December",  # bunch of the key and it have the sepcific value
    0:"zero"
}

print (monthConverter["Aug"]) 
print(monthConverter.get("Dec"))
print(monthConverter.get("Love"))
print(monthConverter.get("Love", "Not a valid key"))
print(monthConverter[0])

print ("---------")

thisset = {"apple", "banana", "cherry"}
print(thisset)

print ("---------")

print("Frozenset")
# Frozenset
animals = frozenset(["Lion", "BigBull", "bug-hunter"])
print("Lion" in animals) 
print("Tiger" in animals)

print ("---------")

#Binary tpye
x=bytes(4)
print(x)

print ("---------")

x=bytearray(4)
print(x)

print ("---------")

print("python is very important")