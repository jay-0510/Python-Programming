" REGULAR EXPRESSION - REGREX "
# It is powerful tools for pattern matching, seaching, replacing and manipulation string. 
# It is used to search for a specific pattern in a string.

" WHAT IS REGREX ? "
# A sequence of characters that defines a search pattern.
# Used for string matching, validation, substitution, etc


" Regular Expression Syntax "
# ^ - Start of the string
# $ - End of the string
# . - Any character except newline
# [...] - Any character in the set
# [^...] - Any character not in the set
# re* - Zero or more occurences of re
# re+ - One or more occurences of re
# re? - Zero or one occurence of re
# re{ n} - n occurences of re
# re{ n, } - n or more occurences of re
# d - Any digit [0-9]
# D - Any non-digit [^0-9]
# s - Any whitespace character
# S - Any non-whitespace character
# w - Any alphanumeric character
# W - Any non-alphanumeric character
# | - OR operator
# () - Grouping
# [] - Character class
# {} - Quantifier
# \ - Escape character

" SEARCHING, MATCHING AND FINDING "
# USING RE MODULE :
# re.match() - Match the pattern at the beginning of the string
# re.search() - Search the pattern in the string
# re.findall() - Find all the patterns in the string
# re.split() - Split the string based on the pattern
# re.sub() - Substitute the pattern in the string


" re.search() " # -- It is used to search for a pattern in a string.
import re

pattern = r"hello"
text = "hello world"
match = re.search(pattern, text)

if match:
    print("Match found:", match.group())  # Output: Match found: hello
else:
    print("No match")
    
    
    
" re.match() " # -- It is used to search for a pattern at the beginning of the string.
match = re.match(r"hello", "hello world")
if match:
    print("Matched:", match.group())  # Output: Matched: hello
    
    
    
" re.findall() " # -- It is used to find all the patterns in the string.
matches = re.findall(r"\d+", "Numbers: 123, 456, 789")
print(matches)  # Output: ['123', '456', '789']


" re.split() " # -- It is used to split the string based on the pattern.
result = re.split(r"\s+", "Split this string")
print(result)  # Output: ['Split', 'this', 'string']


" re.sub() " # -- It is used to substitute the pattern in the string.
result = re.sub(r"\d+", "###", "Call 123-456-789")
print(result)  # Output: Call ###-###-###