# SYNTAX --
# import array
# obj = array.array(typecode[, initializer])


# An array is a collection of items stored at contiguous memory locations.
# Arrays have fixed size.

import array as arr
a = arr.array('i', [1, 2, 3])
print("The new football players is:", end='')
for i in range(0, 3):
    print(a[i], end="")
print()

b = arr.array('d', [1.3, 2.4, 3.5])
print("\n The new football players is:", end='')
for i in range(0, 3):
    print(b[i], end="")


a = arr.array('i', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# indexing
print(a[3])
# slicing
print(a[2:])
# Changing array
a[1] = 20
print(a[1])
# assignment
a[4] = '100'
# add new element
a.append(10)
print(a)
# insert new element
a.insert(1, 20)
print(a)
# extend from another array element
b = arr.array('i', [16, 17, 18, 19, 20])
a.extend(b)
print(a)
# removing an element
a.remove(7)
print(a)
# removes an element at the specified index from the array, and returns the removed element.
a.pop(9)
print(a)


#All the features of ARRAYS are included.