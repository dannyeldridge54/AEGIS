#!/usr/bin/env python3
"""One Loom engine for both directions (D2027). Every domain reports one number, its DESCRIPTION LENGTH in bits (MDL, Rissanen; Grunwald math/0406077):
  inward  (the Forge):  bits = 8 * compressed bytes                       (an online prequential code, Blier & Ollivier 1802.07044)
  outward (the Bloom):  bits = -lnL/ln2 + (k/2) log2 N                     (two-part code: data given theory + theory's fitted knobs; BIC ~ MDL)
The same Centre (loomcore) tunes either: a knob is kept only if it shortens the total description on held-out data.
A domain is any object with: name, knobs (dict, <= 9 per agent), bits(settings, split) -> float."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'bloom'))
from loomcore import Agent, Centre

class BloomDomain:
    """Outward build: theory -> data. Knobs are theory values exposed for a what-if (each free knob costs 0.5 log2 N bits)."""
    name = 'bloom'
    steps = ((1.1, 0.9), (1.03, 0.97), (1.01, 0.99), (1.003, 0.997))   # a theory value moves in fine steps; octaves are for Forge knobs
    def __init__(self, free=('alpha_s',)):
        import bloom; self.b = bloom; self.free = free; self.knobs = {f: 1.0 for f in free}   # multiplicative pokes on 'ours'
    def bits(self, s, split='tune'):
        terms = [dict(t, ours=t['ours'] * s.get(t['id'], 1.0)) for t in self.b.D['terms']]
        kfit = sum(f['n'] for f in self.b.D['fitted_knobs']); moved = sum(1 for k in self.free if abs(s.get(k, 1.0) - 1.0) > 1e-12)
        lnL, tgt, N, k = self.b.target(terms, kfit, moved); return -tgt / math.log(2)

class ForgeDomain:
    """Inward build: data -> code. Calls a loomz build; held-out split = a different slice. (The Forge is paused: not run by default.)"""
    name = 'forge'
    def __init__(self, binary, slices, env, knobs):
        self.binary, self.slices, self.env, self.knobs = binary, slices, env, dict(knobs)
    def bits(self, s, split='tune'):
        e = dict(os.environ, **self.env, **{k: str(v) for k, v in s.items()}); out = self.slices[split] + '.lz'
        r = subprocess.run([self.binary, 'c', self.slices[split], out], env=e, capture_output=True, text=True)
        return 8.0 * os.path.getsize(out)

def tune(domain, rounds=40):
    a = Agent(domain.name, domain.knobs, domain.bits, steps=getattr(domain, 'steps', ((2.0, 0.5), (1.5, 0.75)))); c = Centre([a], explore=0.0); c.run(rounds)
    return {'domain': domain.name, 'bits_start': a.ledger[0]['base_tune'] if a.ledger else None, 'bits_end': a.cost_tune, 'knobs': a.settings(), 'log_end': c.log[-1]}

if __name__ == '__main__':
    d = BloomDomain(); base = d.bits(d.knobs)
    print('Bloom description length %.1f bits (outward). Forge: 8 x bytes (inward), e.g. enwik8 best build = %d bits.' % (base, 8 * 19270420))
    r = tune(d); print('free-alpha_s what-if:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != 'log_end'})
    print('read: a moved theory value is a FREE knob (+0.5 log2 N bits); if it shortens the description it is FIT, never derived.')
