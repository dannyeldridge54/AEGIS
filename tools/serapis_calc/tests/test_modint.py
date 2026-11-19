from tools.serapis_calc.modint import dkl, dkl_closed


def test_dkl_numeric_matches_closed_form():
    # S5a validation (2026-11-18): numeric modular integral = DKL closed form (3e-5 at full quadrature; light settings here)
    T, U = 2j, 1j
    assert abs(dkl(T, U, n1q=24, n2q=80) - dkl_closed(T, U)) < 5e-4
