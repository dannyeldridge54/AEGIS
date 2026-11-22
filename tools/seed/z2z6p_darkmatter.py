#!/usr/bin/env python3
"""D2126: centre parities and electric charges of all states (Tables 28/29) after PS->SM; axion misalignment estimate."""
import json, math
from fractions import Fraction as Fr
# states: (label, multiplicity, reps{stack: 'f'|'af'|'adj'|'sym'|'anti'}, chiral?)
ST = [('ab',1,{'a':'f','b':'af'},1),("ab'",2,{'a':'f','b':'f'},1),('ac',1,{'a':'af','c':'f'},1),("ac'",2,{'a':'af','c':'af'},1),('bc',1,{'b':'f','c':'af'},1),
      ('bd',1,{'b':'f','d':'af'},1),("bd'",3,{'b':'af','d':'af'},1),("be'",1,{'b':'af','e':'af'},1),('cd',1,{'c':'af','d':'f'},1),("cd'",3,{'c':'f','d':'f'},1),("ce'",1,{'c':'f','e':'f'},1),
      ('dd(adj)',4,{'d':'adj'},0),("dd'(sym)",2,{'d':'sym'},0),("dd'(anti)",2,{'d':'anti'},0),("ee'(sym)",1,{'e':'sym'},0),("ee'(anti)",1,{'e':'anti'},0),
      ('ad',2,{'a':'f','d':'af'},0),("de'",1,{'d':'f','e':'f'},0)]
nidx = {'f':1,'af':1,'adj':2,'sym':2,'anti':2}
def su4_comps(rep):   # list of (colour?, B-L)
    s = 1 if rep == 'f' else -1
    return [('quark', s*Fr(1,3))]*3 + [('lepton', s*Fr(-1))] if rep in ('f','af') else []
def su2_T3(rep): return [Fr(1,2), Fr(-1,2)] if rep in ('f','af') else ([Fr(1), Fr(0), Fr(-1)] if rep in ('adj','sym') else [Fr(0)])
out = []
for lab, mult, reps, chi in ST:
    odd_d = nidx.get(reps.get('d'), 0) % 2 == 1; odd_e = nidx.get(reps.get('e'), 0) % 2 == 1
    BL = su4_comps(reps['a']) if 'a' in reps else [('none', Fr(0))]
    T3L = su2_T3(reps['b']) if 'b' in reps else [Fr(0)]
    T3R = su2_T3(reps['c']) if 'c' in reps else [Fr(0)]
    Qs = sorted({t3l + t3r + bl/2 for (_, bl) in BL for t3l in T3L for t3r in T3R})
    colour = any(c == 'quark' for c, _ in BL)
    frac = any(q.denominator != 1 for q in Qs)
    out.append(dict(state=lab, mult=mult, chiral=bool(chi), odd_d=odd_d, odd_e=odd_e, coloured=colour, charges=[str(q) for q in Qs], fractional=frac))
stable_odd = [o for o in out if o['odd_d'] or o['odd_e']]
frac_odd = [o['state'] for o in stable_odd if o['fractional']]
neutral_odd = [o['state'] for o in stable_odd if not o['fractional'] and set(o['charges']) == {'0'}]
ax = {('f_a=%.0e' % fa): math.sqrt(1/((fa/9e11)**1.165)) for fa in (1e12, 8e12)}
R = dict(states=out, centre_odd=[o['state'] for o in stable_odd], centre_odd_fractional=frac_odd, centre_odd_neutral_only=neutral_odd,
         axion_theta_required=ax, ITEM18='OBSTRUCTED (stable fractional charges, no mass mechanism)' if frac_odd else 'CONDITIONAL')
print(json.dumps(R, indent=1))
