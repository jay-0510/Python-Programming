# DELETING THE FILE

# Using the OS module
# Module is file written by another programmer that generally has a function to use.

# import os
# os.remove()

# Practice question
with open("FileX.txt", "r") as f:
    f.write("Mumbai Indians\nChennai Super Kings")
    f.write("RCB\nRohit Sharma, MSD, Virat Kohli")

word = "MSD"
with open("FileX.txt", "r") as f:
    data = f.read()
    if (data.find(word) != -1):
        print("Found")
    else:
        print("Notfound")
