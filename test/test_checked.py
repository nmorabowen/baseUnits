"""Smoke test for the opt-in checked layer."""

import pytest


def test_checked_imports():
    from baseUnits.checked import C, F, K, MPa, N, Quantity, kg, m

    assert Quantity is not None
    assert m is not None
    assert K is not None


def test_quantity_arithmetic():
    from baseUnits.checked import m, mm

    q = 5 * m
    assert q.value == 5.0
    converted = q.to(mm)
    assert converted.value == pytest.approx(5000.0)


def test_quantity_addition():
    from baseUnits.checked import m, mm

    q = (1 * m) + (500 * mm)
    assert q.to(mm).value == pytest.approx(1500.0)


def test_kelvin_bug_fixed():
    from baseUnits.checked import C, K

    q = (1 * K).to(C)
    assert q.value == pytest.approx(1.0)


def test_fahrenheit_delta():
    from baseUnits.checked import F, K

    q = (1 * F).to(K)
    assert q.value == pytest.approx(5.0 / 9.0)
