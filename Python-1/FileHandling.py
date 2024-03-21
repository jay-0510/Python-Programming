# TEXT FILES -- .txt, .doc, .log
# BINARY FILES -- .mp4, .mov, .png, .jpeg


# r = Reading
# w = Writing , truncating the file first
# a = Appending to the end of the file
# x = Creating and opening it for writing
# t = Text mode
# b = Binary mode

# r+ = open for reading & writing. STREAM is positioned at beginning of file. NO TRUNCATE
# w+ = open for reading & writing. The file is created if it doesn't exist otherwise its truncated. TRUNCATE
# a+ = open for reading & writing. STREAM is positioned at end of file. NO TRUNCATE

# f.read() -- read entirer file
# f.readline() -- read one line at a time

# open a file before reading or writing
f = open("Python-1/FileP.txt", "r")
data = f.read()
print(data)
print(type(data))
f.close()


f = open("Python-1/FileP.txt", "w")  # overwrites the entire the file
f.write("Kylian Mbappe  is the best player in the world.")

f = open("Python-1/FileP.txt", "a")  # adds to the file
f.write("Luka Modric is the best midfielder in football")


# with syntax
with open("", "a") as f:
    data = f.read()
