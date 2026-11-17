import sys, math; sys.path.insert(0, 'tools/janus_astro')
import bbn_net as B, serapis_inputs as SI
sY = math.hypot(0.0013, 0.0002); sD = math.hypot(0.028, 0.083)
base = B.abundances(SI.OMBH2, 0.0, 1.0); out = []
for lab, init, tgt in (('base', 0.0, 0.0), ('U(1)', 0.2069, 0.054), ('SU(2)', 0.6169, 0.161), ('SU(2)+gaugino', 1.1533, 0.301)):
    a = B.abundances(SI.OMBH2, init, 1.0); dN = a['Neff_final'] - base['Neff_final']
    pY = (a['Yp_mass'] - 0.2458)/sY; pD = (a['DH']*(1e5 if a['DH'] < 1e-3 else 1) - 2.513)/sD
    m = max(abs(pY), abs(pD)); v = 'OK' if m < 2 else ('TENSION' if m <= 3 else 'EXCLUDED')
    out.append(f"{lab}: dN_final={dN:.4f} (B7 {tgt}, {'ok' if abs(dN-tgt) <= 0.003 else 'MISMATCH'}) Yp={a['Yp_mass']:.5f} pull {pY:+.2f}; 1e5DH={a['DH']*(1e5 if a['DH'] < 1e-3 else 1):.4f} pull {pD:+.2f} -> {v} | EMPRESS Yp pull {(a['Yp_mass']-0.2402)/0.0040:+.2f}")
open('field_tests/results/b8_lbt.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
