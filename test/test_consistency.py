"""The one consistency rule.

Every consistent unit system in this library must satisfy Newton's second
law without spurious factors. This file is the single canonical place
where that invariant is enforced, parametrized over every system.

Each entry in ``SYSTEMS`` declares all three primitive choices explicitly
(length, time, plus exactly one of force or mass — matching the
:func:`baseUnits._make_system.make_system` signature). The fourth
primitive is derived from the consistency rule.

Four assertions per system:
  1. F = m * a holds numerically (100 kg * 9.81 m/s^2 = 981 N).
  2. sigma = F / A holds numerically (20 kgf / 2 mm^2 = 98.0665 MPa).
  3. Every unit's value in the system equals (absolute SI) / (system base SI),
     for every unit in every dimension dict in _factors.
  4. Natural derived bases (the F/L^2 pressure unit, the F*L energy unit,
     the F*L/T power unit) collapse to exactly 1.0 in their system.
"""

import importlib

import pytest

from baseUnits import _factors as _f

# (sysname, length, force_or_None, mass_or_None, time)
# Exactly one of force / mass is set per row. The other is derived by
# make_system so F = m * a holds without factors.
SYSTEMS = [
    ("N_mm_s", "mm", "N", None, "s"),
    ("N_m_s", "m", "N", None, "s"),
    ("kN_m_s", "m", "kN", None, "s"),
    ("kip_in_s", "inches", "kip", None, "s"),
    ("kgf_m_s", "m", "kgf", None, "s"),  # derived mass = hyl (unnamed)
    ("dyne_cm_s", "cm", "dyne", None, "s"),  # CGS
]


def _bases(L_name, F_name, M_name, T_name):
    """Return the seven base SI scalars (L, T, F, M, P, E, Pw, D, UW)."""
    L = _f.LENGTH[L_name]
    T = _f.TIME[T_name]
    if F_name is not None:
        F = _f.FORCE[F_name]
        M = F * T**2 / L
    else:
        M = _f.MASS[M_name]
        F = M * L / T**2
    return {
        "LENGTH": L,
        "FORCE": F,
        "MASS": M,
        "TIME": T,
        "PRESSURE": F / L**2,
        "ENERGY": F * L,
        "POWER": F * L / T,
        "DENSITY": M / L**3,
        "UNIT_WEIGHT": F / L**3,
    }


@pytest.mark.parametrize("sysname,L_name,F_name,M_name,T_name", SYSTEMS)
def test_newton_second_law(sysname, L_name, F_name, M_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    mass = 100 * sys.kg
    accel = 9.81 * sys.m / sys.s**2
    force = mass * accel
    expected = 981 * sys.N
    assert force == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("sysname,L_name,F_name,M_name,T_name", SYSTEMS)
def test_stress_force_over_area(sysname, L_name, F_name, M_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    force = 20 * sys.kgf
    area = 2 * sys.mm**2
    stress = force / area
    expected = 98.0665 * sys.MPa
    assert stress == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("sysname,L_name,F_name,M_name,T_name", SYSTEMS)
def test_every_unit_matches_absolute_si(sysname, L_name, F_name, M_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    bases = _bases(L_name, F_name, M_name, T_name)

    for dim_name, base_si in bases.items():
        for unit_name, abs_si in getattr(_f, dim_name).items():
            sys_val = getattr(sys, unit_name)
            expected = abs_si / base_si
            assert sys_val == pytest.approx(expected, rel=1e-12), (
                f"{sysname}.{unit_name}: got {sys_val}, expected {expected}"
            )

    for unit_name, abs_si in _f.ANGLE.items():
        assert getattr(sys, unit_name) == abs_si
    for unit_name, abs_si in _f.TEMPERATURE.items():
        assert getattr(sys, unit_name) == abs_si


# Per system: which named (pressure, energy, power) units happen to equal 1.0
# in that system. None means the natural derived base has no popular name in
# the factor table (e.g., barye, erg, kgf*m).
NATURAL_BASES = {
    "N_mm_s": ("MPa", "mJ", "mJ_s"),
    "N_m_s": ("Pa", "J", "W"),
    "kN_m_s": ("kPa", "kJ", "kW"),
    "kip_in_s": ("ksi", None, None),
    "kgf_m_s": (None, None, None),
    "dyne_cm_s": (None, None, None),
}


@pytest.mark.parametrize("sysname,L_name,F_name,M_name,T_name", SYSTEMS)
def test_natural_derived_bases_are_unity(sysname, L_name, F_name, M_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    p_name, e_name, w_name = NATURAL_BASES[sysname]
    if p_name:
        assert getattr(sys, p_name) == pytest.approx(1.0)
    if e_name:
        assert getattr(sys, e_name) == pytest.approx(1.0)
    if w_name:
        assert getattr(sys, w_name) == pytest.approx(1.0)
