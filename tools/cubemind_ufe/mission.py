"""CubeMind mission targets (after mastery). Each step: a face proposes, the proposal is LOCKED (sha256 in the ledger), then scored.
M1 Hutter knobs: propose fader/learning-rate settings for the Loom compressor; scored by the real compressed size of a fixed slice.
M2 Ramsey R(3,10): propose a two-circulant 40-vertex graph; scored mechanically (triangle-free? largest independent set <= 9?).
M3 Postulates on the big open problems: placed in the UFE field; recorded as POSTULATE (no claim) for the referee (Claude) to lock and test.
Every piece examined fits somewhere in the field: say where, and say honestly when it does not."""
import json, os, re, hashlib, subprocess, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); TOOLS = os.path.join(ROOT, 'ufe_tools')
LEDGER = os.path.join(ROOT, 'proposals_ledger.jsonl'); STATE = os.path.join(HERE, 'data', 'mission_state.json')
from .ufe_lens import LENS
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def log(rec):
    with open(LEDGER, 'a') as f: f.write(json.dumps(rec) + '\n')
def load():
    try: return json.load(open(STATE))
    except Exception: return {'hutter_best': None, 'hutter_best_knobs': None, 'ramsey_best': None, 'n': 0}
def save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True); json.dump(s, open(STATE, 'w'), indent=1)
PROTOCOL = open(os.path.join(ROOT, 'CUBEMIND_KNOB_PROTOCOL.md'), encoding='utf-8').read()[:3000] if os.path.exists(os.path.join(ROOT, 'CUBEMIND_KNOB_PROTOCOL.md')) else ''
def hutter(face, s):
    prompt = (LENS + PROTOCOL + '\nTASK M1 (Hutter): propose ONE knob setting for the Loom compressor as JSON on one line: '
              '{"GAINS":[15 numbers, node order o0,o1,o2,o3,o4,o5,o6,mlit,word,wpair,class,column,ltype,markup,stack], "LR1":1-6, "EV":0 or 1}. '
              f'Current best: {s.get("hutter_best_knobs")} -> {s.get("hutter_best")} bytes. Change one knob at a time like tuning an instrument.\nJSON:')
    raw = face.ask(prompt); m = re.search(r'\{.*\}', raw, flags=re.S)
    try: k = json.loads(m.group(0)); gains = [float(x) for x in k['GAINS']][:15]; lr = int(k.get('LR1', 3)); ev = int(k.get('EV', 1))
    except Exception: return {'task': 'M1', 'valid': False, 'raw': raw[:200]}
    gains = [min(4.0, max(0.0, x)) for x in gains] + [1.0] * (15 - len(gains)); lr = min(6, max(1, lr))
    lock = sha(json.dumps([gains, lr, ev])); log({'t': time.time(), 'kind': 'M1_lock', 'sha256': lock})
    env = dict(os.environ, LR1=str(lr), CLASSMAP=os.path.join(TOOLS, 'DIR_ONE.map'), MASK=str(0x12ffff), GAINS=','.join('%g' % x for x in gains))
    if ev: env['EV'] = '1'
    exe = os.path.join(TOOLS, 'loomz.exe' if os.name == 'nt' else 'loomz_linux'); out = os.path.join(TOOLS, 'm1.lmz')
    r = subprocess.run([exe, 'c', os.path.join(TOOLS, 'tune_slice.txt'), out], env=env, capture_output=True, text=True)
    size = int(re.search(r'out (\d+)', r.stderr).group(1)) if 'out ' in r.stderr else None
    better = size is not None and (s['hutter_best'] is None or size < s['hutter_best'])
    if better: s['hutter_best'], s['hutter_best_knobs'] = size, {'GAINS': gains, 'LR1': lr, 'EV': ev}
    rec = {'task': 'M1', 'sha256': lock, 'size': size, 'new_best': better}; log(dict(rec, kind='M1_score', t=time.time())); return rec
def _alpha(adj, n):
    best = 0
    def rec(size, cand):
        nonlocal best
        if size + bin(cand).count('1') <= best: return
        if not cand: best = size; return
        v = (cand & -cand).bit_length() - 1
        rec(size + 1, cand & ~adj[v] & ~(1 << v)); rec(size, cand & ~(1 << v))
    rec(0, (1 << n) - 1); return best
def ramsey(face, s):
    prompt = (LENS + '\nTASK M2 (Ramsey R(3,10), open: 40 <= R <= 41): a triangle-free graph on 40 vertices with no independent set of 10 '
              'proves R(3,10) = 41. Known: no circulant works, the degree-4 case is impossible (D2003), min degree >= 5. Propose a TWO-CIRCULANT: '
              'vertices (i,0),(i,1) for i in Z20; A = distances inside layer 0, B = inside layer 1, C = cross offsets (i,0)~(i+c,1). '
              'Reply one line of JSON {"A":[..],"B":[..],"C":[..]} with distances in 1..10 for A,B and 0..19 for C.\nJSON:')
    raw = face.ask(prompt); m = re.search(r'\{.*\}', raw, flags=re.S)
    try: k = json.loads(m.group(0)); A = sorted({int(x) % 20 for x in k['A']} - {0}); B = sorted({int(x) % 20 for x in k['B']} - {0}); C = sorted({int(x) % 20 for x in k['C']})
    except Exception: return {'task': 'M2', 'valid': False}
    lock = sha(json.dumps([A, B, C])); log({'t': time.time(), 'kind': 'M2_lock', 'sha256': lock, 'A': A, 'B': B, 'C': C})
    n = 40; adj = [0] * n
    def e(u, v): adj[u] |= 1 << v; adj[v] |= 1 << u
    for i in range(20):
        for d in A: e(i, (i + d) % 20)
        for d in B: e(20 + i, 20 + (i + d) % 20)
        for c in C: e(i, 20 + (i + c) % 20)
    tri = any(adj[u] & adj[v] for u in range(n) for v in range(u) if adj[u] >> v & 1)
    al = None if tri else _alpha(adj, n); ok = (not tri) and al <= 9
    rec = {'task': 'M2', 'sha256': lock, 'triangle_free': not tri, 'alpha': al, 'R310_witness': ok}
    if ok: rec['ALERT'] = 'CANDIDATE WITNESS: re-verify with ramsey/verify.py before any claim'
    if not tri and (s['ramsey_best'] is None or al < s['ramsey_best']): s['ramsey_best'] = al
    log(dict(rec, kind='M2_score', t=time.time())); return rec
PROBLEMS = ['Yang-Mills mass gap', 'Navier-Stokes smoothness', 'Riemann hypothesis', 'P vs NP', 'Hodge conjecture', 'Birch and Swinnerton-Dyer',
            'the cosmological constant problem', 'the Hubble tension', 'the nature of dark matter', 'the strong CP problem', 'the matter-antimatter asymmetry']
def postulate(face, s):
    p = PROBLEMS[s['n'] % len(PROBLEMS)]
    raw = face.ask(LENS + f'\nTASK M3: place "{p}" in the UFE field. Which field or interface (S, T, U, S-T, T-U, S-U, or NONE) does it live on, '
                   'what would the field predict, and what single test could falsify that? Label it POSTULATE. Be honest if it does not fit.\nANSWER:')
    lock = sha(raw); rec = {'t': time.time(), 'kind': 'M3_postulate', 'problem': p, 'sha256': lock, 'text': raw[:2000], 'status': 'POSTULATE - needs referee'}
    log(rec); return {'task': 'M3', 'problem': p, 'sha256': lock}
def step(faces, k):
    s = load(); s['n'] += 1; face = list(faces.values())[k % len(faces)]
    task = (hutter, ramsey, postulate)[s['n'] % 3]; rec = task(face, s); save(s); return rec
