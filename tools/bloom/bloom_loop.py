#!/usr/bin/env python3
"""Bloom Loom loop (D2032): data mining + triangulation + balance, run until the Centre is balanced and the mining queue is empty.
Each tick:  (1) TRIANGULATE every term from its 'sources' (Rule 6h: 3 sources, consensus within 1 sigma, never average away a conflict)
            (2) QUEUE the next mining target: fewest sources first, then largest pull (the term whose data matter most)
            (3) BALANCE the levers with the Centre (loomcore) and report bits.
Web mining itself is done by the agent (the shell has no web); this script decides WHAT to mine next and scores it."""
import json, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloom
def circ(a, b): d = (a - b + 180) % 360 - 180; return d
def triangulate(t):
    src = [s for s in t.get('sources', []) if s.get('sigma')]
    out = {'n_sources': len(t.get('sources', [])), 'gaussian_sources': len(src)}
    if len(src) >= 2:
        angle = t['id'] == 'delta_CP'; worst = 0.0
        for i in range(len(src)):
            for j in range(i + 1, len(src)):
                dv = circ(src[i]['value'], src[j]['value']) if angle else src[i]['value'] - src[j]['value']
                worst = max(worst, abs(dv) / math.hypot(src[i]['sigma'], src[j]['sigma']))
        out['worst_pair_sigma'] = round(worst, 2); out['consensus'] = worst <= 1.0
        out['z_ours_per_source'] = [round((circ(t['ours'], s['value']) if angle else t['ours'] - s['value']) / s['sigma'], 2) for s in src]
    out['status'] = 'DONE' if out['n_sources'] >= 3 and out.get('consensus', True) else ('CONFLICT->shadow' if out.get('consensus') is False else 'MINE')
    return out
def tick():
    D = bloom.D; tri = {t['id']: triangulate(t) for t in D['terms']}
    pull = {t['id']: abs(bloom.lnL_term(t)[1]) for t in D['terms']}
    queue = sorted([k for k, v in tri.items() if v['status'] != 'DONE'], key=lambda k: (tri[k]['n_sources'], -pull[k]))
    bal = bloom.balance({'lnm32': 1.0})
    return {'triangulation': tri, 'mining_queue': queue, 'balance': {k: bal[k] for k in ('knobs', 'state', 'bits')}}
if __name__ == '__main__':
    r = tick()
    for k, v in r['triangulation'].items(): print('  %-12s %s' % (k, v))
    print('MINING QUEUE (next first):', r['mining_queue']); print('BALANCE:', r['balance'])
