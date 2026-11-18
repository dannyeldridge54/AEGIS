# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Lattice Lab against published values (Conway & Sloane, SPLAG; OEIS)."""
import math, numpy as np
from tools.lattice import lattice_lab as LL

KISSING = {'D4': 24, 'E6': 72, 'E7': 126, 'E8': 240}          # SPLAG Table 1.2
DET = {'D4': 4, 'E6': 3, 'E7': 2, 'E8': 1}                     # SPLAG ch. 4

def test_determinants():
    for L, d in DET.items(): assert abs(np.linalg.det(LL.gram(L)) - d) < 1e-9, L

def test_kissing_numbers():
    for L, k in KISSING.items():
        mv = LL.minvecs(LL.gram(L)); mv = mv[0] if isinstance(mv, tuple) else mv
        assert len(mv) == k, (L, len(mv))

def test_e8_theta_is_E4():                                       # theta_E8 = E4 = 1 + 240 sum sigma3(n) q^n (OEIS A004009)
    r = LL.modular('E8'); assert r['match'] and r['shells'][:4] == [1, 240, 2160, 6720]

def test_hexagonal_planes_e8():
    assert LL.hexagons('E8')['hexagonal_planes'] == 1120

def test_epstein_a2_closed_form():                               # Z_A2(2) = 6 zeta(2) L(2, chi_-3) for x^2+xy+y^2; unit area scales by (sqrt3/2)^2
    L2 = 0.7813024128964862                                      # L(2, chi_-3), OEIS A086724
    want = 0.75 * 6 * (math.pi**2 / 6) * L2
    assert abs(LL.epstein('A2', 2)['epstein'] - want) < 1e-7
