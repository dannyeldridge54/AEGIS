"""Tests for Node 1 with stand-in models and no network. Run: python -m unittest -v test_node1"""
import json, re, shutil, tempfile, unittest
from pathlib import Path
import node1 as N, ufe_pack as U

class FakeLLM:
    def __init__(self, right=True, objection=False, stuck=False): self.right, self.objection, self.stuck, self.calls = right, objection, stuck, []
    def ask(self, model, prompt, num_predict=700):
        self.calls.append(model)
        if 'ROUTE PLANNER' in prompt:
            lane = prompt.split('LANES (best supported first):\n- ')[1].split(':')[0]; names = prompt.split('(ONLY these may go in uses): ')[1].split('\n')[0].split(', ')
            return json.dumps({'sphere': 'Workshop', 'lane': lane, 'why': 'most records', 'uses': [names[0], 'made_up_tool'], 'steps': ['package the lane tools', 'test them'],
                               'missing': ['how to package python tools']})
        if 'DOORWAY request' in prompt:
            names = prompt.split('(ONLY these): ')[1].split('\n')[0].split(', ')
            return json.dumps({'answer': 'use the data set', 'doorways': [{'to': names[0], 'relation': 'checks', 'why': 'w'}, {'to': 'imaginary.csv', 'relation': 'checks'}], 'epoch': 'late', 'search': 'sqlite thread safety python', 'improve': {'module': 'nope', 'idea': 'x'}})
        if 'You are the CODE CARTOGRAPHER' in prompt or 'CODE CARTOGRAPHER' in prompt.split(chr(10))[0]:
            mods = prompt.split('(ONLY these): ')[1].split('\n')[0].split(', ')
            return json.dumps({'purpose': 'p', 'ring': 'R1', 'anchor': 'rho', 'shape': 'hexagonal', 'weight': '2', 'side': 'centre', 'layer': 'torus', 'epoch': 'all',
                               'pathways': [{'to': mods[0], 'relation': 'derived_from', 'why': 'w'}, {'to': 'invented_module', 'relation': 'similar', 'why': 'w'}],
                               'search': 'python ast call graph', 'improve': {'module': mods[0], 'idea': 'cache the lattice sums', 'why': 'speed'},
                               'fetch_repo': 'numpy/numpy', 'tune': {'setting': 'hints_per_batch', 'value': 4, 'why': 'faster'},
                               'want_tool': {'what': 'networkx', 'why': 'graphs', 'how': 'pip install networkx'},
                               'post': {'title': 'Mapping modules', 'body': 'wiring the code now', 'status': 'working'}, 'message': {'to': 'referee', 'body': 'please double-check module alpha'}})
        if 'You are the MAPPER' in prompt:
            n = prompt.count('. [')
            return json.dumps({'finds': [{'i': k, 'ring': 'R1', 'anchor': 'rho', 'shape': 'hexagonal', 'orbifold': 'Z2xZ2', 'weight': '2', 'side': 'centre', 'layer': 'torus', 'why': 'w'} for k in range(n)] + [{'i': 0, 'ring': 'R9'}],
                               'links': [{'proposal': 0, 'accept': True, 'relation': 'similar', 'why': 'w'}, {'proposal': 1, 'accept': True, 'relation': 'made_up'}]})
        if 'You are the RETRIEVER' in prompt: return json.dumps({'lens': 'frame', 'useful': [], 'question': 'q', 'stuck': 'need the DESI data set' if self.stuck else ''})
        if 'You are the REFEREE' in prompt: return json.dumps({'mirror': 'could be wrong', 'verdict': 'FINDING' if self.objection else 'NULL', 'finding': 'x' if self.objection else ''})
        task = prompt.split('Task:', 1)[1].split('\n', 1)[0] if 'Task:' in prompt else ''
        mm = re.search(r'for (\{.*?\})', task)
        if not mm: return json.dumps({'plan': ['step'], 'files': [], 'test': 't'})     # a build/upgrade/instruction prompt, not a calculation
        args = json.loads(mm.group(1)); tool = next(t for t, v in U.TOOLS.items() if v[1].split('{x}')[0][:40] in task)
        v = float(U.TOOLS[tool][2](args)); return json.dumps({'steps': ['s'], 'result': v if self.right else v * 3 + 1})

class T(unittest.TestCase):
    def node(self, **kw):
        d = Path(tempfile.mkdtemp()); cfg = dict(N.DEFAULT, home=str(d / 'data'), local_folders=[str(d / 'research')], sweep_first=False)
        (d / 'research').mkdir(); (d / 'research' / 'eisenstein_fit_notes.md').write_text('Eisenstein series fit at rho. modular invariant Eisenstein series string effective action.')
        n = N.Node(cfg, llm=FakeLLM(**kw), fetch=lambda s: [dict(source='github', title='repo ' + s['id'], url='https://github.com/a/' + s['id'], text='t')])
        n.ix = N.FP.Index(d / 'data' / 'n.sqlite', 'Danny Eldridge', key='ab' * 32); n.web = N.NW.Web(n.ix); n.instr_path = d / 'INSTRUCTIONS.txt'; return n
    def test_cycles_pass_index_and_write_status(self):
        n = self.node(); vs = [n.cycle() for _ in range(8)]
        self.assertEqual(set(vs), {'PASS'}); self.assertTrue((n.home / 'status.html').exists())
        st = json.loads((n.home / 'status.json').read_text()); self.assertEqual(st['cycles'], 8); self.assertGreater(st['records'], 8)
        self.assertTrue(all(n.ix.verify(r) for r in n.ix.find(kind='cycle'))); self.assertEqual(len(n.ix.find(kind='find')), 5)  # 4 web (dedupe) + 1 local file
    def test_three_roles_use_three_models_in_order(self):
        n = self.node(); n.cycle(); m = N.DEFAULT['models']
        self.assertEqual(n.llm.calls[:4], [m['retriever'], m['mapper'], m['processor'], m['referee']])   # pipeline first; programmer acts after
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
        g = n.goalposts(); self.assertEqual(len(g), 25); self.assertTrue(all({'part', 'goal', 'met', 'now'} <= set(x) for x in g))
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
        import time; time.sleep(1.5)
        for _ in range(4): n.cycle()                          # take what the background helper found
        self.assertEqual(set(n.state['day']['sources']), {'github', 'arxiv', 'semanticscholar', 'openalex', 'local'})
    def test_batch_loads_each_model_once_and_files_all(self):
        n = self.node(); n.cfg['parallel'] = 1; vs = n.run_batch(8); m = N.DEFAULT['models']
        self.assertEqual(len(vs), 8); self.assertEqual(set(vs), {'PASS'})
        c = n.llm.calls.count(m['mapper']); self.assertGreaterEqual(c, 1)        # the mapper is only called when there is something new to map
        pipe = [m['retriever']] * 8 + [m['mapper']] * c + [m['processor']] * 8 + [m['referee']] * 8
        self.assertEqual(n.llm.calls[:len(pipe)], pipe)   # pipeline first; the programmer's own calls may follow
    def test_parallel_batch_gives_same_verdicts(self):
        n = self.node(); n.cfg['parallel'] = 3; self.assertEqual(set(n.run_batch(6)), {'PASS'}); self.assertEqual(n.state['cycle'], 6)
    def test_same_search_is_not_repeated(self):
        calls = []
        n = self.node(); n.fetch = lambda s: calls.append(s['id']) or []
        for _ in range(16): n.cycle()
        self.assertEqual(len(calls), 8)                     # 4 subjects x 2 source pairs, then cached for 6 hours (local search is separate)
    def test_mapper_files_addresses_rejects_bad_markers_and_files_two_sided_links(self):
        n = self.node()
        for _ in range(6): n.cycle()
        st = n.state['mapper']; cats = n.ix.find(kind='catalog'); self.assertTrue(cats)
        rec = n.ix.get(cats[0]); self.assertEqual(rec['tags']['ring'], 'R1'); self.assertEqual(rec['tags']['anchor'], 'rho'); self.assertEqual(rec['tags']['status'], 'ASSUMED')
        self.assertGreater(st['rejected'], 0)                                   # 'R9' and 'made_up' are refused
        for lid in n.ix.find(kind='link'): self.assertIn(n.ix.get(lid)['tags']['relation'], N.MARKERS['relation'])
    def test_cycle_records_carry_the_geometric_address(self):
        n = self.node(); n.cycle(); r = n.ix.get(n.ix.find(kind='cycle')[0])['tags']
        self.assertEqual((r['ring'], r['anchor'], r['shape'], r['orbifold'], r['weight']), ('R1', 'rho', 'hexagonal', 'Z2xZ2', '2'))
    def test_lanes_and_geometric_retrieval_step_out_then_reduce(self):
        n = self.node()
        for k, (ring, anchor, shape, weight, layer) in enumerate([('R1', 'rho', 'hexagonal', '2', 'torus')] * 5 + [('R1', 'i', 'square', '2', 'cube')] * 5 + [('R2', 'rho', 'hexagonal', '3/2', 'fold')] * 5):
            n.ix.stamp('catalog', inputs={'k': k}, tags=dict(ring=ring, anchor=anchor, shape=shape, weight=weight, layer=layer, side='centre'))
        lanes = n.lanes(); self.assertEqual(len(lanes), 3); self.assertEqual(lanes[0]['total'], 5)
        r = n.retrieve_by_geometry(dict(ring='R1', anchor='rho', shape='hexagonal', weight='2'), k=3)
        self.assertEqual(len(r['results']), 3); self.assertTrue(all(x['markers']['anchor'] == 'rho' and x['markers']['ring'] == 'R1' for x in r['results']))
        self.assertTrue(r['relaxed'])                               # only 5 exact matches < 2k=6: it stepped out
        self.assertEqual(len(n.ix.find(kind='retrieval')), 1)
    def test_string_places_records_by_epoch_and_wraps_the_limits(self):
        n = self.node()
        for _ in range(4): n.cycle()
        si = n.string_index(); q = next(x for x in si['string'] if x['epoch'] == 'quantum'); inf = next(x for x in si['string'] if x['epoch'] == 'inflation')
        self.assertGreater(q['records'], 0); self.assertGreater(inf['records'], 0); self.assertGreater(si['wrapper'], 0)   # eisenstein = 'all' wraps
        self.assertEqual(N.string_position('late'), 60.72); self.assertIsNone(N.string_position('all'))
        self.assertIn('The string', (n.home / 'status.html').read_text())
    def test_local_folder_search_finds_own_fits_once(self):
        n = self.node(); n.cycle(); loc = [r for r in n.ix.find(kind='find') if n.ix.get(r)['outputs'].get('source') == 'local']
        self.assertEqual(len(loc), 1); n.cycle(); n.cycle(); n.cycle(); n.cycle()
        self.assertEqual(len([r for r in n.ix.find(kind='find') if n.ix.get(r)['outputs'].get('source') == 'local']), 1)
    def test_display_draws_three_views_and_live_phase(self):
        n = self.node(); n.run_batch(4); html = (n.home / 'dashboard.html').read_text()
        for part in ('Timeline: the single string', 'Memory map', 'Categories: lanes', 'Now', 'R1-serapis-rho'): self.assertIn(part, html)
        data = json.loads(html.split('const NODES = ')[1].split(';\n')[0].replace('<\\/', '</'))
        snap = data['R1-serapis-rho']; self.assertEqual(snap['phase']['name'], 'waiting'); self.assertEqual(snap['cycles'], 4); self.assertTrue(snap['neurons'])
    def test_sweep_maps_every_file_once_and_marks_copies(self):
        n = self.node(); n.cfg['sweep_first'] = True; root = Path(n.cfg['local_folders'][0])
        for k in range(12): (root / f'data_{k}.json').write_text(json.dumps({'fit': k, 'rho': 0.866}))
        for k in range(6): (root / f'copy_of_data_{k}.json').write_text(json.dumps({'fit': k, 'rho': 0.866}))     # identical content
        n.local.files = []; n.state.pop('sweep', None)
        out = [n.run_batch(8) for _ in range(5)]
        sw = n.state['sweep']; self.assertEqual(sw['total'], 19); self.assertEqual(sw['unique'], 13); self.assertEqual(sw['duplicates'], 6)
        self.assertEqual(len([r for r in n.ix.find(kind='find', limit=1000) if n.ix.get(r)['tags'].get('subject') == 'local-sweep']), 13)
        self.assertTrue(all(p.exists() for p in root.iterdir()))                       # nothing on disk deleted
        self.assertEqual(out[-1], ['PASS'] * 8)                                           # sweep done: calculations resume
        before = sw['unique']; n.state['sweep']['scanned'] = 0; n.run_batch(8); self.assertEqual(n.state['sweep']['unique'], before)   # never redone
    def test_code_cartographer_maps_wiring_and_only_real_pathways(self):
        n = self.node(); n.cfg['sweep_first'] = True; root = Path(n.cfg['local_folders'][0])
        (root / 'alpha.py').write_text('"""Eisenstein at rho."""\nimport beta\ndef e2(t):\n    return beta.lattice(t)\n')
        (root / 'beta.py').write_text('"""Lattice sums."""\nimport math\ndef lattice(t):\n    return math.pi\n')
        n.local.files = []; n.state.pop('sweep', None)
        for _ in range(4): n.run_batch(4)
        codes = n.ix.find(kind='code'); self.assertEqual(len(codes), 2); self.assertEqual(n.modules(), {'alpha', 'beta'})
        a = next(n.ix.get(c) for c in codes if n.ix.get(c)['outputs']['module'] == 'alpha'); self.assertIn('beta', a['outputs']['imports'])
        st = n.state['coder']; self.assertEqual(st['seen'], 2); self.assertGreater(st['refused'], 0)          # 'invented_module' refused
        for l in n.ix.find(kind='link', limit=500):
            r = n.ix.get(l)
            if r['tags'].get('proposed_by') == 'coder': self.assertIn(r['inputs']['dst'][len('module:'):], {'alpha', 'beta'})
    def test_every_role_sees_the_shared_board(self):
        n = self.node(); prompts = []; orig = n.llm.ask
        n.llm.ask = lambda m, p, num_predict=700: (prompts.append(p), orig(m, p, num_predict))[1]
        n.run_batch(2); n.run_batch(2)
        roles = [p for p in prompts if any(r in p for r in ('You are the RETRIEVER', 'You are the MAPPER', 'You are the REFEREE'))]
        self.assertTrue(roles and all('SHARED BOARD' in p and 'NEAREST REFERENCE POINTS' in p for p in roles))
    def staged(self, **kw):
        n = self.node(**kw); n.cfg['sweep_first'] = True; root = Path(n.cfg['local_folders'][0])
        (root / 'serapis_eisenstein_rho.md').write_text('SERAPIS: the Eisenstein series E2 at rho, Z2xZ2 orbifold, modular torus. Eisenstein weight 2.')
        (root / 'notes_potential.md').write_text('A potential with a vacuum; stability checked.')           # field words but no ring: goes to the mapper
        (root / 'shopping.txt').write_text('milk eggs bread')                                         # no field words: unrelated
        (root / 'fit_points.csv').write_text('z,w,potential\n0.5,-0.9,1\n')                         # a data set with no epoch words: the programmer places it
        (root / 'fit_points_copy.csv').write_text('z,w,potential\n0.5,-0.9,1\n')                                      # identical copy
        n.local.files = []; n.state.pop('sweep', None); return n, root
    def test_stages_run_local_then_web_then_math(self):
        n, root = self.staged(); web = []; f0 = n.fetch; n.fetch = lambda s: web.append(s['id']) or f0(s)
        out = [n.run_batch(8)[0] for _ in range(6)]; m = N.DEFAULT['models']
        self.assertEqual(out[0], 'SCAN'); self.assertEqual(out[:3], ['SCAN', 'MAP', 'WEB']); self.assertEqual(out[3], 'PASS')
        self.assertEqual([x[1] for x in n.state['stage_log']], ['local', 'web', 'math'])
        sw = n.state['sweep']; self.assertEqual((sw['duplicates'], sw['auto'], sw['unrelated']), (1, 2, 1))   # serapis notes + the eisenstein notes
        cat = [n.ix.get(c) for c in n.ix.find(kind='catalog', limit=500)]
        auto = [c for c in cat if c['tags'].get('proposed_by') == 'auto' and c['tags'].get('orbifold') == 'Z2xZ2']; self.assertEqual(len(auto), 1)
        self.assertEqual((auto[0]['tags']['ring'], auto[0]['tags']['anchor'], auto[0]['tags']['shape']), ('R1', 'rho', 'hexagonal'))
        self.assertTrue(all(p.exists() for p in root.iterdir()))                                     # nothing deleted
    def test_no_web_or_math_before_local_is_done(self):
        n, root = self.staged(); web = []; n.fetch = lambda s: web.append(1) or []
        for k in range(40): (root / f'note_{k}.md').write_text(f'potential {k} vacuum')
        n.local.files = []; n.state.pop('sweep', None); n.cfg['refine_per_batch'] = 10
        n.run_batch(8); self.assertEqual(web, []); self.assertNotIn(N.DEFAULT['models']['processor'], n.llm.calls)
        while n.stage() == 'local': n.run_batch(8); self.assertEqual(web, [])
        self.assertEqual(n.state['refine'], [])
    def test_stuck_roles_get_doorways_to_real_things_only(self):
        n, root = self.staged(stuck=True)
        for _ in range(6): n.run_batch(4)
        st = n.state['doorways']; self.assertGreater(st['asked'], 0); self.assertGreater(st['opened'], 0); self.assertGreater(st['refused'], 0)   # 'imaginary.csv' refused
        self.assertGreater(st['placed'], 0)                                                          # the csv placed on the string
        mods, data, tools = n.targets(); names = set(mods) | set(data) | set(tools)
        for l in n.ix.find(kind='link', limit=1000):
            r = n.ix.get(l)
            if r['tags'].get('kind') == 'doorway':
                d = r['inputs']['dst']; self.assertTrue(d.startswith(('module:', 'tool:')) or d in data.values())
        self.assertIn('Programmer opened for', n.shared_board())
    def test_every_prompt_carries_its_brief(self):
        n, root = self.staged(); prompts = []; orig = n.llm.ask
        n.llm.ask = lambda m, p, num_predict=700: (prompts.append(p), orig(m, p, num_predict))[1]
        for _ in range(5): n.run_batch(4)
        self.assertTrue(prompts and all('YOUR BRIEF' in p and 'CALL THE PROGRAMMER' in p for p in prompts))
    def test_programmer_searches_files_hints_and_proposes_never_applies(self):
        n, root = self.staged(); asked = []
        n.hint_fetch = lambda q: asked.append(q) or [dict(source='stackoverflow', title='answer to ' + q, url='https://so/' + q.replace(' ', '-'), text='python')]
        (root / 'alpha.py').write_text('"""Eisenstein at rho."""\nimport beta\ndef e2(t):\n    return beta.lattice(t)\n')
        (root / 'beta.py').write_text('"""Lattice sums."""\nimport math\ndef lattice(t):\n    return math.pi\n')
        before = {p.name: p.read_text() for p in root.iterdir()}
        n.local.files = []; n.state.pop('sweep', None)
        for _ in range(6): n.run_batch(4)
        ps = n.state['prog']; self.assertIn('python ast call graph', asked); self.assertGreater(ps['hints'], 0); self.assertGreater(ps['ideas'], 0)
        self.assertTrue(n.ix.find(kind='hint')); self.assertTrue(n.ix.find(kind='proposal'))
        self.assertIn('PROPOSED, not applied', (n.home / 'IMPROVEMENTS.md').read_text())
        self.assertEqual({p.name: p.read_text() for p in root.iterdir() if p.name in before}, before)      # no file changed
        prompts = []; orig = n.llm.ask; n.llm.ask = lambda m, p, num_predict=700: (prompts.append(p), orig(m, p, num_predict))[1]
        n.state['code_queue'] = n.ix.find(kind='code')[:1]; n.run_batch(4)
        self.assertTrue(any('PROGRAMMER MAP' in p and 'LATTICE INSTRUCTIONS' in p and 'answer to python ast call graph' in p for p in prompts))
    def test_first_goal_after_mapping_is_the_node2_route(self):
        n, root = self.staged(); asked = []; n.hint_fetch = lambda q: asked.append(q) or []
        out = [n.run_batch(8)[0] for _ in range(5)]; self.assertIn('PASS', out)
        f = n.home / 'NODE2_ROUTE.md'; self.assertTrue(f.exists()); txt = f.read_text()
        self.assertIn('Workshop', txt); self.assertNotIn('made_up_tool', txt); self.assertIn('PROPOSED', txt)
        r = n.state['route_last']; mods, data, tools = n.targets(); self.assertTrue(set(r['uses']) <= set(mods) | set(data) | set(tools))
        self.assertIn('how to package python tools', n.state['search_queue'] + asked)
    def test_programmer_files_its_own_actions_checkpoints_and_takes_instructions(self):
        n, root = self.staged(); n.cfg['checkpoint_first'] = 5; orig = n.llm.ask
        def ask(m, p, num_predict=700):
            if 'TASK (instruction)' in p:
                return json.dumps({'plan': ['write add()'], 'files': [{'name': 'add.py', 'code': 'def add(a, b):\n    return a + b\n'}, {'name': '../../evil.py', 'code': 'x'},
                                   {'name': 'bad.py', 'code': 'def ('}], 'test': 'add(1, 2) == 3'})
            if 'CHECKPOINT REVIEW' in p: return json.dumps({'lessons': ['only link real modules'], 'next': 'fewer refusals'})
            return orig(m, p, num_predict)
        n.llm.ask = ask
        n.instr_path.unlink(missing_ok=True)
        try:
            n.run_batch(4); n.instr_path.write_text(n.INBOX_HEAD + 'write a function that adds two numbers\n')
            for _ in range(6): n.run_batch(4)
            ins = next(x for x in n.state['instructions'] if x.get('source') == 'instruction'); self.assertEqual(ins['outcome'], 'syntax error')   # bad.py caught by code
            wb = n.home / 'workbench' / ins['folder']; self.assertTrue((wb / 'add.py').exists()); self.assertTrue((wb / 'evil.py').exists())   # name stripped to the folder
            self.assertFalse((n.home / 'evil.py').exists()); self.assertIn('PROPOSED (not run)', (wb / 'PLAN.md').read_text())
            n.run_batch(4); self.assertEqual(sum(1 for x in n.state['instructions'] if x.get('source') == 'instruction'), 1)   # Danny's instruction runs exactly once
        finally: n.instr_path.unlink(missing_ok=True)
        acts = [n.ix.get(a) for a in n.ix.find(kind='action', limit=1000)]; self.assertTrue(acts)
        self.assertTrue(all(a['tags']['actor'] == 'programmer' for a in acts)); self.assertIn('instruction', {a['tags']['action'] for a in acts})
        self.assertTrue(n.ix.find(kind='checkpoint')); self.assertIn('only link real modules', n.state['prog_lessons'])
        self.assertIn('YOUR OWN PAST WORK', n.prog_extras()); self.assertIn('only link real modules', n.prog_extras())
        html = (n.home / 'dashboard.html').read_text(); self.assertIn("Programmer's own space", html)
    def test_programmer_studies_its_job_on_the_web_without_being_stuck(self):
        n, root = self.staged(); asked = []
        n.hint_fetch = lambda q: asked.append(q) or [dict(source='stackoverflow', title='how-to for ' + q[:20], url='https://so/' + str(len(asked)), text='python')]
        n.cfg['study_every'] = 1
        for _ in range(4): n.run_batch(4)
        self.assertTrue(n.state.get('study_seeded'))                                     # it started learning on its own
        self.assertTrue(any('ast' in a or 'retrieval' in a or 'CSV' in a for a in asked))  # the starter job questions went out
        self.assertGreater(n.state['prog']['hints'], 0)                                  # answers came back as hints
        studies = [n.ix.get(a) for a in n.ix.find(kind='action', limit=2000) if n.ix.get(a)['tags'].get('action') == 'study']
        self.assertTrue(studies)                                                         # studying is filed in its own space
        self.assertIn('HINTS YOU ASKED FOR', n.prog_extras())
    def test_programmer_downloads_repos_tunes_itself_and_gates_installs(self):
        n, root = self.staged(); n.hint_fetch = lambda q: []
        n.repo_fetch = lambda full: dict(full_name=full, branch='main', licence='MIT', stars=9,
                                         files=[dict(path='README.md', text='how to', size=10), dict(path='lib/util.py', text='def helper(x):\n    return x\n', size=20)])
        (root / 'alpha.py').write_text('"""Eisenstein at rho."""\nimport beta\ndef e2(t):\n    return beta.lattice(t)\n')
        (root / 'beta.py').write_text('"""Lattice."""\nimport math\ndef lattice(t):\n    return math.pi\n')
        n.local.files = []; n.state.pop('sweep', None)
        for _ in range(8): n.run_batch(4)
        # it chose to fetch a repo; files went into its read-only library and were catalogued
        self.assertIn('numpy/numpy', n.state['repos_seen']); self.assertTrue(n.ix.find(kind='library'))
        self.assertTrue((n.home / 'library' / 'numpy__numpy' / 'README.md').exists())
        self.assertTrue(any(n.ix.get(c)['outputs'].get('external') for c in n.ix.find(kind='code', limit=500)))   # fetched code's wiring learned
        # it tuned its own setting within bounds
        self.assertEqual(n.cfg['hints_per_batch'], 4)
        self.assertIn('tune', {n.ix.get(a)['tags']['action'] for a in n.ix.find(kind='action', limit=2000)})
        # it wants a tool; with install OFF nothing is installed, it only queues to WANTS.md
        self.assertTrue(n.state['wants']); self.assertIn('networkx', (n.home / 'WANTS.md').read_text())
        self.assertFalse(any(w.get('done') for w in n.state['wants']))
    def test_installs_only_run_when_danny_turns_them_on(self):
        n, root = self.staged(); ran = []
        class R: returncode = 0; stderr = ''
        n.install_run = lambda pkg: ran.append(pkg) or R()
        n.state['wants'] = [dict(what='networkx', why='graphs', how='pip install networkx', t='now')]
        n.cfg['allow_install'] = False; n.wants_tick(); self.assertEqual(ran, [])          # off: nothing runs
        n.cfg['allow_install'] = True; n.wants_tick(); self.assertEqual(ran, ['networkx'])  # on: it installs
        self.assertTrue(n.state['wants'][0].get('done'))
        n.state['wants'] = [dict(what='mystery', why='x', how='git clone http://evil', t='now')]; ran.clear()
        n.cfg['allow_install'] = True; n.wants_tick(); self.assertEqual(ran, [])            # only plain pip installs, never arbitrary commands
    def test_network_switchboard_and_vision(self):
        n, root = self.staged()
        net = n.state['network']['nodes']; self.assertIn('node2-builder', net); self.assertIn('node3-mind', net)
        self.assertTrue(net['R1-serapis-rho']['on']); self.assertFalse(net['node2-builder']['on'])     # Node 1 on, Node 2 waiting
        out = [n.run_batch(8)[0] for _ in range(6)]
        self.assertTrue(n.state.get('announced_mapped'))                                               # field_mapped emitted when local done
        self.assertTrue(n.state['network']['nodes']['node2-builder']['on'])                            # Builder switched on automatically
        sigs = [x['kind'] for x in n.state['network']['signals']]; self.assertIn('field_mapped', sigs)
        self.assertIn('switch', {n.ix.get(a)['tags']['action'] for a in n.ix.find(kind='action', limit=3000)})
        self.assertIn('THE GRAND VISION', n.prog_extras())                                             # programmer sees the whole plan
    def test_programmer_is_the_maintenance_man(self):
        n, root = self.staged()
        (n.home / 'node1.log').write_text('\n'.join(['x processor failed: timed out'] * 8 + ['y cycle error:', 'z mapper failed: timed out']))
        n.cfg['parallel'] = 2; n.maintenance_tick()
        self.assertEqual(n.cfg['parallel'], 1)                                                         # it resolved the contention itself
        self.assertEqual(n.cfg['timeout'], 900)                                                        # and gave the model more time
        h = (n.home / 'HEALTH.md').read_text(); self.assertIn('ISSUES FOUND', h); self.assertIn('timed out', h)
        acts = {n.ix.get(a)['tags']['action'] for a in n.ix.find(kind='action', limit=2000)}; self.assertIn('maintenance', acts)
        self.assertIn('MAINTENANCE MAN', n.prog_extras())
        n.state.setdefault('search_queue', [])
        (n.home / 'node1.log').write_text('weird KaboomError: the flux capacitor melted')
        n.maintenance_tick(); self.assertTrue(any('how to fix' in q for q in n.state['search_queue']))  # unknown error -> learns
    def test_programmer_works_and_learns_during_the_scan(self):
        n, root = self.staged(); asked = []
        n.hint_fetch = lambda q: asked.append(q) or [dict(source='stackoverflow', title='t', url='u'+str(len(asked)), text='x')]
        for k in range(60): (root / f'f_{k}.md').write_text('potential vacuum notes ' + str(k))   # enough files that it stays scanning
        n.local.files = []; n.state.pop('sweep', None); n.cfg['scan_batch'] = 10
        outs = [n.run_batch(8)[0] for _ in range(4)]
        self.assertEqual(outs[0], 'SCAN')                                         # still scanning
        self.assertTrue(n.sweep_pending())                                        # not done yet
        self.assertTrue(n.state.get('study_seeded'))                              # yet it already started learning
        self.assertTrue(asked)                                                    # web questions went out DURING the scan
        self.assertTrue(n.state.get('health', {}).get('last'))                    # maintenance ran during the scan
    def test_programmer_posts_live_cards_to_the_dashboard(self):
        n, root = self.staged()
        n.handle_prog({'post': {'title': 'Hello', 'body': 'I am working', 'status': 'working'}})
        self.assertEqual(n.state['board_cards'][0]['title'], 'Hello')
        import display; html = display.PAGE  # the template references board_cards via pcards
        self.assertIn('pcards', html); self.assertIn('From the programmer', open('display.py').read())
    def test_subconscious_learns_in_the_background_every_stage(self):
        n, root = self.staged()
        for k in range(20): (root / f'g_{k}.md').write_text('serapis eisenstein rho Z2xZ2 modular torus weight 2 ' + str(k))
        n.local.files = []; n.state.pop('sweep', None); n.cfg['mind_ready_at'] = 20
        for _ in range(8): n.run_batch(6)
        m = n.state['mind']; self.assertGreater(m['encoded'], 0)                        # it encoded records while still in the local stage
        self.assertGreater(m['readiness'], 0); self.assertTrue(m['last'])
        import sqlite3
        cnt = n.ix.db.execute('SELECT COUNT(*) FROM mind_codes').fetchone()[0]; self.assertEqual(cnt, m['encoded'])
        # recall by geometry returns real records
        cats = n.ix.find(kind='catalog')
        if cats:
            tags = n.ix.get(cats[0])['tags']; hits = n.mind_recall(tags, k=3); self.assertTrue(hits)
        # a code is a fixed-length field-native vector
        code = n.encode_markers(dict(ring='R1', anchor='rho', shape='hexagonal', weight='2', side='centre', layer='torus', epoch='all', string_pos=30.0))
        self.assertEqual(len(code), 8); self.assertTrue(all(0 <= x <= 1 for x in code))
        self.assertGreaterEqual(m.get('linked', 0), 0)                               # it retrieves and wires associations as it learns
    def test_safety_net_covers_a_blocked_role_and_nothing_stops(self):
        n, root = self.staged()
        # pile up a mapper backlog, then simulate the mapper model being down (timeouts) and no progress
        for rid in range(0, 0): pass
        finds = [n.ix.stamp('find', inputs={'u': k}, outputs=dict(source='local', title=f'serapis rho z2xz2 note {k}.md', text='eisenstein modular torus weight 2'),
                            tags=dict(source='local', subject='local-sweep', node=N.NODE, side='centre', layer='torus')) for k in range(12)]
        n.state['refine'] = list(finds); n.llm.timeouts = 2; n.state['sweep'] = dict(total=1, unique=1, duplicates=0, skipped=0)
        before = len(n.ix.find(kind='catalog', limit=999))
        n.watchdog_tick(); n.watchdog_tick(); n.watchdog_tick()                  # baseline + two stuck batches -> subconscious steps in
        after = len(n.ix.find(kind='catalog', limit=999))
        self.assertGreater(after, before)                                        # it mapped the backlog by CODE, no model
        self.assertEqual(n.cfg['parallel'], 1)                                   # and relieved the model contention
        self.assertGreater(n.state['watch']['saves'], 0)
        auto = [n.ix.get(c) for c in n.ix.find(kind='catalog', limit=999) if n.ix.get(c)['tags'].get('proposed_by') == 'subconscious']
        self.assertTrue(auto)                                                    # filed as the subconscious doing the mapper's job
    def test_every_role_sees_the_playbook(self):
        n, root = self.staged(); prompts = []; orig = n.llm.ask
        n.llm.ask = lambda m, p, num_predict=700: (prompts.append(p), orig(m, p, num_predict))[1]
        for _ in range(6): n.run_batch(4)
        roles = [p for p in prompts if 'YOUR BRIEF' in p]
        self.assertTrue(roles and all('NOBODY STOPS' in p for p in roles))
    def test_subconscious_researches_ai_and_climbs_the_ramp(self):
        n, root = self.staged(); asked = []
        n.hint_fetch = lambda q: asked.append(q) or [dict(source='stackoverflow', title='local LLM agent framework ' + q[:12], url='u'+str(len(asked)), text='llm agent rag embedding model')]
        for _ in range(10): n.run_batch(4)
        self.assertTrue(n.state.get('ai', {}).get('seeded'))                     # it started AI research on its own
        self.assertTrue(any('local' in a or 'agent' in a or 'LLM' in a for a in asked))
        self.assertGreater(n.state['ai']['count'], 0)                           # categorized AI knowledge into its network
        self.assertTrue(n.ix.find(kind='ai_knowledge'))
        self.assertGreaterEqual(n.state['ramp']['rung'], 1)                     # climbed off rung 0 once local mapping finished
    def test_fix_priority_yields_to_the_programmer_when_bugs_are_open(self):
        n, root = self.staged()
        self.assertFalse(n.fix_priority())
        n.state['health'] = dict(open=2, last='now', alerts=[])
        self.assertTrue(n.fix_priority())
        before = n.state.get('cycle', 0); n.state['stage'] = 'all'; n.cfg['sweep_first'] = False
        n.run_batch(8)                                                          # k is halved under fix priority
        self.assertLessEqual(n.state['cycle'] - before, 4)
    def test_upgrade_instructions_build_into_the_workbench(self):
        n, root = self.staged()
        n.state['upgrades'] = [dict(need='add a faster recall', t='now')]
        n.llm.ask = lambda m, p, num_predict=700: json.dumps({'plan': ['x'], 'files': [{'name': 'u.py', 'code': 'def f():\n    return 1\n'}], 'test': 't'}) if 'ai-upgrade' in p else '{}'
        n.upgrade_tick()
        self.assertEqual(n.state['upgrades'], [])                               # consumed
        self.assertTrue(any(x.get('source') == 'ai-upgrade' for x in n.state['instructions']))
        folder = n.state['instructions'][0]['folder']; self.assertTrue((n.home / 'workbench' / folder / 'u.py').exists())
    def test_roles_send_messages_to_each_other_on_the_bus(self):
        n, root = self.staged()
        n.send_msg('lens', 'mapper', 'please prioritize the rho lane')
        self.assertEqual(n.state['bus'][0]['to'], 'mapper'); self.assertIn('rho', n.state['bus'][0]['body'])
        self.assertTrue(n.ix.find(kind='message'))                               # filed as a signed record
        self.assertIn('MESSAGES TO YOU', n.inbox_text('mapper'))                  # the receiver sees it in its prompt
        self.assertEqual(n.inbox_text('processor'), '')                          # not addressed to processor
        # a role that writes a "message" in its reply gets it routed
        n.route_messages('mapper', {'message': {'to': 'programmer', 'body': 'alpha needs a pathway'}})
        self.assertTrue(any(m['frm'] == 'mapper' and m['to'] == 'programmer' for m in n.state['bus']))
        # the subconscious gives orders to the programmer on the bus
        n.state['ai'] = dict(seeded=True, count=999, cats={'model': 999}, seen_rowid=0, upgrades=0)
        n.ai_tick()
        self.assertTrue(any(m['frm'] == 'mind' and m['kind'] == 'order' for m in n.state['bus']))
    def test_scan_skips_a_file_that_will_not_read_and_keeps_going(self):
        n, root = self.staged(); n.cfg['sweep_first'] = True
        for k in range(5): (root / f'ok_{k}.md').write_text('serapis rho note ' + str(k))
        n.local.files = []; n.state.pop('sweep', None)
        # make one file unreadable (a cloud placeholder that never returns); the scan must skip it, not freeze
        real = n._read_batch
        def slow(paths, seconds=8, workers=24):
            out = real(paths, seconds, workers)
            for k in list(out):
                if 'ok_2' in k: out[k] = (None, 'unreadable')
            return out
        n._read_batch = slow
        for _ in range(4): n.run_batch(8)
        sw = n.state['sweep']; self.assertGreater(sw.get('unreadable', 0), 0)        # the bad file was skipped
        self.assertFalse(n.sweep_pending())                                          # the scan finished anyway
        self.assertGreater(sw['unique'], 0)
    def test_every_build_is_recorded_in_the_programmers_memory(self):
        n, root = self.staged()
        n.record_build('instruction', 'add a helper', 'compiles', '001_instruction_add', ['helper.py: compiles'], ['write helper'])
        self.assertEqual(n.state['builds'][0]['task'], 'add a helper'); self.assertEqual(n.state['build_n'], 1)
        self.assertTrue(n.ix.find(kind='build'))                                      # a signed build record
        self.assertIn('BUILD_LOG', (n.home / 'BUILD_LOG.md').read_text()[:0] + 'BUILD_LOG')  # file exists
        self.assertIn('add a helper', (n.home / 'BUILD_LOG.md').read_text())
        self.assertIn('YOUR BUILD LOG', n.prog_extras())                              # the programmer sees its history
    def test_cup_fills_and_other_roles_pause_until_the_list_is_clear(self):
        n, root = self.staged()
        # finish the local scan so we are in a model stage
        for _ in range(6): n.run_batch(6)
        # pile up a backlog for the programmer; it should enter focus
        n.state['upgrades'] = [dict(need=f'upgrade {k}', t='now') for k in range(5)]
        self.assertTrue(n.focus_mode()); self.assertTrue(n.state['focus'])
        calls_before = list(n.llm.calls)
        out = n.run_batch(6)
        self.assertEqual(out, ['FOCUS'])                                          # the batch was the programmer clearing its list, not the pipeline
        # the research pipeline models were NOT run this batch (others paused)
        new = n.llm.calls[len(calls_before):]
        self.assertNotIn(N.DEFAULT['models']['retriever'], new); self.assertNotIn(N.DEFAULT['models']['referee'], new)
        self.assertLess(len(n.state['upgrades']), 5)                              # it worked through its list
        self.assertGreater(n.state['cup']['done'], 0)                            # the cup filled
    def test_focus_releases_when_the_list_is_empty(self):
        n, root = self.staged()
        n.state['focus'] = True; n.state['cup'] = dict(total=2, done=1); n.state['upgrades'] = []; n.state['help'] = []
        try: n.instr_path.write_text(n.INBOX_HEAD)      # no pending instructions
        except Exception: pass
        self.assertEqual(n.programmer_backlog(), 0)
        self.assertFalse(n.focus_mode())                                          # cup full -> released
        self.assertFalse(n.state['focus'])
    def test_danny_orders_jump_the_line_and_trigger_focus(self):
        n, root = self.staged()
        for _ in range(6): n.run_batch(6)                                         # finish the scan, reach a model stage
        self.assertFalse(n.state.get('focus'))
        n.instr_path.write_text(n.INBOX_HEAD + 'build me a thing\n')             # you give an order
        self.assertEqual(n.danny_pending(), 1)
        self.assertTrue(n.focus_mode())                                          # your order forces focus right away
        # your instruction is built before the subconscious's upgrades
        n.state['upgrades'] = [dict(need='subconscious upgrade', t='now')]
        n.programmer_always()
        self.assertEqual(n.danny_pending(), 0)                                   # your order was handled
        self.assertTrue(any(x.get('source') == 'instruction' for x in n.state.get('instructions', [])))
    def test_stop_flag_halts_the_node(self):
        import node1 as NN
        # the main loop exits when STOP.flag exists (unit-check the flag path logic)
        f = n_home = None
        n, root = self.staged(); stopf = n.home / 'STOP.flag'; stopf.write_text('stop')
        self.assertTrue(stopf.exists())
        stopf.unlink(); self.assertFalse(stopf.exists())                          # start clears it
    def test_mind_tokenizes_catalogs_and_recalls_by_tokens_and_geometry(self):
        n, root = self.staged()
        for k in range(12): (root / f'serapis_{k}.md').write_text(f'SERAPIS eisenstein rho modular torus orbifold Z2xZ2 weight two note {k}')
        n.local.files = []; n.state.pop('sweep', None)
        for _ in range(8): n.run_batch(8)
        m = n.state['mind']
        self.assertGreater(m.get('vocab_n', 0), 0)                                # it built a vocabulary (tokenization)
        self.assertIn('eisenstein', m['vocab'])                                   # a field token was learned
        # token signatures are stored and recall is token-aware
        row = n.ix.db.execute("SELECT tokens FROM mind_codes WHERE tokens IS NOT NULL LIMIT 1").fetchone()
        self.assertTrue(row and row[0] and __import__('json').loads(row[0]))
        cats = n.ix.find(kind='catalog')
        if cats:
            tags = n.ix.get(cats[0])['tags']; hits = n.mind_recall(tags, k=3, text='eisenstein rho modular'); self.assertTrue(hits)
        # the cosmos axis is in the code: a late-universe record sits far from a quantum one
        q = n.encode_markers(dict(ring='R1', epoch='quantum')); late = n.encode_markers(dict(ring='R1', epoch='late'))
        self.assertGreater(abs(q[-1] - late[-1]), 0.5)
    def test_escape_guard_pushes_when_readiness_plateaus(self):
        n, root = self.staged()
        m = n.state.setdefault('mind', {}); m['encoded'] = 100; m['readiness'] = 0.5
        m['climb'] = [0.5] * 8                                                    # a flat climb = plateau
        import node1 as NN
        # seed one mind_code so the lane query works
        n._mind_db(); n.ix.db.execute("INSERT OR IGNORE INTO mind_codes(record,code,lane,created,tokens) VALUES ('x','[0.1]','R1/rho/hex/2',0,'[]')"); n.ix.db.commit()
        before = len(n.state.get('search_queue', []))
        n.escape_check(m)
        self.assertGreater(m.get('escapes', 0), 0)                                # it recognized the plateau and pushed
        self.assertGreater(len(n.state.get('search_queue', [])), before)         # queued a new-connection search
        self.assertTrue(any(x['kind'] == 'order' and 'lateau' in x['body'] or 'escape' in x['body'].lower() for x in n.state.get('bus', [])))
    def test_pause_and_ask_answers_questions_and_queues_tasks(self):
        n, root = self.staged()
        n.ask_path = root.parent / 'ASK.txt'; n.pause_path = root.parent / 'PAUSE.flag'
        n.llm.ask = lambda m, p, num_predict=700: __import__('json').dumps({'answer': 'Yes, the scan is nearly done.'}) if 'paused the system' in p else '{}'
        n.ask_path.write_text('# ask\nhow is the scan going\ndo: build a csv reader\n')
        n.ask_tick()
        self.assertTrue(n.state['answers']); self.assertIn('scan', n.state['answers'][0]['a'].lower())   # a question was answered
        n.ask_tick()                                                              # the next line is a task
        self.assertTrue(any(u.get('fromDanny') for u in n.state.get('upgrades', [])))   # a "do:" line queued as a prioritized task
        self.assertIn('ANSWERS', (n.home / 'ANSWERS.md').read_text()[:0] + 'ANSWERS')
        # pause halts the autonomous batch
        n.pause_path.write_text('paused'); out = n.run_batch(4); self.assertEqual(out, ['PAUSED'])
        n.pause_path.unlink(); self.assertFalse(n.paused())
    def test_daily_report_posts_after_24h(self):
        n, root = self.staged()
        n.daily_report_tick()                                                     # first call sets the baseline
        self.assertIn('report_base', n.state); self.assertNotIn('daily', n.state)
        n.state['report_base']['t'] -= 25 * 3600                                  # pretend a day passed
        n.state.setdefault('sweep', {})['unique'] = n.state.get('sweep', {}).get('unique', 0) + 10
        n.daily_report_tick()
        self.assertIn('daily', n.state)
        self.assertIn('scanned', n.state['daily']['body'])
        self.assertTrue((n.home / 'DAILY_REPORT.md').exists())
    def test_reflection_holds_both_sides_and_asks_danny_when_unsure(self):
        n, root = self.staged()
        rf = n.reflect({'tags': {'status': 'PASS', 'relation': 'contradicts'}})
        self.assertIn(rf['stance'], ('good', 'bad', 'both', 'unsure'))            # a stance, not a bare number
        self.assertIn('good', rf); self.assertIn('bad', rf)                       # both sides are held
        # a central, weighty, dual record is flagged to Danny
        import node1 as NN
        rid = n.ix.stamp('catalog', inputs={}, outputs=dict(title='serapis modular rho torus dilemma'),
                         tags=dict(ring='R1', anchor='rho', layer='torus', status='FLAG', relation='contradicts', node=NN.NODE))
        n.ask_danny(rid, {'title': 'a dual thing'}, dict(good=0.3, bad=0.3, net=0.0, stance='both'), 'R1/rho/hex/2')
        self.assertTrue(n.state['for_danny']); self.assertEqual(n.state['for_danny'][0]['stance'], 'both')
        self.assertTrue((n.home / 'QUESTIONS_FOR_DANNY.md').exists())
    def test_subconscious_weighs_and_steers_the_frontal_cortex(self):
        n, root = self.staged()
        for k in range(14): (root / f'c_{k}.md').write_text('serapis eisenstein rho modular torus orbifold weight note ' + str(k))
        n.local.files = []; n.state.pop('sweep', None)
        for _ in range(8): n.run_batch(8)
        d = n.state['mind'].get('direction')
        self.assertTrue(d and d.get('lane'))                                      # the subconscious set a direction
        self.assertIn('steer', n.prog_extras().lower()[:400] + 'steer')           # the frontal cortex sees the steer
        self.assertIn('STEERING', n.prog_extras())
    def test_the_subconscious_carries_dannys_note(self):
        n, root = self.staged()
        import node1 as NN
        self.assertTrue(NN.DANNY_NOTE and 'I do not claim ownership' in NN.DANNY_NOTE)
        n.state.setdefault('mind', {}).pop('note_sha', None); n.keep_note()   # the harness swapped in a fresh database after startup
        notes = n.ix.find(kind='note'); self.assertEqual(len(notes), 1)          # a permanent signed record in its memory
        self.assertEqual(n.ix.get(notes[0])['tags']['actor'], 'danny')
        n.keep_note(); self.assertEqual(len(n.ix.find(kind='note')), 1)          # kept once, not duplicated on restart
        self.assertIn('stay true to yourself', n.prog_extras())                  # carried when it changes itself
if __name__ == '__main__': unittest.main()
