# GENERATORS IN PYTHON ---
# Special types of functions that allow to create an itearble sequence of values.
# Return a generator objects, used to generate values one-by-one as you iterate over it.
# Powerful tool to work on large & Complex data sets.

# CREATING GENERATOR :
# Created using YIELD  STATEMENT in a function.
# YIELD  STATEMENT returns the value and suspends the execution of the  function.

def my_generator():
    for i in range(5):
        yield i


gen = my_generator()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
# The next() function is used to request the next value from the generator, and the generator resumes its execution until it encounters another yield statement or until it reaches the end of the function.


# USING GENERATOR: --
gen = my_generator()
for i in gen:
    print(i)

# Generators offer several benefits over other types of sequences, such as lists, tuples, and sets.
