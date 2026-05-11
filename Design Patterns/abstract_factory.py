# --- STEP 1: The Blueprints (Abstract Products) ---
class Shirt:
    def wear(self): pass


class Jeans:
    def wear(self): pass

# --- STEP 2: Concrete Brand Items (H&M) ---


class HMShirt(Shirt):
    def wear(self): print("Wearing H&M Shirt")


class HMJeans(Jeans):
    def wear(self): print("Wearing H&M Jeans")

# --- STEP 3: The Brand Factory (Abstract Factory) ---


class BrandFactory:
    def get_shirt(self): pass
    def get_jeans(self): pass

# --- STEP 4: The Actual H&M Store (Concrete Factory) ---


class HMStore(BrandFactory):
    def get_shirt(self): return HMShirt()  # Returns H&M shirt
    def get_jeans(self): return HMJeans()  # Returns H&M jeans

# --- STEP 5: Using the Factory (Client) ---


def shopping_trip(factory):
    shirt = factory.get_shirt()  # Doesn't care about brand
    jeans = factory.get_jeans()  # Just knows it's getting clothes
    shirt.wear()
    jeans.wear()


# Execute: Buy everything from H&M
my_factory = HMStore()
shopping_trip(my_factory)

# Blueprint -- tells every shirt must have wear function
# Concrete Product -- H&M Shirt implements the blueprint
# Abstract Factory -- BrandFactory defines the interface for creating products
# Concrete Factory -- HMStore implements the BrandFactory to create H&M products
