# Strings are immutable
a = "!!!MASTER!! !!!!!!!!! MASTER"
print(len(a))
print(a)
print(a.upper()) #string to upper case.

print(a.lower())#string to lower case.

print(a.rstrip("!"))#removes any trailing characters.

print(a.replace("MASTER", "Rohan"))#replaces all occurences of a string with another string.

print(a.split(" "))#string at the specified instance and returns the separated strings as list items.

blogHeading = "introduction tO jS"
print(blogHeading.capitalize())#turns only the first character of the string to uppercase and the rest other characters of the string are turned to lowercase.

str1 = "Welcome to the Console!!!"
print(len(str1))
print(len(str1.center(50)))
print(a.count("MASTER"))

str1 = "Welcome to the Console !!!"
print(str1.endswith("!!!"))

str1 = "Welcome to the Console !!!"
print(str1.endswith("to", 4, 10))

str1 = "He's name is Dan. He is an honest man."
print(str1.find("ishh"))
# print(str1.index("ishh"))

str1 = "WelcomeToTheConsole"
print(str1.isalnum())
str1 = "Welcome"
print(str1.isalpha())

str1 = "hello world"
print(str1.islower())

str1 = "We wish you a Merry Christmas\n"
print(str1.isprintable())
str1 = "         "       #using Spacebar
print(str1.isspace())
str2 = "  "       #using Tab
print(str2.isspace())

str1 = "World Health Organization" 
print(str1.istitle())

str2 = "To kill a Mocking bird"
print(str2.istitle())

str1 = "Python is a Interpreted Language" 
print(str1.startswith("Python"))

str1 = "Python is a Interpreted Language" 
print(str1.swapcase())

str1 = "His name is Cristiano. Cristiano is an honest man."
print(str1.title())