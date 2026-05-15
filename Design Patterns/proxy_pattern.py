# ================================================================
#  PROXY PATTERN — Notification Service
#  All 4 Proxy Types in One File
#
#  Gujarati: "Vachhe man rakho?" — Direct nahi, proxy thi jao
#
#  Scenario:
#  NotificationService expensive che — DB connect kare,
#  external APIs call kare. Direct access thi problems:
#  → Koi pun access kari shake (no auth)
#  → Same message bar bar DB hit kare (no cache)
#  → Koi audit trail nathi (no logging)
#  → App start slow thay (eager initialization)
#
#  Solution: Real service same rakho — Proxy vachhe ma muko.
# ================================================================

import time
from datetime import datetime


# ----------------------------------------------------------------
#  STEP 1 — SUBJECT INTERFACE
#  Common contract — Proxy ane Real Service banne implement kare
#  Caller ne khabar nathi ke koni sathe vaat kare che
# ----------------------------------------------------------------

class NotificationService:
    def send(self, user_role: str, message: str):
        raise NotImplementedError


# ----------------------------------------------------------------
#  STEP 2 — REAL SUBJECT
#  Actual kaam kare. Koi extra logic nathi. Clean ane focused.
#  Start thava ma deliberately slow — virtual proxy demo mate
# ----------------------------------------------------------------

class RealNotificationService(NotificationService):

    def __init__(self):
        # Expensive initialization — DB connect, config load
        print("  [Real Service] Initializing... (DB connect, config load)")
        time.sleep(0.5)            # 0.5 sec delay — real world ma 2-3 sec
        print("  [Real Service] Ready.")

    def send(self, user_role: str, message: str):
        # Core responsibility — bas notification moklo
        print(f"  [Real Service] ✓ Notification sent → '{message}'")
        return f"delivered: {message}"


# ----------------------------------------------------------------
#  PROXY TYPE 1 — PROTECTION PROXY
#  Gujarati: "Kaun aavi shake?" — Access control
#
#  "bulk_alert" type notifications sirf ADMIN mokli shake.
#  Normal user try kare → proxy block kare.
#  Real service ne khabar j nathi padti.
# ----------------------------------------------------------------

class ProtectionProxy(NotificationService):

    # Kone shu moklavani permission che
    PERMISSIONS = {
        "admin": ["order_update", "bulk_alert", "system_alert"],
        # user sirf order update mokli shake
        "user":  ["order_update"],
        "guest": []                             # guest koi notification nahi mokli shake
    }

    def __init__(self, real_service: NotificationService):
        self._real = real_service               # real service andar rakho

    def send(self, user_role: str, message: str):
        # Pehla check — permission che?
        allowed = self.PERMISSIONS.get(user_role, [])

        # Message type check — first word = type
        msg_type = message.split(":")[0].lower().replace(" ", "_")

        # Check if any allowed type matches
        has_permission = any(perm in msg_type for perm in allowed)

        if not has_permission:
            print(f"  [Protection Proxy] ✗ BLOCKED — '{user_role}' "
                  f"cannot send this type")
            return "blocked"

        print(f"  [Protection Proxy] ✓ Access granted for '{user_role}'")
        return self._real.send(user_role, message)  # real ne forward karo


# ----------------------------------------------------------------
#  PROXY TYPE 2 — CACHING PROXY
#  Gujarati: "Aapyu hatu — yaad che?" — No repeat calls
#
#  Same message → cache thi serve, real service call nahi.
#  "Diwali Sale" notification 10,000 users ne joie —
#  sirf pehli vakhat DB hit karo, baaki cache thi serve karo.
# ----------------------------------------------------------------

class CachingProxy(NotificationService):

    def __init__(self, real_service: NotificationService):
        self._real = real_service
        self._cache = {}                        # message → result store

    def send(self, user_role: str, message: str):
        cache_key = f"{user_role}:{message}"    # unique key banavo

        if cache_key in self._cache:
            # Cache hit — real service call nahi
            print(f"  [Caching Proxy] ✓ Cache hit — real service skip")
            return self._cache[cache_key]

        # Cache miss — real service call karo, result store karo
        print(f"  [Caching Proxy] Cache miss — forwarding to real service")
        result = self._real.send(user_role, message)
        self._cache[cache_key] = result         # next time mate store
        return result

    def cache_size(self):
        return len(self._cache)


# ----------------------------------------------------------------
#  PROXY TYPE 3 — LOGGING PROXY
#  Gujarati: "Kone moklyu, kyare moklyu?" — Audit trail
#
#  Compliance requirement: har notification log thavi joie.
#  Real service ma logging mix nathi karvani —
#  Logging Proxy ek j kaam kare — log karo.
# ----------------------------------------------------------------

class LoggingProxy(NotificationService):

    def __init__(self, real_service: NotificationService):
        self._real = real_service
        self._logs = []                         # full audit trail

    def send(self, user_role: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Before — attempt log karo
        log_entry = f"{timestamp} | role={user_role} | msg='{message}'"
        self._logs.append(f"ATTEMPT  | {log_entry}")
        print(f"  [Logging Proxy] → {log_entry}")

        # Forward to real service
        result = self._real.send(user_role, message)

        # After — result log karo
        self._logs.append(f"RESULT   | {timestamp} | {result}")
        print(f"  [Logging Proxy] ✓ Logged result: {result}")

        return result

    def print_audit_log(self):
        print("\n  ── Audit Log ──")
        for entry in self._logs:
            print(f"  {entry}")


# ----------------------------------------------------------------
#  PROXY TYPE 4 — VIRTUAL PROXY (Lazy Initialization)
#  Gujarati: "Jarur padse toh banavo" — Delay expensive creation
#
#  Real service start thava ma 0.5 sec lagay.
#  App start thay tyare create nahi karvi —
#  Pehli genuine call aave tyare j banavo.
# ----------------------------------------------------------------

class VirtualProxy(NotificationService):

    def __init__(self):
        self._real = None           # null — abhi nahi banayo — no delay

    def send(self, user_role: str, message: str):
        if self._real is None:
            # First call — tabhi real service banavo (lazy init)
            print("  [Virtual Proxy] First call — creating real service now...")
            self._real = RealNotificationService()   # expensive — sirf ek j vakhat

        # real_service ready — forward karo
        return self._real.send(user_role, message)


# ================================================================
#  DEMO — All 4 Proxy Types
# ================================================================

print("=" * 55)
print("  PROXY PATTERN — All 4 Types")
print("  Gujarati: 'Vachhe man rakho?'")
print("=" * 55)


# ── TYPE 1: PROTECTION PROXY ────────────────────────────────────
print("\n── PROTECTION PROXY — 'Kaun aavi shake?' ──")

real = RealNotificationService()
guarded = ProtectionProxy(real)

guarded.send("admin", "bulk_alert: System maintenance at 2AM")  # → allowed
print()
guarded.send("user",  "order_update: Your order shipped!")       # → allowed
print()
guarded.send("user",  "bulk_alert: Free coins for everyone!")    # → blocked
print()
guarded.send("guest", "order_update: Something")                 # → blocked


# ── TYPE 2: CACHING PROXY ───────────────────────────────────────
print("\n\n── CACHING PROXY — 'Aapyu hatu — yaad che?' ──")

real = RealNotificationService()
cached = CachingProxy(real)

print("\n  First call — real service hit thay:")
cached.send("user", "Diwali Sale is LIVE! 50% off")

print("\n  Same message again — cache thi serve:")
cached.send("user", "Diwali Sale is LIVE! 50% off")

print("\n  Same message third time — still cache:")
cached.send("user", "Diwali Sale is LIVE! 50% off")

print(f"\n  Cache size: {cached.cache_size()} entry")
print("  Real service sirf ek j vakhat call thayo — cache handled rest")


# ── TYPE 3: LOGGING PROXY ───────────────────────────────────────
print("\n\n── LOGGING PROXY — 'Kone moklyu, kyare moklyu?' ──")

real = RealNotificationService()
logged = LoggingProxy(real)

print()
logged.send("admin", "Server going down at 3AM")
print()
logged.send("user",  "Your order has been delivered!")

logged.print_audit_log()


# ── TYPE 4: VIRTUAL PROXY ───────────────────────────────────────
print("\n\n── VIRTUAL PROXY — 'Jarur padse toh banavo' ──")

print("\n  VirtualProxy create thayo — real service nathi banyo abhi:")
proxy = VirtualProxy()              # instant — no delay, no real service yet
print("  App ready instantly. Real service not initialized yet.")

print("\n  Pehli notification aavi — tabhi j real service bane:")
proxy.send("user", "Flash Sale starts NOW!")

print("\n  Second call — real service already ready:")
proxy.send("user", "Only 2 hours left!")


# ── COMBINED PROXY CHAIN ─────────────────────────────────────────
print("\n\n── COMBINED CHAIN — Real production jevo ──")
print("  Caller → Logging → Protection → Caching → Real Service")
print()

real = RealNotificationService()
cached = CachingProxy(real)           # innermost — cache layer
guarded = ProtectionProxy(cached)      # auth on top of cache
logged = LoggingProxy(guarded)        # log everything

# Admin → logs → auth check → cache check → real service
print("  Admin sending system alert:")
logged.send("admin", "bulk_alert: New feature deployed!")

print()

# Same message again → logs → auth → CACHE HIT — real skipped
print("  Admin sending same alert again:")
logged.send("admin", "bulk_alert: New feature deployed!")

print()

# User trying bulk_alert → logs → auth BLOCKS — cache/real never hit
print("  User trying bulk_alert — should be blocked:")
logged.send("user", "bulk_alert: Unauthorized message")


# ================================================================
#  PROOF — Caller ne khabar nathi proxy sathe vaat kare che
# ================================================================

print("\n\n" + "=" * 55)
print("  PROOF — Same Interface, Transparent to Caller")
print("=" * 55)


def notify_user(service: NotificationService, role: str, msg: str):
    # Aa function ne khabar nathi ke real che ke proxy — same interface
    service.send(role, msg)


real_svc = RealNotificationService()
proxy_svc = CachingProxy(real_svc)

print("\n  Calling with Real Service:")
notify_user(real_svc,  "user", "Test message")

print("\n  Calling with Caching Proxy (same function, no change):")
notify_user(proxy_svc, "user", "Test message")
notify_user(proxy_svc, "user", "Test message")   # cache hit


# ================================================================
#  WITH vs WITHOUT — Final Comparison
# ================================================================

print("\n" + "=" * 55)
print("  WITHOUT PROXY — Messy Real Service")
print("=" * 55)
print("""
  class MessyNotificationService:
      def send(self, role, message):
          # Logging — not my job
          log(f"Sending: {message}")
          # Auth — not my job  
          if role != "admin": return "denied"
          # Cache — not my job
          if message in cache: return cache[message]
          # Finally — actual work
          print("Sending notification...")
          
  Problem: 4 responsibilities in 1 class
  Change logging format → touch this class
  Change auth logic → touch this class  
  Add caching → touch this class
  Every change risks breaking notifications
""")

print("  WITH PROXY — Each class does ONE thing")
print("-" * 55)
print("""
  RealNotificationService  → sirf send karo
  ProtectionProxy          → sirf auth karo
  CachingProxy             → sirf cache karo
  LoggingProxy             → sirf log karo
  
  Change logging → sirf LoggingProxy badle
  Change auth    → sirf ProtectionProxy badle
  Real service untouched — EVER
""")
