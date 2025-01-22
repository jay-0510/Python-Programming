#There are four types of arguments that we can provide in a function:
'''Default Arguments
Keyword Arguments
Variable length Arguments
Required Arguments'''

#DEFAULT ARGUMENTS:
"We can provide a default value while creating a function. This way the function assumes a default value even if a value is not provided in the function call for that argument."

#KEYWORD ARGUMENTS:
"We can provide arguments with key = value, this way the interpreter recognizes the arguments by the parameter name. Hence, the the order in which the arguments are passed does not matter."

#REQUIRED ARGUMENTS:
"In case we don’t pass the arguments with a key = value syntax, then it is necessary to pass the arguments in the correct positional order and the number of arguments passed should match with actual function definition."

#RETURN STATEMENT :
"The return statement is used to return the value of the expression back to the calling function."
def name(fname, mname, lname):
    return "Hello, " + fname + " " + mname + " " + lname

print(name("Lionel", "Andres", "Messi"))



# WAF to convert usd to INR 
def converter(usd_val):
    inr_val = usd_val * 83
    print(usd_val, "USD=", inr_val, "INR")
    
    converter(100)