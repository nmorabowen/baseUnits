"""Default system (N-mm-tonne-s) primitives."""

import pytest

from baseUnits import BASE, MPa, N, cm, g, kg, kN, m, mm, s, tonne


def test_length_primitives():
    assert m == 1000.0
    assert mm == 1.0
    assert cm == 10.0


def test_mass_primitives():
    assert kg == 1e-3
    assert tonne == 1.0


def test_force_primitives():
    assert N == 1.0
    assert kN == 1e3


def test_pressure_primitive():
    assert MPa == 1.0


def test_time_primitive():
    assert s == 1.0


def test_base_label():
    assert BASE == "N-mm-tonne-s"


def test_gravity():
    assert g == pytest.approx(9806.65)
