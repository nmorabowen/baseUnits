from __future__ import annotations
from typing import TYPE_CHECKING, Dict

# Import the Dimension class
from .dimension import Dimension

if TYPE_CHECKING:
    from .quantity import Quantity

# --- Base Unit Registry ---
# This private dictionary will store {Dimension: Unit}
# e.g., {Dimension('Length'): mm, Dimension('Force'): N}
_BASE_UNIT_REGISTRY: Dict[Dimension, 'Unit'] = {}

def register_base_unit(unit_object: 'Unit') -> 'Unit':
    """
    Decorator/function to register a Unit as the base for its dimension.
    
    This function is called from within each dimensions/ file.
    """
    dim = unit_object.dimension
    if dim in _BASE_UNIT_REGISTRY:
        raise ValueError(f"Base unit for {dim!r} is already registered as {_BASE_UNIT_REGISTRY[dim]}")
    _BASE_UNIT_REGISTRY[dim] = unit_object
    return unit_object 

def get_base_unit(dimension: Dimension) -> 'Unit':
    """
    Gets the registered base unit for a given dimension.
    
    If the dimension is compound, it builds a new compound
    base unit from the simple base units.
    """
    # 1. Check if it's a simple, registered dimension (fast path)
    if dimension in _BASE_UNIT_REGISTRY:
        return _BASE_UNIT_REGISTRY[dimension]

    # 2. If not, it must be compound. Build it.
    if len(dimension.components) > 0:
        new_base_unit = None
        for base_dim, exponent in dimension.components.items():
            # Look up the base unit for each *component* (e.g., 'Mass')
            # We create a new Dimension object for the lookup
            component_base_unit = _BASE_UNIT_REGISTRY.get(Dimension(base_dim))
            
            if not component_base_unit:
                raise KeyError(f"No base unit registered for component dimension '{base_dim}'")
            
            # Apply the exponent (e.g., mm**-2)
            part = component_base_unit ** exponent
            
            # Multiply them together (e.g., N * mm**-2)
            if new_base_unit is None:
                new_base_unit = part
            else:
                new_base_unit = new_base_unit * part
        
        if new_base_unit is not None:
            return new_base_unit

    # 3. If we failed to find or build it, raise an error
    raise KeyError(f"No base unit registered for dimension {dimension!r}")


class Unit:
    """
    Represents the definition of a physical unit.
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