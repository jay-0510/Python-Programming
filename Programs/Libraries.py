# Pandas
import numpy as np # type: ignore
import pandas as pd # type: ignore

# Creating and initializing a nested list
age = [['Aman', 95.5, "Male"], ['Sunny', 65.7, "Female"],
       ['Monty', 85.1, "Male"], ['toni', 75.4, "Male"]]

# Creating a pandas dataframe
df = pd.DataFrame(age, columns=['Name', 'Marks', 'Gender'])

# Printing dataframe
df


# Numpy
# Creating a 3-D numpy array using np.array()
org_array = np.array([[23, 46, 85],
                      [43, 56, 99],
                      [11, 34, 55]])

# Printing the Numpy array
print(org_array)
