#Iteration - Control Statement 
#STATE = one to another process under specific conditionwithin given time.
def calculate_pay(pay_type, hours, rate, salary):
  if pay_type == "HOURLY":
    if hours > 40:
      pay = rate * hours + rate * 1.5 * (hours - 40)
    else:
      pay = rate * hours
  else:
    pay = salary
  return pay

# extra
pay_type = input("Enter pay type (HOURLY or SALARY): ")
hours = float(input("Enter hours worked: "))
rate = float(input("Enter hourly rate (for hourly pay): "))
salary = float(input("Enter salary (for salary pay): "))

pay = calculate_pay(pay_type, hours, rate, salary)
print("Total pay:", pay)