#Classwork - Python 

def check_voting_eligibility(age):
    if age >= 18:
        print("You are eligible to vote!")
    elif age > 0:
        print("You are not eligible to vote yet. You need to wait for {} more year(s).".format(
            18 - age))
    else:
        print("Invalid age. Please enter a positive number.")


# Get user input for age
try:
    age = int(input("Enter your age: "))
    check_voting_eligibility(age)
except ValueError:
    print("Invalid input. Please enter a valid age as a number.")
