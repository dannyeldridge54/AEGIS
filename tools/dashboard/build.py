# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""U3: build tools/dashboard/data.json for the toolkit dashboard (index.html). Every number is computed now by the
validated toolkit functions; nothing is typed in by hand. Run: python3 -m tools.dashboard.build"""
import json, os
from tools.prov_block import provenance
from tools.janus_calc import settings as J
from tools.janus_astro import settings as H
from tools.lhc import settings as C
from tools import nested_guard as G
HERE = os.path.dirname(os.path.abspath(__file__))
def main():
    janus = [dict(model=m, **{k: J.predict(m, 55)[k] for k in ('ns', 'r', 'Nstar')}, scores=J.score(J.predict(m, 55)))
             for m in ('serapis_10d', 'serapis_6d', 'weave_10d', 'starobinsky', 'alpha_1_3', 'phi2')]
    consts = {q: {k: dict(value=v[0], sigma=v[1], kind=v[2], source=v[3]) for k, v in d.items()} for q, d in J.CONSTRAINTS.items()}
    b = H.bbn(theory='PRIMAT'); ns = [H.neutron_star(e) for e in H.EOS]
    reach = [C.reach(r) for r in ('run2', 'run3', 'hl-lhc', 'hl-lhc-ult')]
    d1713 = {'Pantheon+': {'lcdm': 2432.76, 'thread': 2430.14, 'coupled': 2432.28},
             'DES-Y5': {'lcdm': 2676.47, 'thread': 2668.33, 'coupled': 2667.44},
             'Union3': {'lcdm': 1055.14, 'thread': 1051.76, 'coupled': 1052.44}}   # D1725 (PC results, locked run)
    nest = [('lcdm', 'thread'), ('thread', 'coupled')]
    planck = [dict(set=k, d_thread=v['thread'] - v['lcdm'], d_coupled=v['coupled'] - v['lcdm'], guard=G.report(v, nest)) for k, v in d1713.items()]
    out = dict(provenance=provenance('AEGIS dashboard', {'Nstar': 55}, H.sources(), ['D1725', 'J3b', 'D1191']),
               janus=janus, constraints=consts, hyperion=dict(bbn=b, neutron_stars=ns), cern=dict(reach=reach), planck=planck)
    json.dump(out, open(os.path.join(HERE, 'data.json'), 'w', encoding='utf-8'), indent=1, default=float); print('wrote data.json')
    from tools.evidence import atlas          # Evidence Atlas (PREREG_EVIDENCE_ATLAS) for the Evidence section
    atlas.build(HERE); print('wrote atlas.json')
if __name__ == '__main__': main()
