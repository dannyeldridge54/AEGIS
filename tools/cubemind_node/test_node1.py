"""Tests for Node 1 with stand-in models and no network. Run: python -m unittest -v test_node1"""
import json, re, shutil, tempfile, unittest
from pathlib import Path
import node1 as N, ufe_pack as U

class FakeLLM:
    def __init__(self, right=True, objection=False): self.right, self.objection, self.calls = right, objection, []
    def ask(self, model, prompt, num_predict=700):
        self.calls.append(model)
        if 'RETRIEVER' in prompt: return json.dumps({'lens': 'frame', 'useful': [], 'question': 'q'})
        if 'REFEREE' in prompt: return json.dumps({'mirror': 'could be wrong', 'verdict': 'FINDING' if self.objection else 'NULL', 'finding': 'x' if self.objection else ''})
        args = json.loads(re.search(r'for (\{.*?\})', prompt).group(1)); tool = next(t for t, v in U.TOOLS.items() if v[1].split('{x}')[0][:40] in prompt)
        v = float(U.TOOLS[tool][2](args)); return json.dumps({'steps': ['s'], 'result': v if self.right else v * 3 + 1})

class T(unittest.TestCase):
    def node(self, **kw):
        d = Path(tempfile.mkdtemp()); cfg = dict(N.DEFAULT, home=str(d / 'data'))
        n = N.Node(cfg, llm=FakeLLM(**kw), fetch=lambda s: [dict(source='github', title='a/b', url='https://github.com/a/' + s['id'], text='t')])
        n.ix = N.FP.Index(d / 'data' / 'n.sqlite', 'Danny Eldridge', key='ab' * 32); n.web = N.NW.Web(n.ix); return n
    def test_cycles_pass_index_and_write_status(self):
        n = self.node(); vs = [n.cycle() for _ in range(8)]
        self.assertEqual(set(vs), {'PASS'}); self.assertTrue((n.home / 'status.html').exists())
        st = json.loads((n.home / 'status.json').read_text()); self.assertEqual(st['cycles'], 8); self.assertGreater(st['records'], 8)
        self.assertTrue(all(n.ix.verify(r) for r in n.ix.find(kind='cycle'))); self.assertEqual(len(n.ix.find(kind='find')), 4)  # same finds dedupe
    def test_three_roles_use_three_models_in_order(self):
        n = self.node(); n.cycle(); m = N.DEFAULT['models']
        self.assertEqual(n.llm.calls, [m['retriever'], m['processor'], m['referee']])
    def test_wrong_answers_are_misses_and_objections_are_unclear(self):
        self.assertEqual(self.node(right=False).cycle(), 'MISS'); self.assertEqual(self.node(objection=True).cycle(), 'UNCLEAR')
    def test_rings_get_harder_after_three_in_a_row(self):
        n = self.node()
        for _ in range(24): n.cycle()
        self.assertTrue(any(r > 0 for r in n.state['ring'].values()))
    def test_survives_a_dead_model_server(self):
        class Dead:
            def ask(self, *a, **k): raise ConnectionError('ollama down')
        n = self.node(); n.llm = Dead(); self.assertEqual(n.cycle(), 'MISS')
    def test_backup_keeps_only_its_own_recent_copies(self):
        n = self.node(); n.cycle(); n.backup(); self.assertEqual(len(list((n.home / 'backups').glob('node1_*.sqlite'))), 1)
    def test_goalposts_listed_and_shown(self):
        n = self.node()
        for _ in range(5): n.cycle()
        g = n.goalposts(); self.assertEqual(len(g), 12); self.assertTrue(all({'part', 'goal', 'met', 'now'} <= set(x) for x in g))
        self.assertIn('Goalposts', (n.home / 'status.html').read_text())
    def test_selfcheck_runs_with_sympy(self):
        n = self.node(); n.cycle(); sc = n.state['selfcheck']; self.assertEqual((sc.get('reproduce'), sc.get('total')), (18, 18))
    def test_new_miners_alternate_sources(self):
        import node1
        node1.semantic_scholar_search = lambda q, n=5: [dict(source='semanticscholar', title='p', url='u1', text='')]
        node1.openalex_search = lambda q, n=5: [dict(source='openalex', title='w', url='u2', text='')]
        node1.github_search = lambda q, t=None, n=5: [dict(source='github', title='r', url='u3', text='')]
        node1.arxiv_search = lambda q, n=5: [dict(source='arxiv', title='a', url='u4', text='')]
        n = self.node(); n.fetch = None
        for _ in range(8): n.cycle()
        self.assertEqual(set(n.state['day']['sources']), {'github', 'arxiv', 'semanticscholar', 'openalex'})
    def test_batch_loads_each_model_once_and_files_all(self):
        n = self.node(); n.cfg['parallel'] = 1; vs = n.run_batch(8); m = N.DEFAULT['models']
        self.assertEqual(len(vs), 8); self.assertEqual(set(vs), {'PASS'})
        self.assertEqual(n.llm.calls, [m['retriever']] * 8 + [m['processor']] * 8 + [m['referee']] * 8)
    def test_parallel_batch_gives_same_verdicts(self):
        n = self.node(); n.cfg['parallel'] = 3; self.assertEqual(set(n.run_batch(6)), {'PASS'}); self.assertEqual(n.state['cycle'], 6)
    def test_same_search_is_not_repeated(self):
        calls = []
        n = self.node(); n.fetch = lambda s: calls.append(s['id']) or []
        for _ in range(16): n.cycle()
        self.assertEqual(len(calls), 8)                     # 4 subjects x 2 source pairs, then cached for 6 hours
if __name__ == '__main__': unittest.main()
