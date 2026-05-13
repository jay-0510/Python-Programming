# ==============================================================
#  NOTIFICATION SYSTEM — All 8 Patterns in One Example
#
#  Scenario:
#  User place kare order → system decide kare ke notification
#  kevi rite moklave — Email, SMS, ya Push.
#  Android/iOS alag, Gmail hoy ke na hoy alag, UI alag.
#
#  Gujarati one-liner har pattern pehla — yaad rakhva mate.
# ==============================================================


# ══════════════════════════════════════════════════════════════
#  PATTERN 1 — FACTORY METHOD
#  "Shu banavu" — Kai type ni notification banavi?
#
#  Tame bas kaho "email" ya "sms" — factory banavi de.
#  Tame new EmailNotification() directly nahi karo.
# ══════════════════════════════════════════════════════════════

class Notification:
    def send(self, message: str):
        raise NotImplementedError


class EmailNotification(Notification):
    def send(self, message: str):
        print(f"  [EMAIL]  Sending: {message}")


class SMSNotification(Notification):
    def send(self, message: str):
        print(f"  [SMS]    Sending: {message}")


class PushNotification(Notification):
    def send(self, message: str):
        print(f"  [PUSH]   Sending: {message}")


# Factory — ek jagya decide kare shu banavu
class NotificationFactory:
    @staticmethod
    def create(type: str) -> Notification:
        if type == "email":
            return EmailNotification()
        if type == "sms":
            return SMSNotification()
        if type == "push":
            return PushNotification()
        raise ValueError(f"Unknown: {type}")


print("=" * 55)
print(" PATTERN 1 — FACTORY METHOD")
print(" 'Shu banavu' — Factory decide kare")
print("=" * 55)
n = NotificationFactory.create("email")
n.send("Tamaro order place thayo!")
n = NotificationFactory.create("sms")
n.send("OTP: 839201")


# ══════════════════════════════════════════════════════════════
#  PATTERN 2 — ABSTRACT FACTORY
#  "Family sathe banavu" — Android ya iOS?
#
#  Android ma notification alag dikhay, iOS ma alag.
#  Sirf notification nahi — UI style pan match thavu joie.
#  Android factory → Android notification + Android UI style.
#  iOS factory     → iOS notification + iOS UI style.
# ══════════════════════════════════════════════════════════════

# Product 1 — Notification look
class AndroidNotificationUI:
    def show(self): print("  [Android UI] Material Design card — top drawer")


class IOSNotificationUI:
    def show(self): print("  [iOS UI]     Banner style — top, auto dismiss")

# Product 2 — Sound/vibration style


class AndroidAlertStyle:
    def alert(self): print("  [Android]    Custom vibration pattern + LED")


class IOSAlertStyle:
    def alert(self): print("  [iOS]        Haptic feedback + default chime")

# Abstract Factory


class OSNotificationFactory:
    def create_ui(self): raise NotImplementedError
    def create_alert(self): raise NotImplementedError


class AndroidFactory(OSNotificationFactory):
    def create_ui(self): return AndroidNotificationUI()
    def create_alert(self): return AndroidAlertStyle()


class IOSFactory(OSNotificationFactory):
    def create_ui(self): return IOSNotificationUI()
    def create_alert(self): return IOSAlertStyle()


def deliver_notification(factory: OSNotificationFactory, message: str):
    ui = factory.create_ui()
    alert = factory.create_alert()
    print(f"  Message: {message}")
    ui.show()
    alert.alert()


print("\n" + "=" * 55)
print(" PATTERN 2 — ABSTRACT FACTORY")
print(" 'Family sathe banavu' — Android/iOS family match thay")
print("=" * 55)
deliver_notification(AndroidFactory(), "New message from Rahul")
print()
deliver_notification(IOSFactory(), "New message from Rahul")


# ══════════════════════════════════════════════════════════════
#  PATTERN 3 — BUILDER
#  "Step by step banavu" — Notification piece by piece banavo
#
#  Har notification ma badhu optional nathi hotu.
#  Koi ne title joie, koi ne image joie, koi ne link joie.
#  Builder thi tame sirf jo joie te set karo.
# ══════════════════════════════════════════════════════════════

class NotificationMessage:
    def __init__(self):
        self.title = None
        self.body = None
        self.image = None    # optional
        self.action = None    # optional — button in notification

    def __str__(self):
        return (
            f"\n  Title  : {self.title}"
            f"\n  Body   : {self.body}"
            f"\n  Image  : {self.image or 'None'}"
            f"\n  Action : {self.action or 'None'}"
        )


class NotificationBuilder:
    def __init__(self):
        self.notif = NotificationMessage()

    def set_title(self, title):
        self.notif.title = title
        return self                   # return self → chaining

    def set_body(self, body):
        self.notif.body = body
        return self

    def set_image(self, url):
        self.notif.image = url        # optional — call only when needed
        return self

    def set_action(self, label):
        self.notif.action = label     # optional — call only when needed
        return self

    def build(self):
        return self.notif


print("\n" + "=" * 55)
print(" PATTERN 3 — BUILDER")
print(" 'Step by step banavu' — piece by piece choose karo")
print("=" * 55)

# Simple SMS — sirf title + body
sms_notif = (
    NotificationBuilder()
    .set_title("OTP")
    .set_body("Tamaro OTP: 482910")
    .build()
)
print(sms_notif)

# Rich Push — badhu set karyu
push_notif = (
    NotificationBuilder()
    .set_title("Order Placed!")
    .set_body("Tamaro order 30 min ma aavse.")
    .set_image("https://img/order.png")
    .set_action("Track Order")
    .build()
)
print(push_notif)


# ══════════════════════════════════════════════════════════════
#  PATTERN 4 — ADAPTER
#  "Fit karvu" — Juna SMS API ne nava system sathe joडo
#
#  Scenario:
#  Company ni paas ek juno SMSService che — OldSMSAPI.
#  Nava system ma badha Notification.send(message) use kare.
#  OldSMSAPI ma method che: send_text(phone, text)
#  — alag signature, fit nathi thatu.
#  Adapter vachhe ma muko — koi change nahi.
# ══════════════════════════════════════════════════════════════

# Juno API — change nahi kari shakta (3rd party hoy toh)
class OldSMSAPI:
    def send_text(self, phone: str, text: str):
        print(f"  [OLD SMS API] → {phone}: {text}")

# Adapter — juna API ne nava interface ma fit kare


class SMSAdapter(Notification):
    def __init__(self, phone: str):
        self.phone = phone
        self.old_api = OldSMSAPI()   # juna API ne andar rakho

    def send(self, message: str):
        # nava interface (send) → juna API (send_text) ne call kare
        self.old_api.send_text(self.phone, message)


print("\n" + "=" * 55)
print(" PATTERN 4 — ADAPTER")
print(" 'Fit karvu' — Juna API ne nava system sathe joडo")
print("=" * 55)
adapted_sms = SMSAdapter("+91-9876543210")
adapted_sms.send("Tamaro order confirm thayo!")   # nava interface, juna kaam


# ══════════════════════════════════════════════════════════════
#  PATTERN 5 — STRATEGY
#  "Kai rite karvu" — Notification moklava ni rit
#
#  Scenario:
#  User Gmail valore hoy toh → Email moklo
#  Na hoy toh → SMS moklo
#  App install hoy toh → Push moklo
#  Sending ni algorithm alag — result same (notification pohoche)
# ══════════════════════════════════════════════════════════════

# Strategy interface
class SendStrategy:
    def send(self, message: str):
        raise NotImplementedError

# Concrete strategies — alag alag tarika


class SendViaEmail(SendStrategy):
    def send(self, message: str):
        print(f"  [STRATEGY: Email] → {message}")


class SendViaSMS(SendStrategy):
    def send(self, message: str):
        print(f"  [STRATEGY: SMS]   → {message}")


class SendViaPush(SendStrategy):
    def send(self, message: str):
        print(f"  [STRATEGY: Push]  → {message}")

# Context — strategy badlo, baaki same rahe


class NotificationSender:
    def __init__(self, strategy: SendStrategy):
        self.strategy = strategy

    def change_strategy(self, strategy: SendStrategy):
        self.strategy = strategy       # runtime ma switch karo

    def notify(self, message: str):
        self.strategy.send(message)


print("\n" + "=" * 55)
print(" PATTERN 5 — STRATEGY")
print(" 'Kai rite karvu' — Tarika runtime ma badlo")
print("=" * 55)

sender = NotificationSender(SendViaEmail())
sender.notify("Order placed!")           # Gmail varo user

sender.change_strategy(SendViaSMS())     # Gmail nathi → SMS
sender.notify("Order placed!")

sender.change_strategy(SendViaPush())    # App install che → Push
sender.notify("Order placed!")


# ══════════════════════════════════════════════════════════════
#  PATTERN 6 — OBSERVER
#  "Badha ne khaber" — Event thay etle badha ne notify karo
#
#  Scenario:
#  User order place kare → event fire thay
#  EmailService, SMSService, PushService — badha "subscribe" che
#  Event thay etle automatically badha ne notification jaay
#  OrderSystem ne khabar nathi katle subscriber che
# ══════════════════════════════════════════════════════════════

class NotificationObserver:
    def update(self, event: str, data: str):
        raise NotImplementedError


class EmailObserver(NotificationObserver):
    def update(self, event, data):
        print(f"  [EMAIL OBSERVER]  Event='{event}' | Sending: {data}")


class SMSObserver(NotificationObserver):
    def update(self, event, data):
        print(f"  [SMS OBSERVER]    Event='{event}' | Sending: {data}")


class PushObserver(NotificationObserver):
    def update(self, event, data):
        print(f"  [PUSH OBSERVER]   Event='{event}' | Sending: {data}")

# Subject — event fire kare, observers ne notify kare


class OrderSystem:
    def __init__(self):
        self._observers = []          # subscriber list

    def subscribe(self, obs: NotificationObserver):
        self._observers.append(obs)   # add subscriber

    def unsubscribe(self, obs: NotificationObserver):
        self._observers.remove(obs)   # remove subscriber

    def place_order(self, item: str):
        print(f"  Order placed for: {item}")
        self._notify("ORDER_PLACED", f"Tamaro '{item}' order confirm thayo!")

    def _notify(self, event, data):
        for obs in self._observers:   # badha ne khaber paado
            obs.update(event, data)


print("\n" + "=" * 55)
print(" PATTERN 6 — OBSERVER")
print(" 'Badha ne khaber' — Subscribe karo, automatic milse")
print("=" * 55)

order_system = OrderSystem()
order_system.subscribe(EmailObserver())
order_system.subscribe(SMSObserver())
order_system.subscribe(PushObserver())
order_system.place_order("iPhone 16")


# ══════════════════════════════════════════════════════════════
#  PATTERN 7 — STATE
#  "Hu kyaa chu" — User ni state upar depend kare shu thay
#
#  Scenario:
#  User Gmail varo → Email moklo
#  Gmail nathi pan app che → Push moklo
#  Koi nathi → SMS moklo
#  Same action (notify), pan STATE badlay etle behaviour badle
# ══════════════════════════════════════════════════════════════

class UserState:
    def notify(self, context, message: str):
        raise NotImplementedError


class HasGmailState(UserState):
    def notify(self, context, message: str):
        print(f"  [STATE: Gmail]  Email mokyo → {message}")
        # state badli shake — jemke 5 min baad app check kare


class HasAppState(UserState):
    def notify(self, context, message: str):
        print(f"  [STATE: App]    Push mokyo → {message}")


class NoChannelState(UserState):
    def notify(self, context, message: str):
        print(f"  [STATE: SMS]    SMS mokyo → {message}")

# Context — state hold kare


class UserNotifier:
    def __init__(self, state: UserState):
        self.state = state

    def change_state(self, state: UserState):
        self.state = state             # state runtime ma badle

    def notify(self, message: str):
        self.state.notify(self, message)  # current state handle kare


print("\n" + "=" * 55)
print(" PATTERN 7 — STATE")
print(" 'Hu kyaa chu' — State badlay etle behaviour badle")
print("=" * 55)

user = UserNotifier(HasGmailState())
user.notify("Order confirm thayo!")

user.change_state(HasAppState())       # Gmail logout thayo
user.notify("Order confirm thayo!")

user.change_state(NoChannelState())    # App pan nathi
user.notify("Order confirm thayo!")


# ══════════════════════════════════════════════════════════════
#  PATTERN 8 — BRIDGE
#  "Alag vadhvu" — Notification type ane platform alag rakho
#
#  Without Bridge:
#  AndroidEmail, AndroidSMS, AndroidPush,
#  iOSEmail, iOSSMS, iOSPush — 6 classes, badhe vadhse
#
#  With Bridge:
#  Notification (Email/SMS/Push) — ek side vadhay
#  Platform (Android/iOS)        — biji side vadhay
#  Banne connected pan independent
#
#  NOTE: This is the most "structural" pattern here.
#  Real projects ma notification system ma Bridge ochhu aave,
#  pan concept samjava mate perfect fit che.
# ══════════════════════════════════════════════════════════════

# Implementation side — Platform
class Platform:
    def deliver(self, message: str):
        raise NotImplementedError


class AndroidPlatform(Platform):
    def deliver(self, message: str):
        print(f"  [Android Platform] Material UI → {message}")


class IOSPlatform(Platform):
    def deliver(self, message: str):
        print(f"  [iOS Platform]     Banner UI   → {message}")

# Abstraction side — Notification type


class BridgeNotification:
    def __init__(self, platform: Platform):
        self.platform = platform      # bridge — platform inject karo

    def send(self, message: str):
        raise NotImplementedError


class BridgeEmail(BridgeNotification):
    def send(self, message: str):
        print("  [Email]", end=" ")
        self.platform.deliver(message)


class BridgeSMS(BridgeNotification):
    def send(self, message: str):
        print("  [SMS]  ", end=" ")
        self.platform.deliver(message)


class BridgePush(BridgeNotification):
    def send(self, message: str):
        print("  [Push] ", end=" ")
        self.platform.deliver(message)


print("\n" + "=" * 55)
print(" PATTERN 8 — BRIDGE")
print(" 'Alag vadhvu' — Type ane Platform independently vadhay")
print("=" * 55)

# Android par Email
BridgeEmail(AndroidPlatform()).send("Order confirm thayo!")
# iOS par Email
BridgeEmail(IOSPlatform()).send("Order confirm thayo!")
# iOS par Push
BridgePush(IOSPlatform()).send("Delivery nikli!")

# Navu platform aavyu? → Bas navi Platform class banavo
# Navo notification type? → Bas navi BridgeNotification class banavo
# Banne ne alag alag vadharo — ek change karo to biju nahi tuttu
