from tools.serapis_calc.modint import dkl, dkl_closed


def test_dkl_numeric_matches_closed_form():
    # S5a validation (2026-11-18): numeric modular integral = DKL closed form (3e-5 at full quadrature; light settings here)
    T, U = 2j, 1j
    assert abs(dkl(T, U, n1q=24, n2q=80) - dkl_closed(T, U)) < 5e-4


def test_rankin_selberg_product():
    # S5b: ∫_F (d²τ/τ₂)(Γ₂,₂ − 1)E(τ,2) = π⁻²E(T,2)E(U,2) − c(2) on a torus not used to fit c
    from tools.serapis_calc.modint import rs_numeric, rs_closed
    T, U = complex(0.1, 2.5), complex(0.5, 1.5)
    assert abs(rs_numeric(T, U, 2.0, n1q=20, n2q=160) - rs_closed(T, U, 2.0)) < 2e-3
