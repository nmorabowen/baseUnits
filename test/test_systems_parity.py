"""Same physical quantity expressed in each system."""

import pytest


def test_five_meters_across_systems():
    import baseUnits.systems.kip_in_s as s_kipin
    import baseUnits.systems.N_m_s as s_Nm
    import baseUnits.systems.N_mm_s as s_Nmm

    assert 5 * s_Nmm.m == 5000.0
    assert 5 * s_Nm.m == 5.0
    assert 5 * s_kipin.m == pytest.approx(196.85, rel=1e-4)


def test_one_kn_across_systems():
    import baseUnits.systems.kN_m_s as s_kNm
    import baseUnits.systems.N_m_s as s_Nm
    import baseUnits.systems.N_mm_s as s_Nmm

    assert 1 * s_Nmm.kN == 1000.0
    assert 1 * s_Nm.kN == 1000.0
    assert 1 * s_kNm.kN == 1.0


def test_kgf_m_s_weight_identity():
    """In gravitational kgf-m-s: 100 kg * g must equal exactly 100 kgf."""
    import baseUnits.systems.kgf_m_s as g

    assert g.kgf == 1.0
    assert g.BASE == "kgf-m-s"
    # The killer demo: a 100 kg mass weighs exactly 100 kgf.
    assert (100 * g.kg) * g.g == pytest.approx(100.0, rel=1e-12)
    # And kgf/cm^2 lands cleanly at 10_000 (kgf per m^2).
    assert g.kgf_cm2 == pytest.approx(1e4)


def test_tf_m_s_force_base():
    """In tonne-force tf-m-s: tf is the force base and 1 tf = 1000 kgf."""
    import baseUnits.systems.tf_m_s as t

    assert t.tf == 1.0
    assert t.BASE == "tf-m-s"
    assert t.kgf == pytest.approx(1e-3)  # 1 tf = 1000 kgf
    # 1 kgf/cm^2 = 10 tf/m^2 (the natural, unnamed pressure base).
    assert t.kgf_cm2 == pytest.approx(10.0)
    # Consistent system: standard gravity is unchanged.
    assert t.g == pytest.approx(9.80665)


def test_dyne_cm_s_force_base():
    """In CGS, the dyne is the natural force unit (M*L/T^2 with M=g, L=cm)."""
    import baseUnits.systems.dyne_cm_s as cgs

    assert cgs.dyne == 1.0
    assert pytest.approx(1e5) == cgs.N  # 1 N = 1e5 dyne
    assert cgs.Pa == pytest.approx(10.0)  # 1 Pa = 10 baryes
    assert cgs.g == pytest.approx(980.665)  # standard gravity in cm/s^2


def test_factory_validates_overspecified_system():
    """Passing both force and mass: factory must verify F = M*L/T^2."""
    from baseUnits._make_system import make_system

    # Consistent: should succeed.
    sys = make_system(length="mm", force="N", mass="tonne", time="s")
    assert sys.BASE == "N-mm-tonne-s"

    # Inconsistent: kg with N at length=mm gives derived M=tonne, not kg.
    with pytest.raises(ValueError, match="Inconsistent system"):
        make_system(length="mm", force="N", mass="kg", time="s")


def test_factory_requires_force_or_mass():
    from baseUnits._make_system import make_system

    with pytest.raises(ValueError, match="at least one"):
        make_system(length="m", time="s")
