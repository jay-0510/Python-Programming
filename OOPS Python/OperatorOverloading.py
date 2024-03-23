# Operator Overloading ---

# Allows to redefine the behaviour of mathematical & Comparison  operators for user-defined data types.
# Allows to create more readable and intitutive code.
# Overload an operator in Python by defining special methods in your class. These methods are identified by their names, which start and end with double underscores (__).

class Vector:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def __str__(self):
        return f"{self.i}i + {self.j}j + {self.k}k"

    def __add__(self, x):
        return Vector(self.i + x.i,  self.j+x.j, self.k+x.k)


v1 = Vector(3, 5, 6)
print(v1)

v2 = Vector(1, 2, 9)
print(v2)

print(v1 + v2)
print(type(v1 + v2))


#  + : __add__
#  - : __sub__
#  * : __mul__
#  / : __truediv__
#  < : __lt__
#  > : __gt__
#  == : __eq__
