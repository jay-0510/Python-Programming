# Two in one -- Abstract Factory and Factory Method
# Factory Method -- creates one product based on input
# Abstract Factory -- creates families of related products (shirts + jeans)
# ============================================================
#  PATTERN 1: FACTORY METHOD — Car Manufacturing
#
#  Scenario: A car company has multiple factories (India, Germany).
#  Each factory knows how to build ONE type of car.
#  The caller just says "build me a car" — doesn't care how.
#
#  KEY IDEA: Subclass decides WHICH object to create.
# ============================================================

# --- The Car (product) ---

class Car:
    def specs(self):
        raise NotImplementedError  # every car must describe itself


class HatchbackCar(Car):
    def specs(self):
        print("Hatchback | Small | Fuel-efficient | City use")


class SedanCar(Car):
    def specs(self):
        print("Sedan     | Medium | Comfort | Highway use")


class SUVCar(Car):
    def specs(self):
        print("SUV       | Large | 4WD | Off-road capable")


# --- The Factory (creator) ---
# Each factory subclass overrides build_car() to decide what Car to make

class CarFactory:
    def build_car(self) -> Car:
        raise NotImplementedError  # subclasses MUST override this


class IndiaFactory(CarFactory):
    def build_car(self) -> Car:
        # India market → build small, affordable hatchback
        return HatchbackCar()


class GermanyFactory(CarFactory):
    def build_car(self) -> Car:
        # Germany market → build premium sedan
        return SedanCar()


class USAFactory(CarFactory):
    def build_car(self) -> Car:
        # USA market → build big SUV
        return SUVCar()


# --- Client code — doesn't know or care which car is created ---

def deliver_car(factory: CarFactory):
    car = factory.build_car()  # factory decides the type
    print("Car delivered →", end=" ")
    car.specs()


deliver_car(IndiaFactory())    # → Hatchback
deliver_car(GermanyFactory())  # → Sedan
deliver_car(USAFactory())      # → SUV


# ============================================================
#  PATTERN 2: ABSTRACT FACTORY — Car + Engine + Tyres (a FAMILY)
#
#  Scenario: Now it's not just the car body.
#  Each region also has its own Engine AND Tyres that must match.
#  You can't mix a German engine with Indian tyres — they're a SET.
#
#  KEY IDEA: A factory that creates a FAMILY of related objects,
#            all guaranteed to be compatible with each other.
#
#  Factory Method  → creates ONE product
#  Abstract Factory → creates a FAMILY of related products
# ============================================================

print("\n" + "="*55)
print(" ABSTRACT FACTORY")
print("="*55 + "\n")

# ---- Product Family 1: Engines ----


class Engine:
    def describe(self):
        raise NotImplementedError


class PetrolEngine(Engine):
    def describe(self):
        print("  Engine : 1.2L Petrol — fuel-efficient, low cost")


class DieselEngine(Engine):
    def describe(self):
        print("  Engine : 2.0L Diesel — high torque, highway")


class ElectricEngine(Engine):
    def describe(self):
        print("  Engine : 400V Electric — zero emission, instant torque")


# ---- Product Family 2: Tyres ----

class Tyre:
    def describe(self):
        raise NotImplementedError


class CityTyre(Tyre):
    def describe(self):
        print("  Tyres  : 175mm Narrow — smooth roads, city grip")


class AllTerrainTyre(Tyre):
    def describe(self):
        print("  Tyres  : 265mm Wide — mud, gravel, off-road")


class SportsTyre(Tyre):
    def describe(self):
        print("  Tyres  : 225mm Sport — dry track, high-speed cornering")


# ---- Product Family 3: Car Body ----
# (reusing from above, simplified)

class IndiaBody:
    def describe(self):
        print("  Body   : Hatchback — compact, lightweight")


class GermanyBody:
    def describe(self):
        print("  Body   : Sedan — aerodynamic, premium interior")


class USABody:
    def describe(self):
        print("  Body   : SUV — large frame, high clearance")


# ---- Abstract Factory Interface ----
# Defines WHAT products a factory must produce — not HOW

class AbstractCarFactory:
    def create_body(self):
        raise NotImplementedError

    def create_engine(self):
        raise NotImplementedError

    def create_tyres(self):
        raise NotImplementedError


# ---- Concrete Factories — each returns a COMPATIBLE family ----

class IndiaCarFactory(AbstractCarFactory):
    def create_body(self):
        return IndiaBody()       # compact body

    def create_engine(self):
        return PetrolEngine()    # matches compact body

    def create_tyres(self):
        return CityTyre()        # matches city use case


class GermanyCarFactory(AbstractCarFactory):
    def create_body(self):
        return GermanyBody()     # premium sedan body

    def create_engine(self):
        return DieselEngine()    # matches highway driving

    def create_tyres(self):
        return SportsTyre()      # matches performance sedan


class USACarFactory(AbstractCarFactory):
    def create_body(self):
        return USABody()         # large SUV frame

    def create_engine(self):
        return ElectricEngine()  # EV-first US market trend

    def create_tyres(self):
        return AllTerrainTyre()  # matches SUV off-road use


# ---- Assembler — works with ANY factory, gets a full compatible car ----

def assemble_car(factory: AbstractCarFactory):
    # factory guarantees all parts belong to the same family
    body = factory.create_body()
    engine = factory.create_engine()
    tyres = factory.create_tyres()

    print("Assembling car...")
    body.describe()
    engine.describe()
    tyres.describe()
    print()


assemble_car(IndiaCarFactory())    # Hatchback + Petrol + City tyres
assemble_car(GermanyCarFactory())  # Sedan + Diesel + Sport tyres
assemble_car(USACarFactory())      # SUV + Electric + All-terrain tyres
