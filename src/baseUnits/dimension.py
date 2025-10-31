from __future__ import annotations
from collections import defaultdict
import math

class Dimension:
    """
    Represents the physical dimension of a unit (e.g., Length, Time, Mass^1*Length^-2).
    
    This class stores dimensions as a dictionary of base dimension names
    and their exponents.
    """
    
    def __init__(self, base_dims: dict[str, float | int] | str):
        """
        Initializes a Dimension.
        
        Args:
            base_dims: A string for a simple dimension (e.g., "Length") or
                       a dict for a compound one (e.g., {"Length": 1, "Time": -1}).
        """
        if isinstance(base_dims, str):
            # Simple dimension like "Length"
            self._dims = {base_dims: 1}
        elif isinstance(base_dims, dict):
            # Compound dimension
            self._dims = {k: v for k, v in base_dims.items() if v != 0}
        else:
            raise TypeError(f"Cannot create Dimension from {type(base_dims)}")

    @property
    def is_dimensionless(self) -> bool:
        """Checks if the dimension is dimensionless (all exponents are 0)."""
        return not any(self._dims.values())

    def __repr__(self) -> str:
        """Creates a string representation, e.g., 'Length^1 * Time^-1'"""
        parts = [f"{dim}^{exp}" for dim, exp in sorted(self._dims.items())]
        return " * ".join(parts) if parts else "Dimensionless"

    def __eq__(self, other: object) -> bool:
        """Checks if two dimensions are identical."""
        if not isinstance(other, Dimension):
            return False
        return self._dims == other._dims

    def __mul__(self, other: Dimension) -> Dimension:
        """
        Multiplies two dimensions (adds their exponents).
        e.g., Length * Time -> {"Length": 1, "Time": 1}
        e.g., Length * Length -> {"Length": 2}
        """
        new_dims = defaultdict(int, self._dims)
        for dim, exp in other._dims.items():
            new_dims[dim] += exp
        return Dimension(dict(new_dims))

    def __truediv__(self, other: Dimension) -> Dimension:
        """
        Divides two dimensions (subtracts their exponents).
        e.g., Length / Time -> {"Length": 1, "Time": -1}
        """
        new_dims = defaultdict(int, self._dims)
        for dim, exp in other._dims.items():
            new_dims[dim] -= exp
        return Dimension(dict(new_dims))

    def __pow__(self, power: float | int) -> Dimension:
        """
        Raises a dimension to a power (multiplies all exponents).
        e.g., Length**2 -> {"Length": 2}
        e.g., (Length/Time)**2 -> {"Length": 2, "Time": -2}
        """
        new_dims = {dim: exp * power for dim, exp in self._dims.items()}
        return Dimension(new_dims)