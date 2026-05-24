# Solution 1 -- Ask user for a string and check whether it is palindrome or not

text = input("Enter the String: ")  # takes input string
reverse_text = text[::-1]  # Reverse string

if text == reverse_text:  # Compare
    print("Palindrome")
else:
    print("Not palindrome")


# Solution 2 - Integers Compute Average
numbers = [10, 20, 30, 40, 50]
avg = sum(numbers) / len(numbers)
print("Average: ", avg)

# Solution 3 - Merge Two lists and Sort Results
list1 = [1, 2, 3, 5]
list2 = [2, 1, 9, 8]

result = list1 + list2  # Merge Lists
result.sort()     # Sort list
print(result)

# Solution 4 - Create Tuple of even & Odd numbers
numbers = (1, 2, 3, 4, 5, 6)

# Empty lists
odd = []
even = []

for num in numbers:  # check numbers
    if num % 2 == 0:
        even.append(num)
    else:
        odd.append(num)

# convert to tuple
even_tuple = tuple(even)
odd_tuple = tuple(odd)

print(even_tuple)
print(odd_tuple)

# Solution 5 -- Student marks dictionary menu program
students = {}  # Empty Dictionary

while True:
    choice = input(
        "A: Add  B: Update C: Search D: Display E: Exit : "
    )

    # Add Students
    if choice == "A":
        name = input("Student Name: ")
        marks = int(input("Marks: "))
        students[name] = marks

     # Update marks

    elif choice == "B":
        name = input("Student name: ")
        if name in students:
            marks = int(input("New marks: "))
            students[name] = marks

    # Search student

    elif choice == "C":
        name = input("Student name: ")
        if name in students:
            print(students[name])
        else:
            print("Not Found")

    # Display all

    elif choice == "D":
        print(students)

    elif choice == "E":
        break

# Solution 6 -- Word Length Dictionary

words = ["cristiano", "mbappe", "messi", "LukaModric", "Dembele"]
result = {}  # Empty dictionary

for word in words:
    result[word] = len(word)
print(result)

# Solution 7 -- Count Spaces in String
text = input("Enter String: ")
count = 0
for char in text:
    if char == " ":
        count += 1

print("Spaces = ", count)

# Solution 8 -- Check whether tw lists share no common elements
list1 = [1, 2, 3, 4]
list2 = [5, 6, 7]

# Convert to sets
set1 = set(list1)
set2 = set(list2)

if set1.isdisjoint(set2):  # Check common elements
    print("No common elements")
else:
    print("Common elements exist")

# Solution 9 -- Print Duplicate Elements from list
numbers = [1, 2, 3, 4, 4, 2, 8, 5, 1]
duplicates = set()

for num in numbers:
    if numbers.count(num) > 1:
        duplicates.add(num)

print(duplicates)

# Solution 10 -- Unique Character and Count
text = input("Enter string: ")

unique_char = set(text)
print(unique_char)

print("Count = ", len(unique_char))
