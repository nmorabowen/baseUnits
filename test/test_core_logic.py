import pytest
from baseUnits import (
    m, cm, mm, ft,
    kg, gr,
    s,
    N, kgf,
    MPa,
    Dimension,
    minutes
)
from baseUnits.units import Unit

def test_dimension_equality_and_hash():
    """Tests that Dimension objects are equal and hashable (for dicts)."""
    dim_l1 = Dimension("Length")
    dim_l2 = Dimension("Length")
    dim_m = Dimension("Mass")
    
    assert dim_l1 == dim_l2
    assert dim_l1 != dim_m
    
    # Test hashability (we fixed this bug)
    dim_set = {dim_l1, dim_l2, dim_m}
    assert len(dim_set) == 2

def test_dimension_math():
    """Tests the __mul__, __truediv__, and __pow__ of Dimension."""
    dim_l = Dimension("Length")
    dim_m = Dimension("Mass")
    dim_t = Dimension("Time")
    
    dim_force = dim_m * dim_l / (dim_t**2)
    assert dim_force == Dimension({"Mass": 1, "Length": 1, "Time": -2})
    
    dim_pressure = dim_force / (dim_l**2)
    assert dim_pressure == Dimension({"Mass": 1, "Length": -1, "Time": -2})

def test_quantity_creation():
    """Tests basic Quantity creation."""
    q = 10.5 * m
    assert q.value == 10.5
    assert q.unit == m
    assert q.base_value == 10500.0 # 10.5 * 1000 mm

def test_quantity_addition_and_subtraction():
    """Tests that quantities add and subtract correctly."""
    q1 = 1 * m
    q2 = 50 * cm
    
    res_add = q1 + q2
    assert res_add.value == 1.5 # 1m + 0.5m = 1.5m
    assert res_add.unit == m
    
    res_sub = q1 - q2
    assert res_sub.value == 0.5 # 1m - 0.5m = 0.5m
    assert res_sub.unit == m

def test_quantity_dimensional_safety():
    """Tests that incompatible arithmetic raises TypeError."""
    with pytest.raises(TypeError, match="Cannot add"):
        _ = 10 * m + 5 * kg
        
    with pytest.raises(TypeError, match="Cannot subtract"):
        _ = 1 * N - 1 * s

def test_quantity_to_conversion():
    """Tests the .to() method."""
    q = 10 * m
    assert q.to(mm).value == pytest.approx(10000.0)
    assert q.to(ft).value == pytest.approx(32.8084)

def test_quantity_to_base_conversion():
    """Tests the .to_base() convenience method."""
    # Simple dimension
    q_len = 1 * ft
    q_base_len = q_len.to_base()
    assert q_base_len.unit == mm
    assert q_base_len.value == pytest.approx(304.8)
    
    # Compound dimension
    q_force = 2 * kgf
    q_base_force = q_force.to_base()
    assert q_base_force.unit == N
    assert q_base_force.value == pytest.approx(19.614)

def test_mixed_type_arithmetic():
    """Tests operations from our debugging (e.g., Quantity / Unit)."""
    # Test: g = 9.81 * m / s**2
    g_val = 9.81 * m / s**2
    assert g_val.value == 9.81
    assert g_val.unit.symbol == "(m/(s**2))"
    
    # Test: (10 * m) * mm
    area = (10 * m) * mm
    assert area.value == 10.0
    assert area.unit.symbol == "(m*mm)"