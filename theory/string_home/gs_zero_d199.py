"""D199: can delta_GS vanish on a Z3-type orbifold while keeping a condensing (asymptotically free) hidden group? AI-assisted.
Ibanez-Lust hep-th/9202046 eq. 3.6: b'^i_a = -C(G_a) + sum_R T(R)(1 + 2 n^i_R), and delta_GS^i = b'^i_a / k_a for every factor (no N=2 sectors).
Z3 modular weights: untwisted matter in plane j: n^i = -delta_ij (one copy per plane, 3 copies by Z3 symmetry);
twisted (no oscillator): n^i = -2/3 each plane; twisted with an oscillator in plane j: n^j = -5/3, others -2/3.
N=1 beta coefficient (same convention): b_a = -3 C + sum_R T(R) over all chiral fields; asymptotic freedom <=> b_a < 0."""
from fractions import Fraction as F
def per_plane(C, untw, tw, osc):
    # untw: sum of T(R) over untwisted reps counted ONCE (each appears in 3 planes); tw / osc: sums over twisted reps
    bprime = -C + untw * (-1 + 1 + 1) + tw * (1 + 2 * F(-2, 3)) + osc * ((1 + 2 * F(-5, 3)) + 2 * (1 + 2 * F(-2, 3))) / 3
    beta = -3 * C + 3 * untw + tw + osc
    return bprime, beta
print("check: hidden E8, no matter  ->", per_plane(30, 0, 0, 0), "(Ibanez-Lust: b' = -30)")
print("check: (2,2) E6: C=12, untw 27s: 3 per plane counted once -> sum T = 3 x 3 = 9 ... twisted 27 x 27 (T=3 each) = 81")
print("        ->", per_plane(12, 9, 81, 0), "(Ibanez-Lust: b'_E6 = -30)")
# general statement: b'^i = 0  =>  untw = C + tw/3 + osc(...)  =>  beta = 2 tw + (osc terms) >= 0
import itertools
viol = 0
for C, untw, tw, osc in itertools.product(range(1, 31), range(0, 40), range(0, 60, 3), range(0, 12, 3)):
    bp, beta = per_plane(C, untw, tw, osc)
    if bp == 0 and beta < 0: viol += 1
print("cases with b' = 0 AND asymptotic freedom (scanned C 1-30, matter sums up to 40/60/12):", viol)
