# SHUTIL is short for shell utility
# provides high level interface for working with file and directories.


# SYNTAX ---------
# import shutil

# SHUTIL provides simple and efficient way to perform common file & directory related tasks in python. Whether you need to copy, move, delete, or preserve metadata about files and directories, the shutil module has you covered.
# SHUTIL module is powerful tool for automating file & directory-related tasks in python.


# shutil.copy(src, dst) ->  Copy the src path to the destination path specified by dst. If dst already exists, it will be overwritten.
# shutil.copy2(src, dst) -> Similar to shutil.copy, but also preserves metadata about the original file, such as timestamp.
# shutil.move(src, dst) -> Moves the file located at src  to the destination path specified by dst.This is equivalent to renaming file.
# shutil.rmtree(path) -> Recursively deletes the directory located at path, along with all of its contents.
# shutil.copytree(src, dst)  -> Copies an entire directory tree rooted at src to a new location specified by dst.

# import shutil

# Copying a file
# shutil.copy("src.txt", "dst.txt")

# Copying a directory
# shutil.copytree("src_dir", "dst_dir")

# Moving a file
# shutil.move("src.txt", "dst.txt")

# Deleting a directory
# shutil.rmtree("dir")

#ADVANCED IMP CONCEPT!!!