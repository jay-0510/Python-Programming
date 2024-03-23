# STATIC METHOD ---

# These are method that belong to a class rather than an instance of the class.
# Define using @static method decorator & don't have access to the instance of the class.
# They are called on the class itself, not on an instance of the class.
# Often used to create utility function that don't need access to instance data.

class Math:
    def __init__(self, num):
        self.num = num

    def addtonum(self, n):
        self.num = self.num + n

    @staticmethod
    def add(a, b):
        return a + b


# result = Math.add(1, 2)
# print(result) # Output: 3
a = Math(5)
print(a.num)
a.addtonum(6)
print(a.num)

print(Math.add(7, 2))
