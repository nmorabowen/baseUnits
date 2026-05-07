"""Spot-check conversion ratios across systems."""

import math

import pytest


def test_kn_to_lbf_default():
    from baseUnits import kN, lbf

    assert (100 * kN) / lbf == pytest.approx(22480.89, rel=1e-5)


def test_ft_to_mm_default():
    from baseUnits import ft, mm

    assert (1 * ft) / mm == pytest.approx(304.8)


def test_mpa_to_ksi_default():
    from baseUnits import MPa, ksi

    assert (1 * MPa) / ksi == pytest.approx(0.14504, rel=1e-4)


def test_degree_to_radian():
    from baseUnits import degree

    assert (180 * degree) == pytest.approx(math.pi)


def test_kip_in_s_pressure_self_consistent():
    from baseUnits.systems.kip_in_s import MPa, ksi

    assert (1 * ksi) / MPa == pytest.approx(6.894757, rel=1e-5)


def test_N_m_s_pressure_natural():
    from baseUnits.systems.N_m_s import Pa

    assert Pa == pytest.approx(1.0)
