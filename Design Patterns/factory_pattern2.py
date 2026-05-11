from abc import ABC, abstractmethod

# common interface for all notifications


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass     # just defines the interface, no implementation


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f'Sending Email with message: {message}')


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f'Sending SMS with message: {message}')


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f'Sending PUSH with message: {message}')


class NotificationFactory:
    # factor method creates object based on type string
    def create_notification(self, channel: str) -> Notification:
        channel = channel.lower()  # Normalise Input
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "push":
            return PushNotification()
        else:
            raise ValueError(f'Unknown Notification Channel: {channel}')


# usage
factory = NotificationFactory()

notify1 = factory.create_notification('email')  # creates Email notification
notify2 = factory.create_notification('sms')   # creates sms notification

notify1.send("Hello Bhai via Email!!")
notify2.send("Hola via SMS!!")

# Notification is the abstract base class that defines the send
# 3 sub classes --- implement send differently
# NotificationFactory.create_notification(channel) --- Factory Method
# Callers only says "email"/"sms"/"push" & gets the right object without knowing class names.
