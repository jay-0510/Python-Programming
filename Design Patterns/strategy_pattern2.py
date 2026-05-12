# Strategy Design Pattern -- You have a family of algorithms & encapsulate them in different classes & make them interchangable without knowing clients

# Each new method requires modifying existing code.
# Testing all the payment methods to ensure nothing breaks

class PaymentProcessor:
    def process_payment(self, method, amount):
        if method == "credit_card":
            print(f'Processing ${amount} payment using credit card.')
        elif method == "paypal":
            print(f'Processing ${amount} payment using PayPal.')
        elif method == "crypto":
            print(f'Processing ${amount} payment using cryptocurrency')
        else:
            print("Unsupported payment method")


# Usage
processor = PaymentProcessor()
processor.process_payment("credit_card", 100)
processor.process_payment("paypal", 150)
