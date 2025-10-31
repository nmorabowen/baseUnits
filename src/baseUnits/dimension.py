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
    def components(self) -> dict[str, float | int]:
        """Returns the dictionary of base dimensions and their exponents."""
        return self._dims

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

    # --- NEW METHOD ---
    def __hash__(self) -> int:
        """
        Makes the Dimension object hashable so it can be used as a
        dictionary key.
        
        We do this by creating an immutable, sorted tuple of its
        internal items and hashing that.
        """
        sorted_items = tuple(sorted(self._dims.items()))
        return hash(sorted_items)
    # --- END NEW ---

    def __mul__(self, other: Dimension) -> Dimension:
        """
        Multiplies two dimensions (adds their exponents).
        """
        new_dims = defaultdict(int, self._dims)
        for dim, exp in other._dims.items():
            new_dims[dim] += exp
        return Dimension(dict(new_dims))

    def __truediv__(self, other: Dimension) -> Dimension:
        """
        Divides two dimensions (subtracts their exponents).
        """
        new_dims = defaultdict(int, self._dims)
        for dim, exp in other._dims.items():
            new_dims[dim] -= exp
        return Dimension(dict(new_dims))

    def __pow__(self, power: float | int) -> Dimension:
        """
        Raises a dimension to a power (multiplies all exponents).
        """
        new_dims = {dim: exp * power for dim, exp in self._dims.items()}
        return Dimension(new_dims)