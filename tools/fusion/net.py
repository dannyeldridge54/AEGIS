"""Fractal engine network (PREREG_FUSION1). An Engine reads and writes a shared Bus, may hold child Engines (which may hold their own),
and may post postulates for its parent. Links are just bus keys, so they can point anywhere: down, up, sideways, or back. settle()
iterates the whole tree (children first) until the bus stops changing = where it settles. Dials = bounded optimisation of knobs."""
import math, time

class Bus:
    def __init__(self): self.v, self.meta, self.sweep = {}, {}, 0
    def put(self, who, key, value, label='LIVE', unit=''):
        self.v[key] = value; self.meta[key] = dict(who=who, label=label, unit=unit, sweep=self.sweep)
    def get(self, key, default=None): return self.v.get(key, default)
    def snap(self): return {k: v for k, v in self.v.items() if isinstance(v, (int, float, bool, str))}

class Engine:
    name = 'engine'
    def __init__(self, children=()): self.children = list(children); self.local = {}
    def run(self, bus): return {}
    def postulates(self, bus): return []
    def walk(self):
        for c in self.children: yield from c.walk()
        yield self

def _same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b): return True
        return abs(a - b) <= 1e-12 * max(1.0, abs(a))
    return a == b

def settle(root, bus, max_sweeps=8):
    prev = None
    for sw in range(1, max_sweeps + 1):
        bus.sweep = sw
        for e in root.walk(): e.local = e.run(bus) or {}
        snap = bus.snap()
        if prev is not None and snap.keys() == prev.keys() and all(_same(snap[k], prev[k]) for k in snap): return sw
        prev = snap
    return max_sweeps

def tree(root, depth=0):
    out = ['  ' * depth + f'- {root.name}']
    for c in root.children: out += tree(c, depth + 1)
    return out
