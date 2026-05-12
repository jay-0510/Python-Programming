# Builder Pattern -- HOw to assemble one complex object ??
# One Product with many optional parts

# Why need of Builder pattern ?
# When an object has many optional parts & we don't need all of them ....... Builder lets you construct it piece by piece instead ofone big messy call.


# ============================================================
#  BUILDER PATTERN — Ordering a Burger at a Restaurant
#
#  Analogy:
#  You walk into a burger place.
#  Every burger has a bun and a patty.
#  But cheese, sauce, veggies — those are YOUR choice.
#
#  The person at the counter (Builder) takes your order
#  step by step. When you say "that's it", they hand you
#  the final burger (build).
#
#  Without Builder → Burger("sesame", "beef", True, False, True, "mayo")
#                    What is True? What is False? No idea.
#
#  With Builder    → clear, readable, only set what you want.
# ============================================================


# ---- The Product ----

class Burger:
    def __init__(self):
        self.bun = None
        self.patty = None
        self.cheese = False   # optional — default off
        self.lettuce = False   # optional
        self.tomato = False   # optional
        self.sauce = None    # optional

    def __str__(self):
        toppings = []
        if self.cheese:
            toppings.append("Cheese")
        if self.lettuce:
            toppings.append("Lettuce")
        if self.tomato:
            toppings.append("Tomato")
        toppings = ", ".join(toppings) if toppings else "None"

        return (
            f"\n  Bun      : {self.bun}"
            f"\n  Patty    : {self.patty}"
            f"\n  Toppings : {toppings}"
            f"\n  Sauce    : {self.sauce or 'None'}"
        )


# ---- The Builder ----

class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()    # start with an empty burger

    def set_bun(self, bun):
        self.burger.bun = bun
        return self               # return self → enables chaining

    def set_patty(self, patty):
        self.burger.patty = patty
        return self

    def add_cheese(self):
        self.burger.cheese = True  # no argument needed — just add it
        return self

    def add_lettuce(self):
        self.burger.lettuce = True
        return self

    def add_tomato(self):
        self.burger.tomato = True
        return self

    def set_sauce(self, sauce):
        self.burger.sauce = sauce
        return self

    def build(self):
        return self.burger         # hand over the finished burger


# ---- The Director — preset menu items ----

class BurgerMenu:
    def classic_burger(self):
        return (
            BurgerBuilder()
            .set_bun("Sesame")
            .set_patty("Beef")
            .add_cheese()
            .set_sauce("Ketchup")
            .build()
        )

    def veg_burger(self):
        return (
            BurgerBuilder()
            .set_bun("Whole Wheat")
            .set_patty("Veggie")
            .add_lettuce()
            .add_tomato()
            .set_sauce("Mint Chutney")
            .build()
        )


# ---- Usage ----

menu = BurgerMenu()


print(menu.classic_burger())

print(menu.veg_burger())

custom = (
    BurgerBuilder()
    .set_bun("Brioche")
    .set_patty("Chicken")
    .add_cheese()
    .add_tomato()
    .set_sauce("BBQ")
    .build()
)
print(custom)
