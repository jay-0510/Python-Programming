# state Pattern -- Change behaviour when internal state changes, It avoids massive if-else or switch statements

# State Interface
class State:     # Defines each & every state must do (toggle the switch)
    def handle_toggle(self, switch):
        self.switch = switch

# These 2 classes define the specific behaviour for each state


class OnState(State):
    def handle_toggle(self, switch):
        print("Turning light OFF...")
        switch.set_state(OffState())  # Transition to next state


class OffState(State):
    def handle_toggle(self, switch):
        print("Turning light ON...")
        switch.set_state(OnState())   # Transition to next state

# CONTEXT - LIGHT SWITCH -- object whose behaviour changes


class LightSwitch:
    def __init__(self):  # initial stage is OFF
        self.current_state = OffState()

    def set_state(self, state):
        self.current_state = state

    def press_button(self):   # Switch assign the works to current object
        self.current_state.handle_toggle(self)


my_switch = LightSwitch()

my_switch.press_button()  # First press - Light ON
my_switch.press_button()  # Second Press - Light OFF
my_switch.press_button()  # Third Press - Light ON
