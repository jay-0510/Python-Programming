#DICTIONARIES :
'Dictionaries are ordered collection of data items. They store multiple items in a single variable.'
'Dictionary items are key-value pairs that are separated by commas and enclosed within curly brackets {}.'


#Accessing single value items:
info = {'name':'Dhruv', 'age':19, 'eligible':True}
print(info['name'])
print(info.get('eligible'))


#Accessing multiple items:
info = {'name':'Pratham', 'age':19, 'eligible':True}
print(info.values())


#Accessing keys :
info = {'name':'Diya', 'age':19, 'eligible':True}
print(info.keys())


#Accessing Key Value pairs:
info = {'name':'Dhruvil', 'age':19, 'eligible':True}
print(info.items())