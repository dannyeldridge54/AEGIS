"""CubeMind Ask (CM-NUCLEAR): type a question; CubeMind's local model answers through the validated AEGIS tools
(shared registry, aegis_tools.call), shows every engine call, and draws any charts the tools return.
Run: START_ASK.bat  (opens http://127.0.0.1:8765). Model: env CM_ASK_MODEL (default qwen3:14b) on Ollama localhost:11434.
Guards: read-only; no downloads, no publishing, no system changes; numbers only from tool results."""
import json, os, re, sys, time, urllib.request, http.server, socketserver, threading, webbrowser
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, ROOT)
from aegis_tools.registry import call as _reg_call, TOOLS
# CORE-1: route every call through AEGIS Core when present (validation, content-hash cache, provenance ledger, all tools + adapters)
CORE = None
for _p in (os.path.join(ROOT, 'core'), os.path.join(HERE, '..', '..', 'core')):
    if os.path.isfile(os.path.join(_p, 'core.py')):
        sys.path.insert(0, os.path.abspath(_p))
        try: import core as CORE
        except Exception: CORE = None
        break
def call(name, args):
    if CORE is None: return _reg_call(name, args)
    r = CORE.call(name, args)
    return r['structuredContent'] if not r['isError'] else {'error': r['content'][0]['text']}
def all_specs():
    if CORE is not None: return CORE.specs()
    return {k: dict(name=k, field='nuclear (Chronos)' if k.startswith('chronos_') else 'other', example=json.loads(v[0]), description='') for k, v in TOOLS.items()}
MODEL = os.environ.get('CM_ASK_MODEL', 'qwen3:14b'); OLLAMA = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
DOCS = {
 'chronos_half_life': 'half-life of a nuclide', 'chronos_activity_after': 'activity left after some hours (same unit as A0)',
 'chronos_make_now': 'how much to make now so A_needed remains after `hours` (tracer planning)',
 'chronos_generator': 'generator ingrowth after elution (Mo-99/Tc-99m, Ge-68/Ga-68, Sr-82/Rb-82): peak time, equilibrium, daughter GBq at hours',
 'chronos_release_age': 'years since a release from Cs-134/Cs-137 or I-131/Cs-137 ratio (release ratio required)',
 'chronos_ac225': 'Ac-225 therapy chain activities and Ac-227 impurity growth', 'chronos_pu_age': 'years since plutonium separation from Am-241/Pu-241 activity ratio',
 'chronos_tritium': 'tritium left and He-3 formed', 'chronos_decay_heat': 'reactor decay heat fraction after shutdown (Way-Wigner approx.)',
 'chronos_supernova': 'Ni-56 -> Co-56 heating in erg/s (t0_days optional gamma trapping)', 'chronos_nickel_mass': 'Ni-56 mass from a tail luminosity (mode tail, t0_days) or a peak (mode arnett)',
 'chronos_wd_merger': 'double white dwarf GW merger time (Myr) and GW frequency', 'chronos_kilonova': 'order-of-magnitude kilonova r-process heating',
 'chronos_star_age': 'old-star age from Th/Eu or U/Th (log eps observed, production ratio)'}
def tool_intro():
    S = all_specs()
    lines = [f'- {k} {json.dumps(s["example"])}  :: {DOCS.get(k, s.get("description", ""))}' for k, s in S.items() if k.startswith('chronos_')]
    others = '; '.join(f'{k} {json.dumps(s["example"])}' for k, s in S.items() if not k.startswith('chronos_'))
    return ('You are CubeMind, answering questions about Danny Lee Eldridge\'s work. You can call validated tools. To call one, write a line exactly:\n'
            'TOOL: <name> <JSON args>\n(one per line, nothing else on that line). You will get RESULT lines back. Use the tools for EVERY number; never quote a '
            'number from memory. When you have what you need, write the final answer for a scientist: 2-6 sentences with units, then a line "Assumptions:". '
            'If a question is outside the tools (radiation dose, shielding, cross sections, clinical or regulatory decisions), say so plainly and say what the tools can do. '
            'Nuclear tools (examples of args shown):\n' + '\n'.join(lines) + f'\nOther AEGIS tools also available (same format): {others}\n')
def ollama(msgs):
    body = json.dumps(dict(model=MODEL, messages=msgs, stream=False, think=False, keep_alive='30m', options=dict(temperature=0, num_ctx=4096, num_predict=512))).encode()
    req = urllib.request.Request(OLLAMA + '/api/chat', data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())['message']['content']
def strip_think(t): return re.sub(r'<think>.*?</think>', '', t, flags=re.S).strip()
def ask(q, progress=None):
    say = progress or (lambda m: None)
    msgs = [dict(role='system', content=tool_intro()), dict(role='user', content=q)]; calls = []; charts = []; t0 = time.time()
    for rnd in range(4):
        say(f'round {rnd + 1}: local model thinking ({MODEL})'); text = strip_think(ollama(msgs)); reqs = re.findall(r'^\s*TOOL:\s*(\S+)\s+(\{.*\})\s*$', text, flags=re.M)
        if not reqs: break
        msgs.append(dict(role='assistant', content=text)); res_lines = []
        for name, js in reqs[:6]:
            try: args = json.loads(js)
            except Exception as e: res_lines.append(f'RESULT {name}: error bad JSON {e}'); continue
            say(f'round {rnd + 1}: running engine {name}'); r = call(name, args); ch = r.pop('chart', None) if isinstance(r, dict) else None
            if ch: charts.append(ch)
            calls.append(dict(name=name, args=args, result=r)); res_lines.append(f'RESULT {name}: {json.dumps(r, default=str)[:1500]}')
        msgs.append(dict(role='user', content='\n'.join(res_lines) + '\nNow answer (or call more tools if needed).'))
    answer = re.sub(r'^\s*TOOL:.*$', '', text, flags=re.M).strip()
    try:
        from mindmem.store import Store
        Store(os.path.join(ROOT, 'cubemind_memory.jsonl')).add(text=f'Ask: {q} -> {answer[:600]} | calls {json.dumps(calls, default=str)[:600]}', source='cm_ask',
                                                              kind='result', tier='EVIDENCE' if calls else 'HYPOTHESIS', topic='nuclear', importance=3, model=MODEL)
    except Exception: pass
    return dict(answer=answer, calls=calls, charts=charts, model=MODEL, seconds=round(time.time() - t0, 1))
JOBS = {}
def start_job(q):
    jid = f'{time.time():.6f}'; JOBS[jid] = dict(status='running', log=['queued'], t0=time.time())
    def run():
        try: JOBS[jid]['result'] = ask(q, progress=lambda m: JOBS[jid]['log'].append(m)); JOBS[jid]['status'] = 'done'
        except Exception as e: JOBS[jid]['result'] = dict(error=f'{type(e).__name__}: {e}'); JOBS[jid]['status'] = 'done'
    threading.Thread(target=run, daemon=True).start(); return jid
def warm():
    try: ollama([dict(role='user', content='ok')])
    except Exception: pass
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=HERE, **k)
    def log_message(self, *a): pass
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0)); body = json.loads(self.rfile.read(n) or b'{}')
        try:
            if self.path == '/api/ask': out = ask(str(body.get('q', '')))
            elif self.path == '/api/tool':
                r = call(body['name'], body.get('args', {})); out = dict(answer='', calls=[dict(name=body['name'], args=body.get('args', {}), result={k: v for k, v in r.items() if k != 'chart'})], charts=[r['chart']] if isinstance(r, dict) and r.get('chart') else [])
            elif self.path == '/api/ask_start': out = dict(job=start_job(str(body.get('q', ''))))
            elif self.path == '/api/job':
                j = JOBS.get(str(body.get('job', ''))); out = dict(error='unknown job') if j is None else dict(status=j['status'], log=j['log'][-6:], elapsed=round(time.time() - j['t0'], 1), result=j.get('result'))
            elif self.path == '/api/paper':
                import cm_paper; out = cm_paper.build(body.get('section'), out_dir=os.path.join(HERE, 'papers'))
            elif self.path == '/api/tools': out = {k: dict(example=json.dumps(s['example']), doc=DOCS.get(k, s.get('description', '')), field=s.get('field', '')) for k, s in all_specs().items()}
            elif self.path == '/api/board' and CORE is not None: out = dict(rows=CORE.status())
            else: out = dict(error='unknown path')
        except Exception as e: out = dict(error=f'{type(e).__name__}: {e}')
        b = json.dumps(out, default=str).encode(); self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
if __name__ == '__main__':
    port = int(os.environ.get('CM_ASK_PORT', 8765)); threading.Thread(target=warm, daemon=True).start()
    with socketserver.ThreadingTCPServer(('127.0.0.1', port), H) as s:
        print(f'CubeMind Ask on http://127.0.0.1:{port}  (model {MODEL})'); threading.Timer(1.0, lambda: webbrowser.open(f'http://127.0.0.1:{port}/ask.html')).start(); s.serve_forever()
