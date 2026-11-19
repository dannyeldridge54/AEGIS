# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""SERAPIS calculator: exact mathematical values and internal consistency."""
from tools.serapis_calc import modular as J, eisenstein as EI, emulator as E, meter as M

def test_klein_j_special_values():                  # j(i) = 1728, j(rho) = 0, j(2i) = 66^3 (classical)
    assert abs(complex(J.j(1j)) - 1728) < 1e-6
    assert abs(complex(J.j(complex(0.5, 3**0.5/2)))) < 1e-6
    assert abs(complex(J.j(2j)) - 66**3) < 1e-4

def test_eisenstein_two_methods_agree():            # Fourier expansion vs direct lattice sum
    for x, y in ((0.0, 1.0), (0.5, 3**0.5/2), (0.2, 1.7)):
        a, b = float(EI.E_fourier(x, y, 2)), float(EI.E_lattice(x, y, 2))
        assert abs(a/b - 1) < 1e-5, (x, y)

def test_meter_inverts_emulator():                  # forward (C -> n_s) then inverse (n_s -> C) returns C within 3%
    for C in (1.05e-6, 1.25e-6, 1.5e-6):
        ns = E.emulate(C)['ns']; back = M.meter(ns)['C']
        assert abs(back/C - 1) < 0.03, (C, back)

def test_ns_inside_frozen_band():                   # D693 frozen n_s 0.970-0.975 across C 1.0-1.3e-6 (emulator at the leptogenesis T_R)
    for C in (1.0e-6, 1.15e-6, 1.3e-6):
        assert 0.970 <= E.emulate(C)['ns'] <= 0.975, C
# NOTE: at C = 1.0e-6 the emulator gives r = 4.51e-4, just below the frozen r floor 4.55e-4. Already recorded by the
# node audit (D1233/D1233a: the corrected N* puts C = 1.0e-6 below the r floor); the frozen band stays locked as made.

def test_j_series_exact_coefficients():   # Klein j = q^-1 + 744 + 196884 q + 21493760 q^2 + ... (moonshine layer, D1359)
    from tools.serapis_calc.jseries import coeffs
    c = coeffs(5)
    assert [c[k] for k in range(-1, 6)] == [1, 744, 196884, 21493760, 864299970, 20245856256, 333202640600]

def test_shape_functions_stationary_structure():   # P3 hunt (D1364): both E(U,2) and E1hat(U) — minimum at rho, saddle at i
    from tools.serapis_calc.shapes import E, E1hat, grad_hess, RHO, I
    assert abs(E(RHO) - 5.7833593) < 1e-6 and abs(E(I) - 6.0268120) < 1e-6
    for f in (E, E1hat):
        _, h = grad_hess(f, RHO); assert h[0]*h[2] - h[1]**2 > 0 and h[0] > 0
        _, h = grad_hess(f, I); assert h[0]*h[2] - h[1]**2 < 0
