"""kg-cm-s consistent unit system (L-M-T).

Length=cm, mass=kg, time=s. Force is *derived* and equals
``1 kg * 1 cm/s^2 = 0.01 N``; this derived unit has no popular name, so
``BASE`` reads ``"cm-kg-s"`` (force slot omitted).

Notable values in this system:

- ``kg = 1.0`` (base mass), ``cm = 1.0`` (base length).
- ``N = 100`` (1 N = 100 system force units).
- ``Pa = 0.01``, ``MPa = 1e4``.
- ``g = 980.665`` (cm/s²).
- ``J = 1e4`` (the system energy base, ``kg*cm^2/s^2``, is 100 erg).
"""

from .._make_system import make_system as _make

_ns = _make(length="cm", mass="kg", time="s")
globals().update(_ns.__dict__)
__all__ = [k for k in _ns.__dict__]
del _make, _ns
