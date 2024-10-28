#ClassWork - Python

def even_or_odd(num):
    if num & 1 == 0:
        return "This Number is Even"
    else:
        return "This Number is odd"


1

num = int(input("Please Enter a Number : "))
result = even_or_odd(num)
print(f"{num} is {result}")


# input age
age = int(input("Enter Age : "))

# condition to check voting eligibility
if age >= 18:
    status = "Eligible"
else:
    status = "Not Eligible"

print("You are ", status, " for Vote.")


# Even Odd Program using Bitwise Operator
a = int(input("Please Enter a Number : "))
if (a & 1 == 1):
    print("This Number is Odd")
else:
    print("This Number is Even")
7
