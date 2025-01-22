#PALINDROME NUMBER ---- Checking
def is_palindrome(n):
    return str(n) == str(n)[::-1]



#Highest Palindrome Product of two 3-digit number
def is_palindrome(n):
    return str(n) == str(n)[::-1]

max_palindrome = 0   #variable is initialized to 0.
for i in range(999, 100, -1):
    for j in range(999, 100, -1):
        if is_palindrome(i*j) and i*j > max_palindrome:
            max_palindrome = i*j
print(max_palindrome)




print("------")
#using if else
def is_palindrome(num):
    # Convert number to string and reverse it
    num_str = str(num)
    reversed_num_str = num_str[::-1]

    # Check if the original number and the reversed number are the same
    if num_str == reversed_num_str:
        return True
    else:
        return False

# Test the function with some examples
print(is_palindrome(121))  # Output: True
print(is_palindrome(12321))  # Output: True
print(is_palindrome(1001))  # Output: True
print(is_palindrome(-1234))  # Output: False