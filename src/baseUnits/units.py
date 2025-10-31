from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from .dimension import Dimension

if TYPE_CHECKING:
    from .quantity import Quantity

# --- NEW: Base Unit Registry ---
# This private dictionary will store {Dimension: Unit}
# e.g., {Dimension('Length'): mm, Dimension('Force'): N}
_BASE_UNIT_REGISTRY: Dict[Dimension, 'Unit'] = {}

def register_base_unit(unit_object: 'Unit') -> 'Unit':
    """
    Decorator/function to register a Unit as the base for its dimension.
    """
    dim = unit_object.dimension
    if dim in _BASE_UNIT_REGISTRY:
        # This check is useful for debugging
        raise ValueError(f"Base unit for {dim!r} is already registered as {_BASE_UNIT_REGISTRY[dim]}")
    _BASE_UNIT_REGISTRY[dim] = unit_object
    return unit_object # Return the unit so it can be used inline

def get_base_unit(dimension: Dimension) -> 'Unit':
    """
    Gets the registered base unit for a given dimension.
    """
    if dimension not in _BASE_UNIT_REGISTRY:
        raise KeyError(f"No base unit registered for dimension {dimension!r}")
    return _BASE_UNIT_REGISTRY[dimension]
# --- END NEW ---


class Unit:
    """
    Represents the definition of a physical unit.
    ...
    """

    def __init__(self, name: str, symbol: str, dimension: Dimension | str, factor: float):
        self.name = name
        self.symbol = symbol
        
        if isinstance(dimension, str):
            self.dimension = Dimension(dimension)
        elif isinstance(dimension, Dimension):
            self.dimension = dimension
        else:
            raise TypeError(f"unit 'dimension' must be a str or Dimension object, not {type(dimension)}")
            
        self.factor = factor

    def __repr__(self) -> str:
        return self.symbol

    def __rmul__(self, value: float | int) -> Quantity:
        from .quantity import Quantity 
        
        if isinstance(value, (int, float)):
            return Quantity(value, self)
        return NotImplemented

    def __mul__(self, other: float | int | Unit) -> Quantity | Unit:
        if isinstance(other, (int, float)):
            return self.__rmul__(other)
        
        if isinstance(other, Unit):
            new_factor = self.factor * other.factor
            new_dimension = self.dimension * other.dimension
            new_symbol = f"({self.symbol}*{other.symbol})"
            new_name = f"({self.name}*{other.name})"
            return Unit(new_name, new_symbol, new_dimension, new_factor)
            
        return NotImplemented

    def __truediv__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            return NotImplemented
        
        new_factor = self.factor / other.factor
        new_dimension = self.dimension / other.dimension
        new_symbol = f"({self.symbol}/{other.symbol})"
        new_name = f"({self.name}/{other.name})"
        
        return Unit(new_name, new_symbol, new_dimension, new_factor)

    def __pow__(self, power: int | float) -> Unit:
        if not isinstance(power, (int, float)):
            return NotImplemented
            
        new_factor = self.factor ** power
        new_dimension = self.dimension ** power
        new_symbol = f"({self.symbol}**{power})"
        new_name = f"({self.name}**{power})"
        
        return Unit(new_name, new_symbol, new_dimension, new_factor)