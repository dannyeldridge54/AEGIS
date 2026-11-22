#!/usr/bin/env python3
"""Loom core (LOOM_CORE_STANDARD.md): a fractal of knob agents with a balancing centre.
Agent: owns <= 9 knobs, tunes them octave-then-fifth against its own cost on the TUNE split, and accepts a change only if it also
helps on the HELD split (held-out gate). Agents nest: an Agent can be a knob-holder inside a parent Agent via its 'subagents'.
Centre: bandit over agents; spends each round on the agent with the best recent gain (with exploration), logs every poke."""
import json, math, random, time
MAX_KNOBS = 9
class Agent:
    def __init__(self, name, knobs, evaluate, steps=((2.0, 0.5), (1.5, 0.75)), lo=None, hi=None, tol=1e-4, subagents=()):
        assert len(knobs) <= MAX_KNOBS, 'standard: at most 9 knobs per agent (split into sub-agents)'
        self.name, self.k, self.evaluate, self.steps, self.tol = name, dict(knobs), evaluate, steps, tol
        self.lo, self.hi = lo or {}, hi or {}; self.sub = list(subagents); self.level = 0; self.gains = []; self.ledger = []
        self.cost_tune = None; self.cost_held = None
    def settings(self):
        s = dict(self.k)
        for a in self.sub: s.update(a.settings())
        return s
    def _clip(self, key, v):
        if key in self.lo: v = max(self.lo[key], v)
        if key in self.hi: v = min(self.hi[key], v)
        return v
    def step(self):
        """One tuning pass at the current interval level. Returns the relative gain on TUNE that also held on HELD (0 if none)."""
        for a in self.sub: a.step()                                     # inner agents first (fractal)
        if self.cost_tune is None:
            self.cost_tune, self.cost_held = self.evaluate(self.settings(), 'tune'), self.evaluate(self.settings(), 'held')
        up, down = self.steps[min(self.level, len(self.steps) - 1)]; best_gain = 0.0
        for key in list(self.k):
            for f in (up, down):
                old = self.k[key]; new = self._clip(key, old * f if old else f - 1)
                if new == old: continue
                self.k[key] = new; s = self.settings(); ct = self.evaluate(s, 'tune')
                rec = {'t': time.time(), 'agent': self.name, 'knob': key, 'from': old, 'to': new, 'tune': ct, 'base_tune': self.cost_tune}
                if ct < self.cost_tune * (1 - self.tol):
                    ch = self.evaluate(s, 'held'); rec['held'] = ch; rec['base_held'] = self.cost_held
                    if ch < self.cost_held * (1 - self.tol):            # held-out gate
                        g = (self.cost_tune - ct) / self.cost_tune; best_gain = max(best_gain, g)
                        self.cost_tune, self.cost_held = ct, ch; rec['kept'] = True; self.ledger.append(rec); break
                self.k[key] = old; rec['kept'] = False; self.ledger.append(rec)
        if best_gain == 0.0: self.level += 1                            # octave exhausted -> fifths; then null
        self.gains.append(best_gain); return best_gain
    def null(self): return self.level >= len(self.steps) and all(a.null() for a in self.sub)
class Centre:
    """Balances agents: picks the agent with the best upper-confidence recent gain; stops when every agent is null (balanced) or budget ends."""
    def __init__(self, agents, explore=0.1, seed=0):
        self.agents, self.explore, self.rng, self.log = agents, explore, random.Random(seed), []
    def run(self, rounds=100):
        for r in range(rounds):
            live = [a for a in self.agents if not a.null()]
            if not live: self.log.append({'round': r, 'event': 'BALANCED: all agents null'}); break
            def ucb(a): g = a.gains[-3:] or [1.0]; return sum(g) / len(g) + self.explore * math.sqrt(math.log(r + 2) / (len(a.gains) + 1))
            a = max(live, key=ucb) if self.rng.random() > self.explore else self.rng.choice(live)
            g = a.step(); self.log.append({'round': r, 'agent': a.name, 'gain': g, 'level': a.level})
        return {a.name: a.settings() for a in self.agents}
if __name__ == '__main__':
    # self-test: a separable toy cost with a held-out twin (slight shift); the optimum is near k_i = 2**(i % 3)
    target = {f'k{i}': 2.0 ** (i % 3) for i in range(12)}
    def cost(s, split):
        shift = 1.0 if split == 'tune' else 1.02
        return sum((math.log2(s[k]) - math.log2(target[k] * shift)) ** 2 for k in s) + 1.0
    inner = Agent('inner', {f'k{i}': 1.0 for i in range(9, 12)}, lambda s, sp: cost(s, sp))
    a1 = Agent('A', {f'k{i}': 1.0 for i in range(0, 5)}, lambda s, sp: cost(dict(s, **{k: v for k, v in target.items() if k not in s}), sp))
    a2 = Agent('B', {f'k{i}': 1.0 for i in range(5, 9)}, lambda s, sp: cost(dict(s, **{k: v for k, v in target.items() if k not in s}), sp), subagents=[inner])
    c = Centre([a1, a2]); out = c.run(60)
    err = max(abs(math.log2(v) - math.log2(target[k])) for d in out.values() for k, v in d.items())
    print('SELFTEST', 'PASS' if err < 0.6 else 'FAIL', 'max log2 error %.2f' % err, c.log[-1])
