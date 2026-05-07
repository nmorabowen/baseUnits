"""baseUnits — float-based unit conversion factors for consistent unit systems.

The top-level package re-exports the default ``N-mm-tonne-s`` system as named
float constants. Multiply scalar values by a unit (``5 * m``) to convert them
into the active system's base units, and divide by a unit to convert back out.

Other pre-built systems live under ``baseUnits.systems`` and follow the
``<force>_<length>_<time>`` naming pattern: ``N_mm_s`` (default), ``N_m_s``,
``kN_m_s``, ``kip_in_s``, ``kgf_m_s``, ``dyne_cm_s``. For runtime dimensional
safety, use the opt-in ``baseUnits.checked`` layer instead.

Attributes:
    BASE: Human-readable label of the active system (e.g. ``"N-mm-tonne-s"``).
    g: Standard gravitational acceleration in the active system.

Example:
    >>> import baseUnits as u
    >>> u.BASE
    'N-mm-tonne-s'
    >>> 5 * u.m            # 5 metres expressed in mm
    5000.0
    >>> (10 * u.MPa) / u.MPa
    1.0
"""

from . import checked, systems
from .systems.N_mm_s import *
from .systems.N_mm_s import BASE, g
