"""The one consistency rule.

Every consistent unit system in this library must satisfy Newton's second
law without spurious factors. This file is the single canonical place
where that invariant is enforced, parametrized over every system.

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

SYSTEMS = [
    # (module name, length name, force name, time name)
    ("N_mm", "mm", "N", "s"),
    ("N_m", "m", "N", "s"),
    ("kN_m", "m", "kN", "s"),
    ("kip_in", "inches", "kip", "s"),
    # `mks` is built via the L-M-T path; numerically identical to N_m.
    ("mks", "m", "N", "s"),
    # `cgs` derives force from mass; force comes out as dyne.
    ("cgs", "cm", "dyne", "s"),
    # `kgf_m` — gravitational/engineering metric. Mass derived (hyl, no name).
    ("kgf_m", "m", "kgf", "s"),
]


@pytest.mark.parametrize("sysname,L_name,F_name,T_name", SYSTEMS)
def test_newton_second_law(sysname, L_name, F_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    mass = 100 * sys.kg
    accel = 9.81 * sys.m / sys.s**2
    force = mass * accel
    expected = 981 * sys.N
    assert force == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("sysname,L_name,F_name,T_name", SYSTEMS)
def test_stress_force_over_area(sysname, L_name, F_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    force = 20 * sys.kgf
    area = 2 * sys.mm**2
    stress = force / area
    expected = 98.0665 * sys.MPa
    assert stress == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("sysname,L_name,F_name,T_name", SYSTEMS)
def test_every_unit_matches_absolute_si(sysname, L_name, F_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    L = _f.LENGTH[L_name]
    F = _f.FORCE[F_name]
    T = _f.TIME[T_name]
    M = F * T**2 / L
    P = F / L**2
    E = F * L
    Pw = E / T
    D = M / L**3
    UW = F / L**3

    bases = [
        ("LENGTH", L),
        ("FORCE", F),
        ("MASS", M),
        ("TIME", T),
        ("PRESSURE", P),
        ("ENERGY", E),
        ("POWER", Pw),
        ("DENSITY", D),
        ("UNIT_WEIGHT", UW),
    ]
    for dim_name, base_si in bases:
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


NATURAL_BASES = {
    ("N", "mm"): ("MPa", "mJ", "mJ_s"),
    ("N", "m"): ("Pa", "J", "W"),
    ("kN", "m"): ("kPa", "kJ", "kW"),
    ("kip", "inches"): ("ksi", None, None),
    # cgs natural derived bases (barye, erg, erg/s) are not in the factor table.
    ("dyne", "cm"): (None, None, None),
    # kgf-m natural pressure (kgf/m^2) and energy (kgf*m) are not named units.
    ("kgf", "m"): (None, None, None),
}


@pytest.mark.parametrize("sysname,L_name,F_name,T_name", SYSTEMS)
def test_natural_derived_bases_are_unity(sysname, L_name, F_name, T_name):
    sys = importlib.import_module(f"baseUnits.systems.{sysname}")
    p_name, e_name, w_name = NATURAL_BASES[(F_name, L_name)]
    if p_name:
        assert getattr(sys, p_name) == pytest.approx(1.0)
    if e_name:
        assert getattr(sys, e_name) == pytest.approx(1.0)
    if w_name:
        assert getattr(sys, w_name) == pytest.approx(1.0)
