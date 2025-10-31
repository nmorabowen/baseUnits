from __future__ import annotations
from .units import Unit, get_base_unit  # <-- Import get_base_unit
from .dimension import Dimension

class Quantity:
    """
    Represents a physical quantity: a value and a Unit.
    ...
    """

    def __init__(self, value: float | int, unit: Unit):
        if not isinstance(unit, Unit):
            raise TypeError(f"Cannot create a Quantity. 'unit' must be a Unit object, not {type(unit)}.")
        
        self.value = float(value)
        self.unit = unit
        self.base_value = self.value * self.unit.factor

    def to(self, new_unit: Unit) -> Quantity:
        # ... (no changes to this method) ...
        if not isinstance(new_unit, Unit):
            raise TypeError(f"Cannot convert. 'new_unit' must be a Unit object, not {type(new_unit)}.")
        if self.unit.dimension != new_unit.dimension:
            raise TypeError(f"Cannot convert from dimension {self.unit.dimension!r} to {new_unit.dimension!r}")
        new_value = self.base_value / new_unit.factor
        return Quantity(new_value, new_unit)

    # --- NEW METHOD ---
    def to_base(self) -> Quantity:
        """
        Converts the Quantity to its dimension's base unit.
        
        e.g., 10*ft -> 3048.0*mm
        e.g., 5*ksi -> 34.475*MPa
        """
        # 1. Get the dimension of this quantity
        dim = self.unit.dimension
        
        # 2. Look up the base unit for that dimension
        base_unit = get_base_unit(dim)
        
        # 3. Use the existing .to() method to convert
        return self.to(base_unit)
    # --- END NEW ---

    # --- Arithmetic Operations ---
    # ... (no changes to __add__, __sub__, __mul__, etc.) ...
    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit.dimension != other.unit.dimension:
            raise TypeError(f"Cannot add {self.unit.dimension!r} and {other.unit.dimension!r}")
        new_base_value = self.base_value + other.base_value
        return Quantity(new_base_value / self.unit.factor, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.unit.dimension != other.unit.dimension:
            raise TypeError(f"Cannot subtract {other.unit.dimension!r} from {self.unit.dimension!r}")
        new_base_value = self.base_value - other.base_value
        return Quantity(new_base_value / self.unit.factor, self.unit)
    
    def __mul__(self, other: float | int | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        if isinstance(other, Quantity):
            new_value = self.value * other.value
            new_unit = self.unit * other.unit
            return Quantity(new_value, new_unit)
        return NotImplemented

    def __rmul__(self, other: float | int) -> Quantity:
        return self.__mul__(other)
    
    def __truediv__(self, other: float | int | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        if isinstance(other, Quantity):
            new_value = self.value / other.value
            new_unit = self.unit / other.unit
            return Quantity(new_value, new_unit)
        return NotImplemented
    
    def __pow__(self, power: int | float) -> Quantity:
        if not isinstance(power, (int, float)):
            return NotImplemented
        new_value = self.value ** power
        new_unit = self.unit ** power
        return Quantity(new_value, new_unit)

    # --- Representation ---
    def __repr__(self) -> str:
        return f"Quantity({self.value}, {self.unit!r})"
    def __str__(self) -> str:
        return f"{self.value} {self.unit.symbol}"