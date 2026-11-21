"""D1938: S–T seam test. Can the supergravity-fixed (Kaplunovsky–Louis / Conlon–Palti 0901.4350) S–T threshold supply Delta3 = +0.044?
Delta3 = alpha3^-1(M12) - alpha12^-1(M12) at the alpha1 = alpha2 crossing (one-loop bookkeeping, as in D1880).
A GAUGE-UNIVERSAL shift d (same for every group) cancels in Delta3 exactly; only the NON-universal part counts."""
import json, math
V, gs = 4.0e4, 2 / math.sqrt(3)
# reading (a): Conlon–Palti untwisted D3–D7 running, gauge-group universal (their Eq. 194/231): coefficient b_untw for every group
b_untw = 1.0                                   # any value: universal
shift_a = [b_untw * math.log(V) / (24 * math.pi ** 2)] * 3
# reading (b): the dilaton shift CP needed to match KL, Re S -> Re S - (2/9)(1/16pi^2) n7 ln V, enters f_a = T + 9S for the visible stack:
# gauge-universal for SU(3) x SU(2) x U(1) living on ONE stack (all three share f_vis)
dS = -(2 / 9) / (16 * math.pi ** 2) * 1.0 * math.log(V)
shift_b = [9 * dS] * 3
# reading (c): M_X raised to (M_P/M_s)^{1/3} M_s: a universal log shift of the matching scale; at one loop Delta3 at the crossing is unchanged
shift_c = [0.0] * 3
def d3_change(sh): return sh[2] - sh[0]        # Delta3 changes only by the non-universal difference (a3 vs a1 = a2 at crossing)
reads = [d3_change(s) for s in (shift_a, shift_b, shift_c)]
need = 0.044
out = dict(readings_dDelta3=reads, centre=sorted(reads)[1], need=need,
           verdict='PASS' if all(0.5 * need <= r <= 1.5 * need for r in reads) else 'FAIL',
           note='every supergravity-fixed S–T seam term on a single visible stack is gauge-universal and cancels in Delta3; the needed +0.044 must be NON-universal (new states / twisted-sector Delta b / split stacks) and is not supplied by the parent-equation form')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1938_seam.json', 'w'), indent=1)
