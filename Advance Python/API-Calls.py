" API - Application programming Interface "
# Allows two software systems to communicate with each other
# Python simplifies API calls with requests library - HTTP request and JSONhandling for parsing data
# API calls are used to get data from a server. 
# API calls are used to send data to a server.

" Using requests library "
# Its one of the most popular libraries in Python for sending HTTP requests.
# It is used to send all kinds of HTTP requests.
# It is used to send GET, POST, PUT, DELETE requests.

" GET Request - Retrieve data from the server."
" POST Request - Send data to the server." # to create new data
" PUT Request - Update data on the server."
" DELETE Request - Delete data from the server."
" HEAD Request - Get metadata from the server."

# Example of GET request:
import requests # type: ignore

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print(f"Status Code: {response.status_code}")  # 200 for success
print(f"Response Text: {response.text}")       # Raw response


# Sending parameters with GET request;
url = "https://jsonplaceholder.typicode.com/posts"
params = {'userId': 1}  # Query parameter
response = requests.get(url, params=params)

print(response.json())  # Parse JSON response


