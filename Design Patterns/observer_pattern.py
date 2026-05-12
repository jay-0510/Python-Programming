from typing import List

# Observer Pattern -- One object changes state & multiple other need to be notified & update automatically; without tight coupling.
# Analogy : Youtube Channel & Subscribers -- You post a video, all subscribers are notified. Subscribers can join or leave at any time.The channel doesn't know wh exactly is watching


class Subject:
    def remove_observer(self, observer):
        raise NotImplementedError(
            "THis method should be overwritten by subclasses")

    def notify_observer(self, observer):
        raise NotImplementedError(
            "This method should be overwritten by subclasses!")


class Stock(Subject):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.observers: List = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.update(self)

    def set_price(self, new_price):
        self.new_price = new_price
        self.notify_observer()


class Observer:
    def update(self, stock):
        raise NotImplementedError(
            " This method should be overwritten by subclasses")


class Dashboard(Observer):
    def update(self, stock):
        print(f'Dashboard updated: {stock.name} is now ${stock.price}')


class EmailAlert(Observer):
    def update(self, stock):
        print(f'Email Alert: {stock.name} price updated to ${stock.price}')


class SMSAlert(Observer):
    def update(self, stock):
        print(f'SMS Alert: {stock.name} price updated to ${stock.price}')


# Usage
apple_stock = Stock("AAPL", 150)
tesla_stock = Stock("TESU", 400)

# Observer
dashboard = Dashboard()
email_alert = EmailAlert()
sms_alert = SMSAlert()

apple_stock.add_observer(dashboard)
apple_stock.add_observer(email_alert)
apple_stock.add_observer(sms_alert)

tesla_stock.add_observer(dashboard)
tesla_stock.add_observer(email_alert)

# Don't need to call manually update mehtof For Stock price. When its changes it updates automatically

apple_stock.set_price(200)
tesla_stock.set_price(300)
