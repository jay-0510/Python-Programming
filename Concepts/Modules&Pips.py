# Modules and PIPS in Python

#Built in Modules:
"These modules are ready to import and use and ships with the python interpreter. there is no need to install such modules explicitly."

#External Modules :
"These modules are imported from a third party file or can be installed using a package manager like pip or conda. Since this code is written by someone else, we can install different versions of a same module with time."

#The PIP Command :
"It can be used as a package manager pip to install a python module. Lets install a module called pandas using the following command."

#using a module in python: (syntax)
import pandas

# Read and work with a file named 'words.csv'
df = pandas.read_csv('words.csv')
print(df)  # This will display first few rows from the words.csv file

import pandas  # This is an example of external module
import hashlib  # This is an example of built in module

print("Hi")

# Dont worry about how to use these modules just yet!
pandas.read_csv("one.csv")
m = hashlib.sha256()
