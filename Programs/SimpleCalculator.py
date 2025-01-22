#EXERCISE :
" SIMPLE CALCULATOR ON PYTHON"

num1 = int(input("Enter first number: "))
num2 = int(input("Enter secomd number: "))
choice = int(input("\nEnter your choice:\n"))
if choice == 1:
  print("The sum of entered numbers is", num1 + num2)
elif choice == 2:
  print("The difference of entered numbers is", num1 - num2)
elif choice == 3:
  print("The product of entered numbers is", num1 * num2)
elif choice == 4:
  print("The divison of entered numbers is", num1 / num2)
elif choice == 5:
  print("The product of entered numbers is", num1 % num2)
elif choice == 6:
  print("The divison of entered numbers is", num1 // num2)
else:
  print("Invalid Operator !!!")
