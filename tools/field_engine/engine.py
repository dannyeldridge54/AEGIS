"""AEGIS Field Engine (24 Nov 2026) - a self-directing, self-correcting, self-learning research loop with CubeMind at the centre.

Roles (one cycle = one point of the field map):
  PLANNER   picks the next point: weakest area first (learn), then one ring further out where mastery is solid (extend).  [code]
  LENSER    frames the point: task text, inputs, tolerance, pass rule.                                                      [code]
  LOCK      the frame is hashed and written to the ledger BEFORE any model is called (pre-registration).                    [code]
  DERIVERS  two or more language models derive the number blind, in parallel (the axes).                                    [LLM]
  FITTER    the validated tool computes the reference value.                                                                [code]
  TESTER    an independent method or invariance check must agree with the fitter, else the POINT is void (not the model).   [code]
  REFEREE   scores each deriver against the reference, and records whether the derivers agreed with each other.             [code]
  CORRECTOR on a miss: one retry, told the kind of error but never the answer; logged as a deviation.                       [LLM]
  LIBRARIAN keeps lessons (worked steps that passed, error kinds that failed) and feeds them back; updates mastery.         [code]
Design rules from the research: models propose, code verifies; an outside check decides, never a model judging a model;
every attempt is logged (no silent discards); agreement between independent models is the trust signal.
Speed: asyncio, all derivers for a point run at once, calls are grouped per model (no VRAM swapping), answers are cached by prompt
hash, tools run in-process. Standard library only."""
import asyncio, hashlib, json, math, os, random, re, time, urllib.request
from pathlib import Path

# ----------------------------------------------------------------------------- tools: fitter + independent tester
def _koide(a):
    m = a['masses']; return sum(m) / sum(math.sqrt(x) for x in m) ** 2
def _koide_test(a, v):                      # scale invariance and the exact bounds 1/3 <= Q <= 1
    m2 = [x * 7.3 for x in a['masses']]; return abs(_koide({'masses': m2}) - v) < 1e-12 and 1 / 3 - 1e-12 <= v <= 1 + 1e-12
def _plateau_r(a):
    return 8.0 / ((a['D'] - 2) * a['N'] ** 2)
def _plateau_r_test(a, v):                  # independent: numerical slow roll on V = 1 - e^(-beta phi), beta^2 = D - 2
    b = math.sqrt(a['D'] - 2); N = a['N']
    f = lambda phi: (math.exp(b * phi) - b * phi) / b ** 2          # N(phi) = integral V/V' dphi (up to the end point)
    lo, hi = 0.0, 60.0
    phi_end = math.log(1 + b / math.sqrt(2)) / b                     # epsilon = 1
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) - f(phi_end) < N: lo = mid
        else: hi = mid
    e = math.exp(-b * lo); eps = 0.5 * (b * e / (1 - e)) ** 2
    return abs(16 * eps - v) / v < 0.12                               # leading-order formula vs numerical: within 12%
def _decay(a): return a['N0'] * 2.0 ** (-a['t'] / a['T'])
def _decay_test(a, v):                      # independent: exponential form, and composition N(t) = N(t/2) applied twice
    half = a['N0'] * math.exp(-math.log(2) * (a['t'] / 2) / a['T'])
    return abs(half * math.exp(-math.log(2) * (a['t'] / 2) / a['T']) - v) <= 1e-9 * max(v, 1e-300)
def _greenwald(a): return a['Ip'] / (math.pi * a['a'] ** 2)
def _greenwald_test(a, v): return abs(_greenwald({'Ip': 2 * a['Ip'], 'a': 2 * a['a']}) - v / 2) < 1e-12 * max(v, 1)
def _magp(a): return a['B'] ** 2 / (2 * 4e-7 * math.pi) / 1e6
def _magp_test(a, v): return abs(_magp({'B': 3 * a['B']}) - 9 * v) < 1e-9 * max(v, 1)
def _par(a): return a['R1'] * a['R2'] / (a['R1'] + a['R2'])
def _par_test(a, v): return abs(1 / (1 / a['R1'] + 1 / a['R2']) - v) < 1e-9 * v     # conductance sum
def _dm(a): return math.exp(a['b'] * a['dphi']) - 1
def _dm_test(a, v):                          # independent: Taylor series to 12 terms
    x = a['b'] * a['dphi']; s = sum(x ** k / math.factorial(k) for k in range(1, 13)); return abs(s - v) < 1e-9
def _amat(a): return a['hit'] + a['miss'] / 100 * a['pen']
def _amat_test(a, v): return abs(((100 - a['miss']) * a['hit'] + a['miss'] * (a['hit'] + a['pen'])) / 100 - v) < 1e-9

def _u(r, lo, hi, nd=3): return round(r.uniform(lo, hi), nd)
# name: (area, task text, fitter, tester, tolerance, args builder(rng, ring)) - ring 0 is the home range, each ring reaches further out
TOOLS = {
 'weave_koide':   ('weave',    'Compute the Koide ratio Q = (m1+m2+m3) / (sqrt(m1)+sqrt(m2)+sqrt(m3))^2 for masses {x}.', _koide, _koide_test, 0.01,
                   lambda r, k: {'masses': sorted([_u(r, 0.1, 1 * 10 ** k + 1), _u(r, 5, 50 * 3 ** k), _u(r, 100, 2000 * 3 ** k)])}),
 'weave_plateau': ('weave',    'For a plateau inflation model the tensor ratio is r = 8 / ((D-2) N^2). Compute r for {x}.', _plateau_r, _plateau_r_test, 0.02,
                   lambda r, k: {'D': r.choice([4, 6, 10][: 1 + min(k, 2)] or [4]) if k else 10, 'N': r.randint(50 - 5 * min(k, 4), 60 + 10 * k)}),
 'weave_negspace':('negspace', 'A dark-matter particle mass scales as exp(b*dphi). Compute the fractional mass change exp(b*dphi) - 1 for {x}.', _dm, _dm_test, 0.02,
                   lambda r, k: {'b': -_u(r, 0.02, 0.12 + 0.1 * k), 'dphi': _u(r, 0.4, 0.8 + 0.4 * k)}),
 'nuc_decay':     ('nuclear',  'A sample has N0 atoms and half-life T. Compute how many remain after time t (same units) for {x}.', _decay, _decay_test, 0.01,
                   lambda r, k: {'N0': r.randint(1, 9) * 10 ** (3 + k), 'T': r.choice([2, 5, 8, 12.3, 30]), 't': _u(r, 1, 20 + 40 * k, 1)}),
 'rx_greenwald':  ('reactor',  'The Greenwald density limit is n_G = Ip / (pi a^2) in 1e20 m^-3 with Ip in MA and a in m. Compute n_G for {x}.', _greenwald, _greenwald_test, 0.01,
                   lambda r, k: {'Ip': _u(r, 5, 20 + 10 * k, 1), 'a': _u(r, 1.0, 3.0 + k, 2)}),
 'field_pressure':('fields',   'Magnetic pressure is p = B^2 / (2 mu0), mu0 = 4 pi 1e-7. Compute p in MPa for {x} (B in tesla).', _magp, _magp_test, 0.01,
                   lambda r, k: {'B': _u(r, 1, 12 + 8 * k, 1)}),
 'circ_parallel': ('circuits', 'Two resistors R1 and R2 (ohms) are in parallel. Compute the equivalent resistance for {x}.', _par, _par_test, 0.01,
                   lambda r, k: {'R1': r.randint(2, 99 * 10 ** k), 'R2': r.randint(2, 99 * 10 ** k)}),
 'cpu_amat':      ('cpu',      'Cache hit time is "hit" cycles, miss rate "miss" percent, miss penalty "pen" cycles. Compute the average access time for {x}.', _amat, _amat_test, 0.01,
                   lambda r, k: {'hit': r.randint(1, 4), 'miss': r.choice([1, 2, 5, 10, 20]), 'pen': r.choice([20, 50, 100, 200]) * (1 + k)}),
}

# ----------------------------------------------------------------------------- backends (the axes)
class Ollama:
    def __init__(self, model, host='http://127.0.0.1:11434', timeout=180):
        self.name, self.host, self.timeout = model, host, timeout
    def _call(self, prompt):
        body = {'model': self.name, 'prompt': prompt, 'stream': False, 'keep_alive': '30m', 'options': {'temperature': 0.2, 'num_predict': 500}}
        if self.name.startswith(('qwen3:', 'deepseek-r1')): body['think'] = False
        req = urllib.request.Request(self.host + '/api/generate', json.dumps(body).encode(), {'Content-Type': 'application/json'})
        return json.loads(urllib.request.urlopen(req, timeout=self.timeout).read()).get('response', '')
    async def ask(self, prompt): return await asyncio.to_thread(self._call, prompt)
class Mock:
    """Test double: answers through a supplied function(prompt) -> text."""
    def __init__(self, name, fn): self.name, self.fn = name, fn
    async def ask(self, prompt): await asyncio.sleep(0); return self.fn(prompt)

def parse_number(text):
    text = re.sub(r'<think>.*?</think>', '', text or '', flags=re.S)
    m = re.search(r'\{.*\}', text, flags=re.S)
    if m:
        try:
            j = json.loads(m.group(0)); return float(j['result']), [str(s)[:200] for s in (j.get('steps') or [])][:6]
        except Exception: pass
    nums = re.findall(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', text)
    return (float(nums[-1]), []) if nums else (None, [])

# ----------------------------------------------------------------------------- the engine
class Engine:
    def __init__(self, home, derivers, seed=0, min_agree=2):
        self.home = Path(home); self.home.mkdir(parents=True, exist_ok=True)
        self.derivers, self.rng, self.min_agree = derivers, random.Random(seed), min_agree
        self.ledger = self.home / 'ledger.jsonl'; self.state_f = self.home / 'state.json'; self.cache_f = self.home / 'cache.json'
        self.state = json.loads(self.state_f.read_text()) if self.state_f.exists() else {'cycle': 0, 'tools': {}, 'lessons': {}, 'prev': '0' * 16}
        self.cache = json.loads(self.cache_f.read_text()) if self.cache_f.exists() else {}
        self.sem = {d.name: asyncio.Semaphore(int(os.environ.get('ENGINE_PARALLEL', '2'))) for d in derivers}
        for t in TOOLS: self.state['tools'].setdefault(t, {'ring': 0, 'hist': [], 'void': 0})
    # --- ledger: append-only, hash-chained, so a reviewer can re-derive and nothing can be silently dropped
    def log(self, kind, **rec):
        rec = dict(kind=kind, cycle=self.state['cycle'], t=round(time.time(), 2), prev=self.state['prev'], **rec)
        h = hashlib.sha256(json.dumps(rec, sort_keys=True, default=str).encode()).hexdigest()[:16]; rec['hash'] = h; self.state['prev'] = h
        with open(self.ledger, 'a', encoding='utf-8') as f: f.write(json.dumps(rec, default=str) + '\n')
        return h
    def mastery(self, tool):
        h = self.state['tools'][tool]['hist'][-8:]; return (sum(h) / len(h)) if len(h) >= 6 else None
    # --- PLANNER: learn where weak, extend where solid; a small exploration share keeps coverage up (diversity)
    def plan(self):
        if self.rng.random() < 0.15: tool = self.rng.choice(list(TOOLS)); why = 'explore'
        else:
            scored = [((self.mastery(t) if self.mastery(t) is not None else -1), len(self.state['tools'][t]['hist']), t) for t in TOOLS]
            m, n, tool = min(scored); why = 'unseen' if m < 0 else ('learn' if m < 0.8 else 'extend')
        st = self.state['tools'][tool]; m = self.mastery(tool)
        if m is not None and m >= 0.8 and len(st['hist']) >= 4 * (st['ring'] + 1): st['ring'] += 1; st['hist'] = st['hist'][-2:]; why = f'extend to ring {st["ring"]}'
        elif m is not None and m < 0.4 and st['ring'] > 0 and len(st['hist']) >= 6: st['ring'] -= 1; st['hist'] = []; why = f'fall back to ring {st["ring"]}'
        return tool, st['ring'], why
    # --- LENSER
    def frame(self, tool, ring):
        area, text, fit, test, tol, mk = TOOLS[tool]; args = mk(self.rng, ring)
        lessons = self.state['lessons'].get(tool, [])[-3:]
        prompt = (text.replace('{x}', json.dumps(args)) + '\nShow short numbered steps, then the final number.'
                  + ('\nNotes from earlier attempts at this kind of problem (methods only, different inputs):\n' + '\n'.join('- ' + l for l in lessons) if lessons else '')
                  + '\nReply JSON only: {"steps": [<strings>], "result": <number>}')
        return dict(tool=tool, area=area, ring=ring, args=args, tol=tol, rule='|answer - reference| <= tol * |reference|', prompt=prompt)
    async def _ask(self, d, prompt):
        key = hashlib.sha256((d.name + '\x00' + prompt).encode()).hexdigest()[:24]
        if key in self.cache: return self.cache[key], True
        async with self.sem[d.name]:
            try: out = await d.ask(prompt)
            except Exception as e: out = f'ERROR {type(e).__name__}: {e}'
        self.cache[key] = out; return out, False
    # --- one cycle
    async def cycle(self):
        self.state['cycle'] += 1
        tool, ring, why = self.plan(); fr = self.frame(tool, ring)
        lock = self.log('lock', tool=tool, ring=ring, why=why, args=fr['args'], tol=fr['tol'], rule=fr['rule'],
                        prompt_sha=hashlib.sha256(fr['prompt'].encode()).hexdigest()[:16])          # LOCK before any model call
        answers = await asyncio.gather(*[self._ask(d, fr['prompt']) for d in self.derivers])     # DERIVERS, in parallel
        _, _, fit, test, tol, _ = TOOLS[tool]
        try: ref = float(fit(fr['args'])); tested = bool(test(fr['args'], ref))                    # FITTER + TESTER
        except Exception as e: ref, tested = None, False
        if not tested:                                                                              # the POINT is void, not the models
            self.state['tools'][tool]['void'] += 1; self.log('void', lock=lock, tool=tool, args=fr['args'], reference=ref)
            self._save(); return dict(tool=tool, ring=ring, why=why, void=True)
        ok_of = lambda v: v is not None and abs(v - ref) <= tol * max(abs(ref), 1e-300)
        res = []
        for d, (out, cached) in zip(self.derivers, answers):
            v, steps = parse_number(out); res.append(dict(model=d.name, value=v, ok=ok_of(v), steps=steps, cached=cached, retried=False))
        # CORRECTOR: one retry for a miss, told the error kind only
        async def retry(d, r):
            kind = 'no number was given' if r['value'] is None else ('the answer is off by more than a factor of 10 (check units or powers of ten)' if ref and r['value'] and (abs(r['value'] / ref) > 10 or abs(r['value'] / ref) < 0.1) else 'the method or arithmetic has an error')
            out, _ = await self._ask(d, fr['prompt'] + f'\nYour first attempt was wrong: {kind}. Redo it carefully from the formula.')
            v, steps = parse_number(out); r.update(value2=v, ok2=ok_of(v), retried=True, kind=kind)
            if r['ok2']: r['steps'] = steps
        await asyncio.gather(*[retry(d, r) for d, r in zip(self.derivers, res) if not r['ok']])
        vals = [r['value'] for r in res if r['value'] is not None]
        agree = len(vals) >= self.min_agree and all(abs(a - b) <= 2 * tol * max(abs(a), abs(b), 1e-300) for a in vals for b in vals)
        first_ok = [r['ok'] for r in res]; point_ok = sum(first_ok) > len(res) / 2          # a point counts only when a strict majority of the axes got it right first time
        # REFEREE record + LIBRARIAN
        self.state['tools'][tool]['hist'].append(1 if point_ok else 0)
        L = self.state['lessons'].setdefault(tool, [])
        for r in res:
            if r['ok'] and r['steps']: L.append('worked: ' + ' | '.join(r['steps'])[:300])
            elif r.get('retried') and not r.get('ok2'): L.append('pitfall: ' + r['kind'])
            elif r.get('retried') and r.get('ok2') and r['steps']: L.append('fixed after a miss (' + r['kind'] + '): ' + ' | '.join(r['steps'])[:240])
        self.state['lessons'][tool] = list(dict.fromkeys(L))[-6:]
        self.log('result', lock=lock, tool=tool, ring=ring, reference=ref, tested=True, agree=agree, point_ok=point_ok,
                 derivers=[{k: r.get(k) for k in ('model', 'value', 'ok', 'retried', 'value2', 'ok2', 'cached')} for r in res])
        self._save()
        return dict(tool=tool, ring=ring, why=why, void=False, agree=agree, point_ok=point_ok, any_ok=any(first_ok), res=res)
    def _save(self):
        self.state_f.write_text(json.dumps(self.state)); self.cache_f.write_text(json.dumps(self.cache))
    def report(self):
        rows = []
        for t, st in self.state['tools'].items():
            m = self.mastery(t); rows.append(dict(tool=t, area=TOOLS[t][0], ring=st['ring'], attempts=len(st['hist']), mastery=None if m is None else round(m, 2), void=st['void']))
        return rows

def verify_ledger(path):
    """Re-check the hash chain: returns (records, ok)."""
    prev, n = '0' * 16, 0
    with open(path, encoding='utf-8') as f:
        for line in f:
            r = json.loads(line); h = r.pop('hash')
            if r['prev'] != prev or hashlib.sha256(json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()[:16] != h: return n, False
            prev, n = h, n + 1
    return n, True

async def run(home, models, cycles, seed=0):
    eng = Engine(home, [Ollama(m) for m in models], seed=seed); t0 = time.time(); agree_n = agree_ok = 0
    for i in range(cycles):
        r = await eng.cycle()
        if r.get('void'): print(f"cycle {eng.state['cycle']}: {r['tool']} VOID (tester disagreed with fitter)", flush=True); continue
        if r['agree']: agree_n += 1; agree_ok += r['any_ok']
        print(f"cycle {eng.state['cycle']}: {r['tool']} ring {r['ring']} [{r['why']}] " + ' '.join(f"{x['model']}={'ok' if x['ok'] else ('fixed' if x.get('ok2') else 'miss')}" for x in r['res']) + (' AGREE' if r['agree'] else ''), flush=True)
    print(json.dumps(eng.report(), indent=1)); print(f'agreement gate: {agree_ok}/{agree_n} correct when the axes agreed; {time.time() - t0:.0f} s; ledger', verify_ledger(eng.ledger))

if __name__ == '__main__':
    import argparse
    a = argparse.ArgumentParser(description='AEGIS Field Engine'); a.add_argument('--models', nargs='+', required=True)
    a.add_argument('--cycles', type=int, default=20); a.add_argument('--home', default='field_engine_data'); a.add_argument('--seed', type=int, default=0)
    g = a.parse_args(); asyncio.run(run(g.home, g.models, g.cycles, g.seed))
