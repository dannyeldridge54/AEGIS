"""PREREG_B5_MBB: m_bb band for normal ordering, m1 = 0 (one free Majorana phase)."""
import math, json
DM21, DM31, S13 = 7.49e-5, 2.513e-3, 0.02195
m2, m3 = math.sqrt(DM21), math.sqrt(DM31)
def band(s12):
    a = m2 * s12 * (1 - S13); b = m3 * S13
    return abs(a - b), a + b
out = {'sum_mnu_eV': m2 + m3, 'm2_eV': m2, 'm3_eV': m3}
for name, s12 in (('TM1 (Weave P)', (1 - 3 * S13) / (3 * (1 - S13))), ('measured 0.307', 0.307)):
    lo, hi = band(s12); out[name] = dict(s12=s12, mbb_min_meV=lo * 1e3, mbb_max_meV=hi * 1e3)
out['fail_threshold_meV'] = 2 * out['TM1 (Weave P)']['mbb_max_meV']
print(json.dumps(out, indent=1))
