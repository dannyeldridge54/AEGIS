"""Tests for the field engine with deterministic mock models (no LLM needed). Run: python -m unittest -v test_engine"""
import asyncio, json, random, shutil, tempfile, unittest
import engine as E

class Harness:
    def __init__(self, acc, seed=1, learns=False):
        self.truth = None; self.rng = random.Random(seed); self.acc = acc; self.learns = learns
    def model(self, name):
        def fn(prompt):
            p = self.acc[name]
            if self.learns and 'worked:' in prompt: p = min(0.98, p + 0.3)      # lessons fed back help
            if 'first attempt was wrong' in prompt: p = min(0.98, p + 0.25)     # the corrector helps
            v = self.truth if self.rng.random() < p else self.truth * self.rng.choice([10, 0.5, 1.3, -1])
            return json.dumps({'steps': ['use the formula', 'substitute', 'compute'], 'result': v})
        return E.Mock(name, fn)
def make(acc, seed=1, learns=False, home=None):
    h = Harness(acc, seed, learns); home = home or tempfile.mkdtemp()
    eng = E.Engine(home, [h.model(n) for n in acc], seed=seed)
    frame0 = eng.frame
    def frame(tool, ring):
        fr = frame0(tool, ring); h.truth = float(E.TOOLS[tool][2](fr['args'])); return fr
    eng.frame = frame; return eng, h, home

class T(unittest.TestCase):
    def test_every_tool_passes_its_independent_tester_on_all_rings(self):
        r = random.Random(3)
        for name, (area, text, fit, test, tol, mk) in E.TOOLS.items():
            for ring in range(4):
                for _ in range(40):
                    a = mk(r, ring); self.assertTrue(test(a, fit(a)), (name, ring, a))
    def test_tester_catches_a_broken_fitter(self):
        self.assertFalse(E._decay_test({'N0': 1000, 'T': 5, 't': 10}, 300.0))   # true value 250
        self.assertFalse(E._plateau_r_test({'D': 10, 'N': 60}, 8.0 / (8 * 60)))  # wrong power of N
    def test_lock_is_written_before_result_and_chain_verifies(self):
        eng, h, home = make({'A': 0.9, 'B': 0.9}); asyncio.run(eng.cycle()); asyncio.run(eng.cycle())
        recs = [json.loads(l) for l in eng.ledger.read_text().splitlines()]
        self.assertEqual([r['kind'] for r in recs[:2]], ['lock', 'result']); self.assertEqual(recs[1]['lock'], recs[0]['hash'])
        self.assertEqual(E.verify_ledger(eng.ledger), (len(recs), True))
        lines = eng.ledger.read_text().splitlines(); r0 = json.loads(lines[0]); r0['tol'] = 0.5; lines[0] = json.dumps(r0)
        eng.ledger.write_text('\n'.join(lines) + '\n'); self.assertFalse(E.verify_ledger(eng.ledger)[1])   # tampering is detected
    def test_strong_models_extend_outward_and_weak_ones_do_not(self):
        strong, _, _ = make({'A': 0.97, 'B': 0.97}, seed=2); weak, _, _ = make({'A': 0.25, 'B': 0.25}, seed=2)
        for eng in (strong, weak):
            for _ in range(160): asyncio.run(eng.cycle())
        self.assertGreater(max(t['ring'] for t in strong.report()), 0); self.assertEqual(max(t['ring'] for t in weak.report()), 0)
    def test_agreement_gate_beats_single_model(self):
        eng, h, _ = make({'A': 0.7, 'B': 0.7}, seed=5); n = a = aok = single = 0
        for _ in range(300):
            r = asyncio.run(eng.cycle())
            if r.get('void'): continue
            n += 1; single += r['res'][0]['ok']
            if r['agree']: a += 1; aok += r['any_ok']
        self.assertGreater(aok / a, single / n + 0.15)
    def test_learning_raises_accuracy(self):
        base, _, _ = make({'A': 0.5, 'B': 0.5}, seed=7, learns=False); lrn, _, _ = make({'A': 0.5, 'B': 0.5}, seed=7, learns=True)
        def acc(eng):
            ok = n = 0
            for _ in range(240):
                r = asyncio.run(eng.cycle())
                if not r.get('void'): n += 1; ok += r['point_ok']
            return ok / n
        self.assertGreater(acc(lrn), acc(base) + 0.1)
    def test_corrector_recovers_some_misses_and_every_attempt_is_logged(self):
        eng, h, _ = make({'A': 0.4, 'B': 0.4}, seed=9)
        for _ in range(80): asyncio.run(eng.cycle())
        recs = [json.loads(l) for l in eng.ledger.read_text().splitlines() if '"result"' in l]
        retried = [d for r in recs for d in r['derivers'] if d['retried']]
        self.assertTrue(retried); self.assertTrue(any(d['ok2'] for d in retried)); self.assertTrue(all('value' in d for r in recs for d in r['derivers']))
    def test_state_survives_restart(self):
        eng, h, home = make({'A': 0.9, 'B': 0.9}, seed=4)
        for _ in range(10): asyncio.run(eng.cycle())
        eng2, _, _ = make({'A': 0.9, 'B': 0.9}, seed=4, home=home); self.assertEqual(eng2.state['cycle'], 10); shutil.rmtree(home)
if __name__ == '__main__': unittest.main()
