from __future__ import annotations
from .units import Unit, get_base_unit
from .dimension import Dimension

class Quantity:
    
    def __init__(self, value: float | int, unit: Unit):
        if not isinstance(unit, Unit):
            raise TypeError(f"Cannot create a Quantity. 'unit' must be a Unit object, not {type(unit)}.")
        
        self.value = float(value)
        self.unit = unit
        # This is the "hard-coded" consistent value
        self.base_value = self.value * self.unit.factor 

    def to(self, new_unit: Unit) -> Quantity:
        if not isinstance(new_unit, Unit):
            raise TypeError(f"Cannot convert. 'new_unit' must be a Unit object, not {type(new_unit)}.")
        if self.unit.dimension != new_unit.dimension:
            raise TypeError(f"Cannot convert from dimension {self.unit.dimension!r} to {new_unit.dimension!r}")
        
        new_value = self.base_value / new_unit.factor
        return Quantity(new_value, new_unit)

    def to_base(self) -> Quantity:
        """
        Converts the Quantity to its dimension's base unit.
        """
        dim = self.unit.dimension
        base_unit = get_base_unit(dim)
        return self.to(base_unit)

    # --- Arithmetic Operations (Updated) ---
    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity): return NotImplemented
        if self.unit.dimension != other.unit.dimension:
            raise TypeError(f"Cannot add {self.unit.dimension!r} and {other.unit.dimension!r}")
        new_base_value = self.base_value + other.base_value
        return Quantity(new_base_value / self.unit.factor, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity): return NotImplemented
        if self.unit.dimension != other.unit.dimension:
            raise TypeError(f"Cannot subtract {other.unit.dimension!r} from {self.unit.dimension!r}")
        new_base_value = self.base_value - other.base_value
        return Quantity(new_base_value / self.unit.factor, self.unit)
    
    def __mul__(self, other: float | int | Quantity | Unit) -> Quantity:
        """
        Multiplies a Quantity by a scalar, another Quantity, or a Unit.
        - (10 * m) * 2     -> 20 * m
        - (10 * N) * (5 * m) -> 50 * (N*m)
        - (10 * N) * m     -> 10 * (N*m)
        """
        if isinstance(other, (int, float)):
            # Scalar multiplication
            return Quantity(self.value * other, self.unit)
        
        if isinstance(other, Quantity):
            # Compound multiplication
            new_value = self.value * other.value
            new_unit = self.unit * other.unit
            return Quantity(new_value, new_unit)

        # --- THIS IS THE NEW LOGIC ---
        if isinstance(other, Unit):
            # (10 * N) * m  -> 10 * (N*m)
            new_unit = self.unit * other
            return Quantity(self.value, new_unit)
        # --- END NEW LOGIC ---
            
        return NotImplemented

    def __rmul__(self, other: float | int) -> Quantity:
        return self.__mul__(other)
    
    def __truediv__(self, other: float | int | Quantity | Unit) -> Quantity:
        """
        Divides a Quantity by a scalar, another Quantity, or a Unit.
        - (10 * m) / 2     -> 5 * m
        - (100 * N) / (10 * mm**2) -> 10 * (N/mm**2)
        - (10 * m) / s     -> 10 * (m/s)
        """
        if isinstance(other, (int, float)):
            # Scalar division
            return Quantity(self.value / other, self.unit)
        
        if isinstance(other, Quantity):
            # Compound division
            new_value = self.value / other.value
            new_unit = self.unit / other.unit
            return Quantity(new_value, new_unit)
            
        # --- THIS IS THE NEW LOGIC ---
        if isinstance(other, Unit):
            # (10 * m) / s -> 10 * (m/s)
            new_unit = self.unit / other
            return Quantity(self.value, new_unit)
        # --- END NEW LOGIC ---

        return NotImplemented
    
    def __pow__(self, power: int | float) -> Quantity:
        if not isinstance(power, (int, float)): return NotImplemented
        new_value = self.value ** power
        new_unit = self.unit ** power
        return Quantity(new_value, new_unit)

    def __repr__(self) -> str:
        return f"Quantity({self.value}, {self.unit!r})"
    def __str__(self) -> str:
        return f"{self.value} {self.unit.symbol}"