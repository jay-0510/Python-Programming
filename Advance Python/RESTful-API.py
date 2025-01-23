" Basics of RESTful API "

# REST - Representational State Transfer
# Its an architectural style for designing networked applications.
# It relies on a stateless, client-server communication protocol.

" Core Features of RESTful API "
# 1. Stateless - Stateless: No session information is stored on the server.
# 2. Resource-Based: Data is treated as resources and accessed via URLs (e.g., /users/1).
# 3. HTTP Methods: Use standard HTTP methods (GET, POST, etc.).
# 4. Representation: Resources are represented in formats like JSON or XML.
# 5. Scalability: REST APIs are scalable and lightweight.

" RESTful API Endpoints "
# An endpoint is a URL that represents an object or a collection of objects.
# means ---- Endpoints are the URLs where APIs expose resources

 # GET /users: Fetch all users
#  GET /users/1: Fetch a single user
#  POST /users: Create a new user
#  PUT /users/1: Update user with ID 1
#  DELETE /users/1: Delete user with ID 1
#  GET /products: Fetch all products

"REST API STATUS CODE "
# 200 - OK: The request was successful.
# 201: Resource created
# 400: Bad request (invalid input)
# 401: Unauthorized (requires authentication)
# 404: Resource not found
# 500: Server error