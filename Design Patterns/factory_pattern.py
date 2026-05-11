from abc import ABC, abstractmethod

# --- Product Interface ---


class Shirt(ABC):
    @abstractmethod
    def get_info(self): pass

# --- Concrete Products ---


class HM_Shirt(Shirt):
    def get_info(self): return "H&M Slim Fit Cotton Shirt"


class Zara_Shirt(Shirt):
    def get_info(self): return "Zara Luxury Silk Shirt"

# --- The Factory Method ---


class ShirtFactory:
    @staticmethod
    def get_shirt(style):
        # The logic of 'which brand' is hidden inside this method
        if style == "cheap":
            return HM_Shirt()
        elif style == "fancy":
            return Zara_Shirt()
        else:
            raise ValueError("Style not found")


# --- Usage ---
# You don't care about the brand; you just ask for a "style"
my_shirt = ShirtFactory.get_shirt("fancy")
print(my_shirt.get_info())  # Output: Zara Luxury Silk Shirt
my_other_shirt = ShirtFactory.get_shirt("cheap")
print(my_other_shirt.get_info())  # Output: H&M Slim Fit Cotton Shirt
