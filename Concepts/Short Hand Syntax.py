#IF ELSE in one line 
'There is also a shorthand syntax for the if-else statement that can be used when the condition being tested is simple and the code blocks to be executed are short.'

a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")


a = 550000
b = 3003
print("A") if a > b else print("=") if a == b else print("B")

c = 9 if a>b else 0
print(c)