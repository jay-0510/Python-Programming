#ARMSTONG NUMBER ---- Checking 
def is_armstrong(num):
    # Convert number to string to find the number of digits
    digits = str(num)
    num_digits = len(digits)

    # Calculate the sum of digits raised to the power of the number of digits
    total = 0
    for digit in digits:
        total += int(digit) ** num_digits

    # Check if the sum is equal to the original number
    return total == num

# Test the function with the number 1634
print(is_armstrong(1634))  # Output: False