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
# NOTE (18 Nov): at C = 1.0e-6 the emulator gives r = 4.51e-4, 0.8% below the frozen r edge 4.55e-4. The frozen band
# was made with N* 48.4-49.9; the emulator's fixed T_R gives N* ~ 50. Reported to Danny; not hidden by a looser test.
