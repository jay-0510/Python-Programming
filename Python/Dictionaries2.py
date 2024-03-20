# Dictionary Methods:
"Dictionary uses several built-in methods for manipulation.They are listed below"

# update():
'The update() method updates the value of the key provided to it if the item already exists in the dictionary, else it creates a new key-value pair.'
info = {'name': 'Mbappe', 'age': 19, 'eligible': True}
print(info)
info.update({'age': 20})
info.update({'DOB': 2001})
print(info)


# Clear():
'The clear() method removes all the items from the list.'


# pop():
'The pop() method removes the key-value pair whose key is passed as a parameter.'


# popitem():
'The popitem() method removes the last key-value pair from the dictionary.'
info = {'name': 'Mbappe', 'age': 19, 'eligible': True, 'DOB': 2003}
info.popitem()
print(info)


# del:
'use the del keyword to remove a dictionary item.'
'If key is not provided, then the del keyword will delete the dictionary entirely.'
info = {'name': 'Mbappe', 'age': 19, 'eligible': True, 'DOB': 2003}
del info
print(info)
