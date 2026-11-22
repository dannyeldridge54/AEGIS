#!/usr/bin/env python3
"""Target-acquisition data table (Danny 20:36). Modeled on OpenML's task / flow / run split, with MLflow-style params, metrics and
trajectories, and a verifier per task (as in benchmark registries and AlphaEvolve-style evaluators).
SQLite at field_tests/targets/targets.sqlite. Tables:
  tasks(task_id, family, statement, params_json, known_answer, verifier, difficulty, status, prize, source)
  flows(flow_id, engine, version, config_json)                       -- an engine + its exact config (git sha as version)
  runs(run_id, task_id, flow_id, seed, host, started, wall_s, steps, pulses, outcome, final_score, best_score, tts_s, verified, lock, notes)
  points(run_id, t_s, step, score, best, temp)                         -- score trajectory (for learning schedules)
  metrics(run_id, key, value)                                          -- any extra numbers (precision, recall, lens counts, ...)
Usage: track.py init | backfill | report"""
import json, os, re, sqlite3, subprocess, sys, time, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); DB = os.path.join(ROOT, 'field_tests/targets/targets.sqlite')
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks(task_id TEXT PRIMARY KEY, family TEXT, statement TEXT, params_json TEXT, known_answer TEXT, verifier TEXT, difficulty REAL, status TEXT, prize TEXT, source TEXT);
CREATE TABLE IF NOT EXISTS flows(flow_id TEXT PRIMARY KEY, engine TEXT, version TEXT, config_json TEXT);
CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, task_id TEXT, flow_id TEXT, seed INTEGER, host TEXT, started TEXT, wall_s REAL, steps INTEGER, pulses INTEGER,
  outcome TEXT, final_score REAL, best_score REAL, tts_s REAL, verified INTEGER, lock TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS points(run_id TEXT, t_s REAL, step INTEGER, score REAL, best REAL, temp REAL);
CREATE TABLE IF NOT EXISTS metrics(run_id TEXT, key TEXT, value REAL);
"""
def db():
    os.makedirs(os.path.dirname(DB), exist_ok=True); c = sqlite3.connect(DB); c.executescript(SCHEMA); return c
def sha():
    try: return subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
    except Exception: return 'unknown'
R3K = {4: 9, 5: 14, 6: 18, 7: 23, 8: 28, 9: 36}   # known R(3,K) (Radziszowski survey); R(3,10) in {40, 41}
def tasks():
    T = []
    for k, r in R3K.items():
        T.append(dict(task_id=f'ramsey_3_{k}_n{r-1}', family='ramsey', statement=f'triangle-free graph on {r-1} vertices with no independent {k}-set', params_json=json.dumps(dict(N=r - 1, K=k)),
                      known_answer='exists', verifier='tools/ramsey/verify.py', difficulty=r - 1, status='calibration', prize='', source='Radziszowski DS1'))
        T.append(dict(task_id=f'ramsey_3_{k}_n{r}', family='ramsey', statement=f'triangle-free graph on {r} vertices with no independent {k}-set', params_json=json.dumps(dict(N=r, K=k)),
                      known_answer='impossible', verifier='tools/ramsey/verify.py', difficulty=r, status='calibration-negative', prize='', source='Radziszowski DS1'))
    T.append(dict(task_id='ramsey_3_10_n39', family='ramsey', statement='triangle-free graph on 39 vertices, independence < 10', params_json=json.dumps(dict(N=39, K=10)), known_answer='exists (Exoo)',
                  verifier='tools/ramsey/verify.py', difficulty=39, status='calibration', prize='', source='arXiv 2401.00392'))
    T.append(dict(task_id='ramsey_3_10_n40', family='ramsey', statement='triangle-free graph on 40 vertices, independence < 10 (would prove R(3,10)=41)', params_json=json.dumps(dict(N=40, K=10)),
                  known_answer='open', verifier='tools/ramsey/verify.py', difficulty=40, status='target', prize='new result (no cash prize)', source='arXiv 2401.00392'))
    T.append(dict(task_id='loom_woven_field', family='loom', statement='woven-field scored run: bars A1-A5 on 61 goalposts', params_json='{}', known_answer='bars', verifier='tools/loom/loom_rt5.py scored',
                  difficulty=None, status='engine', prize='', source='PREREG_D1986-D1996'))
    T.append(dict(task_id='loom_replay', family='loom', statement='real-data replay: MATERIAL recall/specificity', params_json='{}', known_answer='bars', verifier='tools/loom/loom_rt5.py replay',
                  difficulty=None, status='engine', prize='', source='PREREG_D1994'))
    T.append(dict(task_id='mersenne_pattern', family='pattern', statement='pattern beyond LPW in Mersenne exponents', params_json='{}', known_answer='LPW', verifier='theory/tests/d1999_mersenne.py',
                  difficulty=None, status='done', prize='GIMPS $3,000 per new prime (not this task)', source='PREREG_D1999'))
    return T
def init():
    c = db()
    for t in tasks(): c.execute('INSERT OR REPLACE INTO tasks VALUES (:task_id,:family,:statement,:params_json,:known_answer,:verifier,:difficulty,:status,:prize,:source)', t)
    c.execute('INSERT OR REPLACE INTO flows VALUES (?,?,?,?)', ('r310_sa_v1', 'tools/ramsey/r310.c', sha(), json.dumps(dict(T0=2.0, cool=0.97, every=20000, Tmin=0.05, move='add edge in an independent K-set, cut one edge per common neighbour'))))
    c.execute('INSERT OR REPLACE INTO flows VALUES (?,?,?,?)', ('loom_rt5_confirm', 'tools/loom/loom_rt5.py', sha(), json.dumps(dict(B=[0.16, 20], C=[0.08, 40], confirm=200, vclock=1 / 4300))))
    c.commit(); return c
def log_run(c, **r):
    keys = ['run_id', 'task_id', 'flow_id', 'seed', 'host', 'started', 'wall_s', 'steps', 'pulses', 'outcome', 'final_score', 'best_score', 'tts_s', 'verified', 'lock', 'notes']
    c.execute('INSERT OR REPLACE INTO runs VALUES (%s)' % ','.join('?' * len(keys)), [r.get(k) for k in keys])
PROG = re.compile(r'seed (\d+) t=(\d+)s steps (\d+) pulses (\d+) score (\d+) best (\d+) T ([\d.]+)')
DONE = re.compile(r'seed (\d+) done steps (\d+) pulses (\d+) final (\d+) best (\d+)')
def verify(N, K, sd):
    f = f'tools/ramsey/out_{N}_{K}_{sd}.txt'
    if not os.path.exists(f) or 'FOUND' not in open(f).read(): return 0
    g = open(f).read().split()[-1]
    r = subprocess.run([sys.executable, 'tools/ramsey/verify.py', g, str(K)], capture_output=True, text=True, cwd=ROOT); return 1 if r.returncode == 0 else 0
def backfill():
    c = init(); n = 0
    res = {}
    if os.path.exists('tools/ramsey/ladder_results.txt'):
        for l in open('tools/ramsey/ladder_results.txt'):
            m = re.match(r'N=(\d+) K=(\d+) seed=(\d+) found=(\w+) secs=([\d.]+)', l)
            if m: res[(int(m[1]), int(m[2]), int(m[3]))] = (m[4] == 'yes', float(m[5]))
    for f in glob.glob('tools/ramsey/log_*_*_*.txt'):
        N, K, sd = map(int, re.findall(r'log_(\d+)_(\d+)_(\d+)', f)[0]); txt = open(f).read(); rid = f'r310_{N}_{K}_{sd}'
        c.execute('DELETE FROM points WHERE run_id=?', (rid,))
        for m in PROG.finditer(txt): c.execute('INSERT INTO points VALUES (?,?,?,?,?,?)', (rid, float(m[2]), int(m[3]), float(m[5]), float(m[6]), float(m[7])))
        d = DONE.search(txt); found, secs = res.get((N, K, sd), (None, None))
        last = list(PROG.finditer(txt))
        log_run(c, run_id=rid, task_id=f'ramsey_3_{K}_n{N}', flow_id='r310_sa_v1', seed=sd, host='cloud', started=None, wall_s=secs if secs else (float(last[-1][2]) if last else None),
                steps=int(d[2]) if d else (int(last[-1][3]) if last else None), pulses=int(d[3]) if d else (int(last[-1][4]) if last else None),
                outcome=('found' if found else 'not found') if d else 'running', final_score=float(d[4]) if d else (float(last[-1][5]) if last else None),
                best_score=float(d[5]) if d else (float(last[-1][6]) if last else None), tts_s=secs if found else None, verified=verify(N, K, sd) if found else None, lock='PREREG_D1998', notes=None); n += 1
    for f in sorted(glob.glob('field_tests/results/d199[1-6]_*.json')) + sorted(glob.glob('field_tests/results/auto/round_*_20*.json')):
        try: o = json.load(open(f))
        except Exception: continue
        runs = o.get('runs') if isinstance(o.get('runs'), list) else [o]
        for r in runs:
            if 'accuracy' not in r: continue
            rid = 'loom_%s_%s' % (os.path.basename(f).replace('.json', ''), r.get('seed'))
            log_run(c, run_id=rid, task_id='loom_woven_field', flow_id='loom_rt5_confirm', seed=r.get('seed'), host='cloud', started=None, wall_s=r.get('wall_seconds'), steps=r.get('pulses'), pulses=None,
                    outcome=r.get('verdict'), final_score=sum(1 for v in r['accuracy'].values() if v), best_score=None, tts_s=None, verified=1, lock=o.get('prereg'), notes=json.dumps(r['accuracy']))
            c.execute('DELETE FROM metrics WHERE run_id=?', (rid,))
            for k, v in (('pulses_per_s', r.get('pulses_per_s')), ('precision_fast', (r.get('precision') or [None])[0] if 'precision' in r else r.get('precision_fast'))):
                if isinstance(v, (int, float)): c.execute('INSERT INTO metrics VALUES (?,?,?)', (rid, k, v))
            n += 1
    c.commit(); return n
def report():
    c = db(); out = {}
    q = c.execute("""SELECT t.task_id, t.difficulty, t.known_answer, COUNT(r.run_id), SUM(r.outcome='found'), AVG(CASE WHEN r.outcome='found' THEN r.tts_s END), MIN(r.best_score)
                     FROM tasks t LEFT JOIN runs r ON r.task_id=t.task_id WHERE t.family='ramsey' GROUP BY t.task_id ORDER BY t.difficulty""").fetchall()
    out['ramsey_calibration'] = [dict(task=a, N=b, known=k, runs=n, found=f or 0, mean_tts_s=round(m, 2) if m else None, best_score=s) for a, b, k, n, f, m, s in q if n]
    q = c.execute("SELECT outcome, COUNT(*) FROM runs WHERE task_id='loom_woven_field' GROUP BY outcome").fetchall(); out['loom_runs'] = dict(q)
    neg = c.execute("SELECT t.task_id, COUNT(r.run_id), SUM(r.outcome='found') FROM tasks t JOIN runs r ON r.task_id=t.task_id WHERE t.known_answer='impossible' GROUP BY t.task_id").fetchall()
    out['negative_controls'] = [dict(task=a, runs=b, false_finds=f or 0) for a, b, f in neg]
    out['verified_finds'] = c.execute("SELECT COUNT(*) FROM runs WHERE outcome='found' AND verified=1").fetchone()[0]
    out['unverified_finds'] = c.execute("SELECT COUNT(*) FROM runs WHERE outcome='found' AND (verified IS NULL OR verified=0) AND task_id LIKE 'ramsey%'").fetchone()[0]
    fl = [(r['N'], r['mean_tts_s']) for r in out['ramsey_calibration'] if r['mean_tts_s']]
    if len(fl) >= 3:
        import math
        xs = [a for a, b in fl]; ys = [math.log(b) for a, b in fl]; mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); out['tts_scaling'] = dict(log_tts_per_vertex=round(slope, 3), doubling_every_vertices=round(math.log(2) / slope, 2) if slope > 0 else None,
            extrapolated_tts_s={str(n): round(math.exp(my + slope * (n - mx)), 1) for n in (35, 39, 40)},
            warning='fit on solved rungs only; a rung still unsolved past its extrapolated time means hardness grows faster than exponential and the extrapolation is invalid')
    return out
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'report'
    if cmd == 'init': init(); print('ok')
    elif cmd == 'backfill': print('rows', backfill())
    else: print(json.dumps(report(), indent=1))
