"""D1940: split stacks — SU(3) on its own 4-cycle T3, SU(2)xU(1) on T2 (same flux 9S on both, so families stay 3).
alpha_a^-1(M_s) = Re f_a = Re T_a + 9 Re S. Unification is replaced by Re T3 - Re T2 = Delta (needed).
Three readings of the needed Delta(1/alpha_3) at the matching scale (one-loop invariance of differences):
 (r1) bare, gluino 4.93 TeV: 1/alpha_s(pred) - 1/0.1180 with alpha_s(pred) = 0.1142 (D1929 run 1)
 (r2) at the wino bound from the knob engine: alpha_s 0.11433 (D1937)
 (r3) with the post-selected Higgs-pair threshold (CONS): Delta3 = -0.094 (v4)
Each cycle stabilised by its own condensate (same rank N = 6, same W0): x_a = 2 pi Re T_a / N = ln(A_a/|W0|) + ln(1 + 2x/3)
 => d Re T = (N / 2 pi) d ln A  ⇒ the prefactor ratio A3/A2 needed. Natural if 1/3 <= A3/A2 <= 3 (A in [0.3, 3], D1811)."""
import json, math
reads = {'r1_bare_4p93TeV': 1 / 0.1180 - 1 / 0.1142, 'r2_wino_bound': 1 / 0.1180 - 1 / 0.11433, 'r3_higgs_pair_CONS': -0.094}
vals = sorted(reads.values()); centre = vals[1]; spread = vals[-1] - vals[0]
N = 6
ratio = {k: math.exp(v * 2 * math.pi / N) for k, v in reads.items()}
out = dict(dReT3_minus_ReT2_needed=reads, centre=centre, spread=spread, A3_over_A2=ratio,
           natural=all(1 / 3 <= r <= 3 for r in ratio.values()),
           wino_unchanged=True, note_wino='m3/2 is set by W0 and the overall volume; the split moves only Re T3 - Re T2, not m3/2 (orthogonal to the m3/2 line, D1939)',
           proton='no single GUT gauge group on split stacks ⇒ the G-branch X-boson proton decay (1.6e35 yr) no longer follows; proton becomes model-dependent (likely longer-lived)',
           label='FIT: one prefactor ratio A3/A2 is chosen to reproduce alpha_s; alpha_s stops being a prediction unless A3/A2 is derived (one-loop determinants)')
out['verdict'] = 'PASS (viable, natural)' if out['natural'] else 'FAIL (unnatural ratio)'
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1940_split_stacks.json', 'w'), indent=1)
