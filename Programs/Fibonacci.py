# FIBONACCI SERIES
def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        if i == 0:
            print(a, end=" ")
        elif i == 1:
            print(b, end=" ")
        else:
            c = a + b
            a = b
            b = c
            print(b, end=" ")


fibonacci(10)
