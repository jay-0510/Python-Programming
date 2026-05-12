# Adapter Pattern -- THis pattern act as a bridge between two incompatible system, so they can work together seamlessly

# classes with incompatible interfaces work together by wrapping one in another.
# Eg:: TRAVEL POWER ADAPTER --- Indian Plug, European socket --> adapter sits in between so both can connect.

class TypeCPhone:  # TARGET INTERFACE -- (What iphone expects)
    def charge_type_c(self):
        pass


class LightningCable:  # Act as ADAPTEE (incompabtible system)
    def plug_lightning(self):
        return "Charge with Lightning Cable"


class ChargeCable(TypeCPhone):  # ADAPTER (Bridge nu kaam karse)
    # "wraps" the old cable and makes it look like a Type-C connection.
    def __init__(self, lightning_cable: LightningCable):
        self.lightning_cable = lightning_cable

    # Adapter calls the old lightning method internally.
    def charge_type_c(self):
        result = self.lightning_cable.plug_lightning()
        return (f'Adpater Converting : {result} to Type-C')

# Client


class iphone17:
    def charge(self, charger: TypeCPhone):
        # Iphone only knows, it will work in Type-C
        print(charger.charge_type_c())


# Exceution
my_iphone = iphone17()   # Iphone expects Type-C Cable
old_cable = LightningCable()  # Old Cable

# my_iphone.charge(old_cable) # It will fail!! INCOMPATIBLE


adapter = ChargeCable(old_cable)  # Using the adapter to connect(bridge) them.

my_iphone.charge(adapter)  # works..
