"""Same physical quantity expressed in each system."""

import pytest


def test_five_meters_across_systems():
    import baseUnits.systems.kip_in as s_kipin
    import baseUnits.systems.N_m as s_Nm
    import baseUnits.systems.N_mm as s_Nmm

    assert 5 * s_Nmm.m == 5000.0
    assert 5 * s_Nm.m == 5.0
    assert 5 * s_kipin.m == pytest.approx(196.85, rel=1e-4)


def test_one_kn_across_systems():
    import baseUnits.systems.kN_m as s_kNm
    import baseUnits.systems.N_m as s_Nm
    import baseUnits.systems.N_mm as s_Nmm

    assert 1 * s_Nmm.kN == 1000.0
    assert 1 * s_Nm.kN == 1000.0
    assert 1 * s_kNm.kN == 1.0
