class ControlTower():
    _instance = None   # Class variable to store the single shared instance

    def __new__(cls):
        # Check if an instance already exists; if not, create it
        if cls._instance is None:
            # Call the parent class to allocate memory for the new object
            cls._instance = super().__new__(cls)
            print("Initialise Control Tower")
        # Return the existing or newly created single instance
        return cls._instance

    def manage_flight(self, flight):
        # A simple method to demonstrate the tower's functionality
        print(f"Managing Flight {flight}")


# Create the first instance (triggers "Initialise Control Tower")
tower1 = ControlTower()
# Returns the existing instance (no initialisation message)
tower2 = ControlTower()
# Returns the same existing instance again
tower3 = ControlTower()

# Use the instance to manage different flights
tower1.manage_flight("QATAR-452")
tower2.manage_flight("Emirates-007")
tower3.manage_flight("Ethiad-123")

# Check if tower1 and tower2 point to the same memory address (True)
print(tower1 is tower2)
# Check if tower1 and tower3 point to the same memory address (True)
print(tower1 is tower3)
