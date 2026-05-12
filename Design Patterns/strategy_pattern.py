# Strategy Design Pattern -- You have a family of algorithms & encapsulate them in different classes & make them interchangable without knowing clients

from abc import ABC, abstractmethod

# Defining an interface for payment strategies


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Implementing the specific payment strategies
# Each payment method is encapsulated in its own class.


class CreditCard(PaymentStrategy):
    def pay(self, amount):
        print(f'Processing ${amount} payment using Credit card')


class PaypalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f'Processing ${amount} payment using PayPal')


class CryptoPayment(PaymentStrategy):
    def pay(self, amount):
        print(f'Processing ${amount} payment using Cryptocurrency')

# Context Class to use the strategies


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    # If wnat to change payment strategy then its been used.
    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    # Simply calls pay method of the given strategy.
    def process_payment(self, amount):
        self.strategy.pay(amount)


# usage :
processor = PaymentProcessor(CreditCard())
processor.process_payment(100)

processor.set_strategy(PaypalPayment())
processor.process_payment(200)

processor.set_strategy(CryptoPayment())
processor.process_payment(300)


# Real Applications
# Payment Gateway, Sorting Algorithm (Bubble, Merge-- Data size), Compression Tools (Zip, RAR, GZIP), Authentication system

# Pros
# Extensibility -- Add new methods without modifying existing code
# Flexibility -- Can switch to different payment methods dynamically at runtime
# Clean Code -- logic divided into smaller & manageable pieces.

# Cons
# Overhead of managing extra classes
# Setup complexibility
