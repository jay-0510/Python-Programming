# Customise House Making

class House:
    # constructors which accept different arguments
    def __init__(self, bedrooms, bathrooms, kitchen, garden, garage, pools, playground, solar_panels):
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.kitchen = kitchen
        self.garden = garden
        self.garage = garage
        self.pools = pools
        self.playground = playground
        self.solar_panel = solar_panels

    def __str__(self):   # String method split out the features
        features = [
            f"Bedrooms: {self.bedrooms}",
            f"Bathrooms: {self.bathrooms}",
            f"Kitchen: {'Yes' if self.kitchen else 'No'}",
            f"Garden: {'Yes' if self.garden else 'No'}",
            f"Garage: {'Yes' if self.garage else 'No'}",
            f"Pools: {'Yes' if self.pools else 'No'}",
            f"PlayGround: {'Yes' if self.playground else 'No'}",
            f"Solar Panels: {'Yes' if self.solar_panel else 'No'}",
        ]
        return " | ".join(features)

# creating a house
# house = House(3, 2, True, True, False, False, True, True)
# print(house)

# Builder Pattern helps us to create complex objects step by step in readbale & flexible way.


class HouseBuilder:
    def __init__(self):   # Own constructors
        self.bedrooms = 2
        self.bathrooms = 1
        self.kitchen = True
        self.garden = False
        self.garage = False
        self.pools = False
        self.playground = True
        self.solar_panels = False

# different methods ( independently with each features)

    def set_bedrooms(self, count):
        self.bedrooms = count
        return self

    def set_bathrooms(self, count):
        self.bathrooms = count
        return self

    def add_kitchen(self):
        self.kitchen = True
        return self

    def add_garden(self):
        self.garden = True
        return self

    def add_garage(self):
        self.garage = True
        return self

    def add_pool(self):
        self.pools = True
        return self

    def add_playground(self):
        self.playground = True
        return self

    def add_solar_panels(self):
        self.solar_panels = True
        return self

# To actually build a home -- we can have build method which actually creates house & returns house object
    def build(self):
        return House(self.bedrooms, self.bathrooms, self.kitchen, self.playground, self.pools, self.garden, self.garage, self.solar_panels)


# creating the custom house
house_builder = HouseBuilder()

custom_house = (
    house_builder.set_bedrooms(4)
    .set_bathrooms(2)
    .add_kitchen()
    .add_garden()
    .add_playground()
    .add_solar_panels()
    .build()
)

print("Custom_House :", custom_house)


# Keeps creation logic separate from Main logic
