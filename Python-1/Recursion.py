#PYTHON RECURSION FUNCTION:
'In Python, we know that a function can call other functions. It is even possible for the function to call itself. These types of construct are termed as recursive functions.'

#recursive function
def show(n):
  if  (n == 0) : #base case decide recursion should be stop or not
    return
  print(n)
  show(n-1)
  
  show(10)
  

