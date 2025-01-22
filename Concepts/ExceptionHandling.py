#Exception handling is the process of responding to unwanted or unexpected events when a computer program runs.

#Exception handling deals with these events to avoid the program or system crashing, and without this process, exceptions would disrupt the normal operation of a program.
'Python has many built-in exceptions that are raised when your program encounters an error.'
'When these exceptions occur, the Python interpreter stops the current process and passes it to the calling process until it is handled. If not handled, the program will crash.'

#EXAMPLE:

a = input("Enter the number: ")

print(f"Multiplication table of {a} is: ")

try:
  for i in range(1, 11):
    print(f"{int(a)} X {i} = {int(a)*i}")

except:
  print("Invalid  Input!")
  print("Some imp lines of code")
  print("End of program")
