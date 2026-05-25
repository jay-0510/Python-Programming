class User:

    def __init__(self, name):
        self.name = name


class Message:
    def __init__(self, sender, text):  # Accepts both sender AND text
        self.sender = sender
        self.text = text


class ChatRoom:
    # Store whole object instances instead of just text strings.
    def __init__(self):
        self.users = []  # List of User objects
        self.history = []  # List of Message objects

    # Join chat
    def join(self, user):
        # Track active users in the room
        if user not in self.users:
            self.users.append(user)
            print(f"--- {user.name} joined the chat ---")

    def leave(self, user):
        # Allow users to disconnect from the room
        if user in self.users:
            self.users.remove(user)
            print(f"--- {user.name} left the chat ---")

    # Send message
        # Only allow users currently inside the room to send messages
    def send_message(self, message):
        self.history.append(message.text)

    # Show chat history
        # Clean formatting instead of printing a raw list object.
    def show_history(self):
        print(self.history)


# 1. Create a chat room instance
room = ChatRoom()

# 2. Instantiate users
user1 = User("Jay")
user2 = User("Alice")

# 3. Users must join before talking
room.join(user1)
room.join(user2)

# 4. Create messages linking the sender to their text
msg1 = Message(user1, "Hello everyone!")
msg2 = Message(user2, "Hey Jay! Welcome.")

# 5. Broadcast and view the live conversation
room.send_message(msg1)
room.send_message(msg2)
room.show_history()

# 6. Test leaving the room
room.leave(user2)
