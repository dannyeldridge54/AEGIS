"""D2146 positive control: Gmeiner-Honecker 0708.2285 SM example (Table 13, ABa)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
S = {'a': (3, [0, 0, 1, -1, 0, 1, -1, 0, 0, 1, -1, 0]), 'b': (2, [3, 0, 3, 0, -3, 0, -3, 0, 0, 0, 0, 0]),
     'c': (1, [1, 1, 0, 0, 0, 0, 3, -3, 0, 0, -3, 3]), 'd': (1, [0, 0, 3, -3, 0, -1, 1, 0, 0, -1, 1, 0]),
     'e': (1, [0, 0, 3, -3, 3, 0, 0, 3, -3, 0, 0, -3])}
tp = Z.tadpole(S.values(), Z.image_ABa, Z.O6_ABa)
ch = Z.chiral(S, Z.image_ABa, Z.O6_ABa)
pub = {('a','Anti'):0,('a','Sym'):0,('a','b'):0,('a','c'):-3,('a','d'):0,('a','e'):0,("a","b'"):3,("a","c'"):-3,("a","d'"):0,("a","e'"):0,
       ('b','c'):-9,('b','d'):6,('b','e'):0,("b","c'"):-9,("b","d'"):3,("b","e'"):0,('c','d'):-3,('c','e'):0,("c","d'"):3,("c","e'"):0,
       ('d','e'):0,("d","e'"):0}
for x in 'bcde': pub[(x,'Anti')] = 0; pub[(x,'Sym')] = 0
mism = {str(k): (ch.get(k), v) for k, v in pub.items() if ch.get(k) != v}
res = dict(tadpole_residual=tp.tolist(), tadpoles_ok=bool(abs(tp).max() < 1e-9), mismatches=mism, PASS=bool(abs(tp).max() < 1e-9 and not mism))
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(os.path.dirname(__file__), 'z6p_control.json'), 'w'), indent=1)
