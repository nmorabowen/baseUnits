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


def test_mks_equals_N_m_for_every_unit():
    """L-M-T and F-L-T paths must produce numerically identical systems."""
    import baseUnits._factors as _f
    import baseUnits.systems.mks as mks
    import baseUnits.systems.N_m as nm

    for dim in (
        "LENGTH",
        "FORCE",
        "MASS",
        "TIME",
        "PRESSURE",
        "ENERGY",
        "POWER",
        "DENSITY",
        "UNIT_WEIGHT",
        "ANGLE",
        "TEMPERATURE",
    ):
        for name in getattr(_f, dim):
            assert getattr(mks, name) == pytest.approx(getattr(nm, name), rel=1e-15), name


def test_kgf_m_weight_identity():
    """In gravitational kgf-m-s: 100 kg * g must equal exactly 100 kgf."""
    import baseUnits.systems.kgf_m as g

    assert g.kgf == 1.0
    assert g.BASE == "kgf-m-s"
    # The killer demo: a 100 kg mass weighs exactly 100 kgf.
    assert (100 * g.kg) * g.g == pytest.approx(100.0, rel=1e-12)
    # And kgf/cm^2 lands cleanly at 10_000 (kgf per m^2).
    assert g.kgf_cm2 == pytest.approx(1e4)


def test_cgs_force_base():
    """In CGS, the dyne is the natural force unit (M*L/T^2 with M=g, L=cm)."""
    import baseUnits.systems.cgs as cgs

    assert cgs.dyne == 1.0
    assert pytest.approx(1e5) == cgs.N  # 1 N = 1e5 dyne
    assert cgs.Pa == pytest.approx(10.0)  # 1 Pa = 10 baryes
    assert cgs.g == pytest.approx(980.665)  # standard gravity in cm/s^2
