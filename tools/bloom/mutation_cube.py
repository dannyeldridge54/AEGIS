#!/usr/bin/env python3
"""The mutation cube (D2038, Danny 01:50-01:51): the UFE's six open structural choices as a 6-D hypercube (2^6 = 64 corners),
with the OBSERVATION POINT (the data) at the centre. Each corner = one mutated UFE. Its distance from the centre = its Bloom
description length in bits (data misfit + knob cost), plus a filter count. Unknowns are never filled in: a corner whose seam value
is not derived is marked OPEN and ranked only on what is known. Run: python3 mutation_cube.py"""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import bloom
AXES = [('M', 'gaugino mediation', ('pure-AMSB', 'mirage')),
        ('V', 'visible branes', ('D7 on KKLT cycle', 'sequestered D3 (LVS)')),
        ('I', 'inflation vs m3/2', ('coupled', 'decoupled sector')),
        ('K', 'Kahler stabilisation', ('KKLT non-perturbative', 'flux-scaling')),
        ('T', 'S-T seam term', ('none', 'derived threshold')),
        ('U', 'U3 value', ('i', '2i'))]
NEW_KNOBS = {'V': 1, 'I': 2, 'K': 1, 'T': 0, 'U': 0, 'M': 0}      # extra fitted knobs each mutation brings (estimate, D2037 fix menu)
ALPHA = {'pure-AMSB': 0.1142, 'mirage': 0.1086}                    # D2036/D2037 (mirage midpoint of 0.1077-0.1095)
def corner(c):
    s = dict(zip([a[0] for a in AXES], c)); flags, open_ = [], []
    sequestered = s['V'] == 1 or s['K'] == 1                        # F^T_vis suppressed only off the KKLT-stabilised D7 cycle
    if s['M'] == 0 and not sequestered: flags.append('pure-AMSB contradicts F^T_vis (D2036 M)')
    if s['M'] == 1 and sequestered: flags.append('mirage needs F^T_vis; this corner suppresses it')
    if not (s['I'] == 1 or s['K'] == 1): flags.append('Kallosh-Linde: H_inf >> barrier (D2036 K, D2037 B0b)')
    if s['U'] == 1: flags.append('U3 = 2i breaks neutrinos at i (D2022)')
    if s['K'] == 1: flags.append('flux-scaling: m32 shares the moduli flux scaling (>= H_inf), so the AMSB wino >> TeV (D2041, 1503.07634)')
    if s['V'] == 1 and s['M'] == 0: open_.append('pure AMSB on sequestered D3 needs a warped-throat tip (LVS no-scale may kill AMSB at our m32, D2040)')
    if s['V'] == 1: open_.append('f_vis = S only: the whole gauge chain must be re-derived')
    if s['T'] == 1: open_.append('seam value not yet derived (B4)')
    if s['I'] == 1: open_.append('no realistic decoupled-inflation construction exists: HKW toy is ruled out; embedding is an unmet challenge (D2042, 1003.4265)')
    if s['K'] == 1: open_.append('no condensate: the W0 = A e^-x(1+2x/3) selection of N = 6 is lost and must be re-derived')
    if s['M'] == 1: open_.append('bino LSP 3.5-8 TeV overcloses unless RPV/dilution')
    terms = [dict(t, ours=ALPHA[AXES[0][2][s['M']]]) if t['id'] == 'alpha_s' else t for t in bloom.D['terms']]
    if s['M'] == 1: terms = [dict(t, ours=11.4, kind='lower', bound=0.670) if t['id'] == 'wino' else t for t in terms]   # mirage wino ~10.8-12.1 TeV: only the LHC lower bound applies (the 0.70 top edge was a pure-AMSB relic bar)
    kfit = sum(f['n'] for f in bloom.D['fitted_knobs']) + sum(NEW_KNOBS[k] for k, v in s.items() if v)
    lnL, tgt, N, k = bloom.target(terms, kfit); bits = -tgt / math.log(2)
    return {'corner': ''.join(str(v) for v in c), 'choice': {a[0]: a[2][v] for a, v in zip(AXES, c)}, 'bits_known': round(bits, 1),
            'k_fit': k, 'filters_failed': flags, 'open': open_}
if __name__ == '__main__':
    R = [corner(c) for c in itertools.product((0, 1), repeat=6)]
    R.sort(key=lambda r: (len(r['filters_failed']), len(r['open']), r['bits_known']))
    print('MUTATION CUBE: 64 corners, centre = the observation point. Distance = (filters failed, open items, bits). v4 as written = corner 000000.')
    v4 = [r for r in R if r['corner'] == '000000'][0]; print('v4 (000000): bits %.1f, filters %d %s' % (v4['bits_known'], len(v4['filters_failed']), v4['filters_failed']))
    for r in R[:10]: print('%s bits %5.1f k %2d | fail %d open %d | %s | %s' % (r['corner'], r['bits_known'], r['k_fit'], len(r['filters_failed']), len(r['open']), r['choice'], r['open']))
    json.dump(R, open(os.path.join(HERE, 'mutation_cube.json'), 'w'), indent=1)
