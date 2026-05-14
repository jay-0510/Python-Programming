# ================================================================
#  MEMENTO PATTERN — Notification Settings with Undo History
#
#  Gujarati: "Pachhu jaavu hoy toh?" — Jeva hata teva karo
#
#  Scenario:
#  User potana notification settings configure kare —
#  Email, SMS, Push, DND, Frequency.
#  Ghabravani jarur nathi — koi pun change undo thay.
#  Ctrl+Z jevo — pachhi jeva hata teva.
# ================================================================


# ----------------------------------------------------------------
#  STEP 1 — MEMENTO (The Snapshot — opaque box)
#  Sirf state hold kare. Bahar koi read nahi kari shake.
#  Only NotificationSettings (Originator) reads it.
# ----------------------------------------------------------------

class NotificationMemento:

    def __init__(self, email_on, sms_on, push_on, dnd_mode, frequency):
        # __ prefix = name mangling = practically private in Python
        self.__email_on  = email_on    # state copy karke andar lock
        self.__sms_on    = sms_on
        self.__push_on   = push_on
        self.__dnd_mode  = dnd_mode
        self.__frequency = frequency

    # No public getters — bahar koi individual field read nahi kari shake
    # Only Originator gets the full state back via get_state()

    def get_state(self):
        # Returns full state as tuple — only Originator calls this
        return (
            self.__email_on,
            self.__sms_on,
            self.__push_on,
            self.__dnd_mode,
            self.__frequency
        )


# ----------------------------------------------------------------
#  STEP 2 — ORIGINATOR (Notification Settings)
#  Real object. Apni state save kare, ane restore pan kare.
#  Aa j jaane apni andar shu che.
# ----------------------------------------------------------------

class NotificationSettings:

    def __init__(self):
        # Default state — everything on, no DND, instant alerts
        self.email_on  = True
        self.sms_on    = True
        self.push_on   = True
        self.dnd_mode  = False
        self.frequency = "instant"

    # --- State change methods ---

    def toggle_email(self):
        self.email_on = not self.email_on   # on hoy toh off, off hoy toh on

    def toggle_sms(self):
        self.sms_on = not self.sms_on

    def toggle_push(self):
        self.push_on = not self.push_on

    def enable_dnd(self):
        self.dnd_mode = True                # Do Not Disturb on

    def disable_dnd(self):
        self.dnd_mode = False

    def set_frequency(self, freq: str):
        self.frequency = freq               # "instant", "hourly", "daily"

    # --- Memento methods ---

    def save(self) -> NotificationMemento:
        # Object khud j apni state pack kare — no one else involved
        return NotificationMemento(
            self.email_on,
            self.sms_on,
            self.push_on,
            self.dnd_mode,
            self.frequency
        )

    def restore(self, memento: NotificationMemento):
        # Snapshot thi state pachi lavo — only this class reads it
        (
            self.email_on,
            self.sms_on,
            self.push_on,
            self.dnd_mode,
            self.frequency
        ) = memento.get_state()

    def show(self, label=""):
        tag = f" [{label}]" if label else ""
        print(f"\n  ── Settings{tag} ──")
        print(f"  Email : {'ON ' if self.email_on  else 'OFF'}")
        print(f"  SMS   : {'ON ' if self.sms_on    else 'OFF'}")
        print(f"  Push  : {'ON ' if self.push_on   else 'OFF'}")
        print(f"  DND   : {'ON ' if self.dnd_mode  else 'OFF'}")
        print(f"  Freq  : {self.frequency}")


# ----------------------------------------------------------------
#  STEP 3 — CARETAKER (History Manager)
#  Mementos ni list rakhe. Undo handle kare.
#  Andar shu che te NATHI jaanta — sirf hold kare.
# ----------------------------------------------------------------

class NotificationHistory:

    def __init__(self):
        self._stack = []            # mementos ni stack — last in, first out

    def push(self, memento: NotificationMemento):
        self._stack.append(memento) # checkpoint save karo

    def pop(self) -> NotificationMemento:
        if not self._stack:
            print("  [History] Koi history nathi — undo possible nathi")
            return None
        return self._stack.pop()    # last saved state kado

    def count(self):
        return len(self._stack)


# ================================================================
#  USAGE — Real scenario step by step
# ================================================================

print("=" * 50)
print("  MEMENTO PATTERN — Notification Settings Undo")
print("  Gujarati: 'Pachhu jaavu hoy toh?'")
print("=" * 50)

# Setup
settings = NotificationSettings()
history  = NotificationHistory()

# --- Initial state ---
settings.show("Initial — Default Settings")


# ── Change 1 ────────────────────────────────────────────────────
# Save before changing — checkpoint banavo
history.push(settings.save())          # snapshot 1 saved

settings.toggle_email()                # Email band kari
settings.enable_dnd()                  # DND on kari
settings.show("After Change 1 — Email OFF, DND ON")


# ── Change 2 ────────────────────────────────────────────────────
history.push(settings.save())          # snapshot 2 saved

settings.toggle_sms()                  # SMS pan band kari
settings.set_frequency("daily")        # frequency badli
settings.show("After Change 2 — SMS OFF, Freq: daily")


# ── Change 3 ────────────────────────────────────────────────────
history.push(settings.save())          # snapshot 3 saved

settings.toggle_push()                 # Push pan band kari
settings.show("After Change 3 — Push OFF too")

print(f"\n  [History] {history.count()} checkpoints saved")


# ── UNDO 1 ──────────────────────────────────────────────────────
print("\n  → UNDO pressed...")
settings.restore(history.pop())        # snapshot 3 restore
settings.show("After Undo 1 — Back to before Change 3")


# ── UNDO 2 ──────────────────────────────────────────────────────
print("\n  → UNDO pressed again...")
settings.restore(history.pop())        # snapshot 2 restore
settings.show("After Undo 2 — Back to before Change 2")


# ── UNDO 3 ──────────────────────────────────────────────────────
print("\n  → UNDO pressed again...")
settings.restore(history.pop())        # snapshot 1 restore
settings.show("After Undo 3 — Back to Original")


# ── UNDO 4 — history empty ──────────────────────────────────────
print("\n  → UNDO pressed — but history khaali che...")
result = history.pop()
if result is None:
    print("  Nothing to undo.")


# ================================================================
#  PROOF — Encapsulation intact
#  Caretaker Memento hold kare che pan read nahi kari shake
# ================================================================

print("\n" + "=" * 50)
print("  ENCAPSULATION PROOF")
print("=" * 50)

test_snapshot = settings.save()

# Caretaker try kare to read internal state — fails
try:
    print(test_snapshot.__email_on)   # name mangling — AttributeError
except AttributeError:
    print("  Caretaker cannot read Memento internals. ✓")
    print("  Only NotificationSettings (Originator) can restore from it.")


# ================================================================
#  COMPARE — With vs Without Memento
# ================================================================

print("\n" + "=" * 50)
print("  WITHOUT MEMENTO (naive — wrong way)")
print("=" * 50)
print("""
  # Bahar thi state read karo — encapsulation tute
  saved = {
      "email": settings.email_on,     # private internals expose
      "sms":   settings.sms_on,
      "push":  settings.push_on,
      "dnd":   settings.dnd_mode,
      "freq":  settings.frequency
  }
  # Problem 1: Navo field aavyu → saving code pan badle
  # Problem 2: Bahar ne badhu khabar padyu — tight coupling
  # Problem 3: settings class na internals badlya → badhu tute
""")

print("  WITH MEMENTO (correct way)")
print("-" * 50)
print("""
  snapshot = settings.save()   # object khud pack kare
  settings.restore(snapshot)   # object khud unpack kare
  # Bahar koi nathi jaanta andar shu che
  # Internal fields badlya → saving code same rahe
  # Encapsulation 100% intact
""")
