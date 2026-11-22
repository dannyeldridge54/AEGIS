#!/usr/bin/env python3
"""D1989 engine v4 (physical bounds, STUCK rule, fit-aware scorer, quiet-window fix, real-data replay; PREREG_D1989). Derived from D1987 engine v3 (two detectors: exact residual test for deterministic margins, self-normalised CUSUM for data margins; PREREG_D1987). Derived from D1986 engine v2: the woven field (PREREG_D1986_woven_field.md + DEVIATIONS). One process; every pulse runs layers 1->9 in order.
Each layer's referee: triangulates its data (median of 3/5 readings), sorts margins IN/PULL/OUT, tracks resonance with hysteresis (3 in, 3 out),
detects unexplained shifts with a CUSUM on whitened residuals, balances on its free, BOUNDED knobs (split visible), feeds the next layer in
the same pulse, and scores the node's goalposts (tools/loom/goalposts.json) live. A population of shadow detectors tunes the live detector
online on self-injected probes (never on the scored events). Usage:
  python3 tools/loom/loom_rt2.py calibrate        # O2: 5 training seeds x 5 s, no events, 12 configs
  python3 tools/loom/loom_rt2.py run [seconds]    # O4: scored blind run, seed 2026"""
import json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); os.chdir(ROOT)
_ns = {}; exec(open('tools/loom/resonance.py').read().split("out = {'sweeps'")[0], _ns)
obs, margins_ref, D, LOG, m_phi = _ns['obs'], _ns['margins'], _ns['D'], _ns['LOG'], _ns['m_phi']
K = ['u', 'MN', 'm32', 'TR', 'split']; NK = 5; IS = K.index('split')
LO = np.array([math.log(0.02588 / D['u']), math.log(4.5e10 / D['MN']), -math.log(3), math.log(5e-3 / D['TR']), -math.log(3)])   # D1989 P1.4 physical bounds
HI = np.array([math.log(0.02740 / D['u']), math.log(2.5e12 / D['MN']), math.log(3), math.log(m_phi / D['TR']), math.log(3)])
DEP = {'as': {'m32', 'split'}, 'M2': {'m32'}, 'Y': {'TR', 'MN'}, 'Om': {'TR', 'm32'}, 'ns': {'TR'}, 'u': {'u'}, 'rung': {'u'}, 'MN': {'MN'}}
NOM = dict(ns=0.9728, as_=0.1180, lep=0.0253, wino=700.0, Y=0.87e-10)
SIG = dict(ns=0.0027, as_=0.00107, lep=0.0003, wino=20.0, Y=0.0087e-10)
STREAM_OF = {4: ['lep'], 5: ['wino'], 6: ['ns'], 7: ['as_'], 8: ['Y']}
HELD = {'u'}; PHI = 0.95
def margins_rt(st, T):
    o = obs(st); rung = [o['u'], T['lep'], math.exp(-9 * math.pi / 8)]
    return {1: dict(quark_window=min(math.log(o['u'] / 0.02588), math.log(0.02740 / o['u']))),
            2: dict(nu_ratio=math.log(1.33), MN_top=math.log(2.5e12 / o['MN']), MN_bottom=math.log(o['MN'] / 4.5e10)), 3: {},
            4: dict(rung_agreement=math.log(1.15) - math.log(max(rung) / min(rung))),
            5: dict(wino=math.log(o['M2'] / T['wino'])),
            6: dict(n_s=2 - abs((o['ns'] - T['ns']) / 0.0027)),
            7: dict(alpha_s=2 - abs((o['a_s'] - T['as_']) / math.hypot(0.0009, 0.00057)), split_natural=math.log(3) - abs(o['split'])),
            8: dict(gravitino_box=math.log(0.12 / o['Om']), leptogenesis=math.log(o['Y'] / T['Y'])), 9: {}}
def state(x): return {k: (D[k] * math.exp(x[i]) if k in LOG else D[k] + x[i]) for i, k in enumerate(K)}
def flat(M): return np.array([M[L][a] for L in range(1, 10) for a in sorted(M[L])])
IDX = {}; _i = 0
for _L in range(1, 10):
    for _a in sorted(margins_rt(state(np.zeros(NK)), NOM)[_L]): IDX.setdefault(_L, []).append(_i); _i += 1
NM = _i; LAYER_OF = {i: L for L, ii in IDX.items() for i in ii}
NAMES = [a for L in range(1, 10) for a in sorted(margins_rt(state(np.zeros(NK)), NOM)[L])]
DET_NAMES = {'quark_window', 'MN_bottom', 'MN_top', 'nu_ratio', 'split_natural', 'gravitino_box'}
DET = np.array([i for i, n in enumerate(NAMES) if n in DET_NAMES]); STO = np.array([i for i, n in enumerate(NAMES) if n not in DET_NAMES])
def jac(x, T, h=1e-5, hs=0.05):
    J = np.zeros((NM, NK)); f0 = flat(margins_rt(state(x), T))
    for j in range(NK):
        if j == IS:   # forward finite step: the split FIT switch is visible (D1985 F3)
            s = hs if x[j] + hs <= HI[j] else -hs; e = np.zeros(NK); e[j] = s; J[:, j] = (flat(margins_rt(state(x + e), T)) - f0) / s
        else:
            e = np.zeros(NK); e[j] = h; J[:, j] = (flat(margins_rt(state(x + e), T)) - flat(margins_rt(state(x - e), T))) / (2 * h)
    return J
def lens_knobs(J, L):
    if L not in IDX: return None, 0
    Jl = J[IDX[L]]; s = np.linalg.svd(Jl, compute_uv=False)
    r = int((s > 1e-3 * s.max()).sum()) if s.max() > 0 else 0
    if r == 0: return set(), 0
    vt = np.linalg.svd(Jl)[2][:r]; return {K[i] for i in range(NK) if np.abs(vt[:, i]).max() > 0.1}, r
# ---------------- goalposts
GP = json.load(open('tools/loom/goalposts.json'))['goalposts']
def live_value(key, st, est, Mcur):
    o = obs(st)
    return {'u': o['u'], 'MN': o['MN'], 'M2': o['M2'], 'ns': o['ns'], 'as': o['a_s'], 'Y': o['Y'], 'Om': o['Om'],
            'rung': float(Mcur[IDX[4][0]])}[key]
LIVE_DATA = {'ns': ('ns', 0.0027), 'as': ('as_', 0.0009), 'M2': ('wino', None), 'Y': ('Y', None)}
def score(gp, st=None, est=None, Mcur=None):
    d = gp['data']; w = gp['weave']['value']
    if gp['live']:
        w = live_value(gp['live'], st, est, Mcur)
        if gp['live'] in LIVE_DATA:
            k, s = LIVE_DATA[gp['live']]; d = dict(d)
            if d['type'] == 'band': d['value'] = est[k]
            if d['type'] == 'lower': d['limit'] = est[k]
    t = d['type']
    if gp['kind'] == 'OPEN' or w is None or isinstance(w, str) or t == 'none':
        st_ = 'OPEN' if (gp['kind'] == 'OPEN' or w is None) else 'UNSCORED'; return st_, None
    if t == 'internal': r = 'PASS' if w >= 0 else 'FAIL'; v = w
    elif t == 'band':
        if not d.get('sigma'): return 'UNSCORED', None
        v = (w - d['value']) / d['sigma']; r = 'PASS' if abs(v) <= 2 else 'TENSION' if abs(v) <= 3 else 'FAIL'
    elif t == 'upper': v = w / d['limit'] if d['limit'] else w; r = 'PASS' if w < d['limit'] else 'FAIL'
    elif t == 'lower': v = w / d['limit']; r = 'PASS' if w > d['limit'] else 'FAIL'
    elif t == 'window': v = w; r = 'PASS' if d['lo'] <= w <= d['hi'] else 'FAIL'
    else: return 'UNSCORED', None
    return r, v
def label(gp, r):
    if r in ('OPEN', 'UNSCORED'): return r
    return {'PRED': r, 'FIT': r + ' (FIT)', 'NULL': r + ' (null)', 'TRUST': 'TRUST', 'BOUND': r + ' (bound)', 'OPEN': 'OPEN'}[gp['kind']]
# ---------------- detectors (CUSUM bank on whitened residuals)
class Bank:
    def __init__(s, ks, hs): s.k = np.array(ks, float)[:, None]; s.h = np.array(hs, float)[:, None]; s.Sp = np.zeros((len(ks), NM)); s.Sn = np.zeros((len(ks), NM))
    def step(s, w):
        s.Sp = np.maximum(0, s.Sp + w[None, :] - s.k); s.Sn = np.maximum(0, s.Sn - w[None, :] - s.k)
        al = (s.Sp > s.h) | (s.Sn > s.h); s.Sp[al] = 0; s.Sn[al] = 0; return al
GRID = [(k, h) for k in (0.08, 0.16, 0.25) for h in (12, 20, 30, 40, 60)]
EVENTS = [dict(name='E1 n_s +3 sigma', t0=10, t1=20, kind='data', key='ns', f=lambda v: v + 3 * SIG['ns'], pred={6}),
          dict(name='E2 m3/2 x1.05 kick', t0=25, t1=35, kind='knob', key='m32', dx=math.log(1.05), pred=None),
          dict(name='E3 Y_B -30 %', t0=45, t1=55, kind='data', key='Y', f=lambda v: v * 0.7, pred={8})]
QUIET = [(2, 10), (20.5, 25), (35.5, 45), (55.5, 60)]
E2T = [24.0, 25.0, 35.0]   # prediction time, kick, revert
SC = {'WINDOW': 0, 'OPAQUE': 1, 'NO LOCK': 2, 'RESONANT': 3, 'LOST': 4, 'STUCK': 5}
def engine(T_total, seed, events=True, live_cfg=(1.0, 16), calib=False, pbt=True, verbose=False, replay=None):
    rng = np.random.default_rng(seed); srng = np.random.default_rng(seed + 7919)
    x = np.zeros(NK); est = dict(NOM); J = jac(x, NOM); lensK = {L: lens_knobs(J, L) for L in range(1, 10)}
    M0 = flat(margins_rt(state(x), est)); base = M0.copy(); var = np.full(NM, 1e-4); zprev = np.zeros(NM); med = np.full(NM, 0.6745); Mlast = M0.copy(); armA = np.ones(NM, bool); calA = 0
    live = Bank([live_cfg[0]], [live_cfg[1]]); live_cfg = list(live_cfg)
    shadows = [list(c) for c in ((0.08, 40), (0.16, 30), (0.16, 40), (0.25, 30))]; sh = Bank(*zip(*shadows)); sh_stats = np.zeros((4, 3))  # delay sum, n probes, false alarms
    cb = Bank(*zip(*GRID)) if calib else None; cbp = Bank(*zip(*GRID)) if calib else None; cal = np.zeros((len(GRID), 4))  # FA, delay sum, n, misses
    probe = None; cprobe = None
    ok_run = {L: 0 for L in range(1, 10)}; bad_run = {L: 0 for L in range(1, 10)}; res_since = {L: None for L in range(1, 10)}
    status = {L: ('WINDOW' if L not in IDX else 'NO LOCK') for L in range(1, 10)}
    esc = {L: 0 for L in range(1, 10)}; clean = {L: 0 for L in range(1, 10)}; throttle = 1
    alarms, transitions, ctl, pbt_log = [], [], [], []; a1_max = 0.0; a1_n = 0; win_al = {L: 0 for L in range(1, 10)}; win_p = 0; win_t0 = 0.0; win_a1 = False
    bound_hits = 0; fits_seen = set(); kicked = False; pred_E2 = None; base_period = None; last_pbt = 0.0
    gp_counts = {g['id']: {} for g in GP}; gp_last = {}; done_since = {L: None for L in range(1, 10)}; done_time = {L: 0.0 for L in range(1, 10)}
    nofree = {L: 0 for L in range(1, 10)}; rows_t, rows_s = [], []; stuck_since = {L: None for L in range(1, 10)}; gp_samples = []; last_sample = -1.0; rel_log = []
    t0 = time.perf_counter(); p = 0
    while True:
        tp = time.perf_counter(); t = tp - t0
        if t >= T_total: break
        p += 1; truth = dict(NOM); sig = dict(SIG)
        if replay:   # P2 real-data replay: the latest release at time t sets the truth and its sigma
            for key, rels in replay.items():
                cur = [r for r in rels if r[0] <= t]
                if cur: truth[key], sig[key] = cur[-1][1], cur[-1][2]
        if events:
            for E in EVENTS:
                if E['kind'] == 'data' and E['t0'] <= t < E['t1']: truth[E['key']] = E['f'](NOM[E['key']])
            if pred_E2 is None and t >= E2T[0]:
                dx = np.zeros(NK); dx[K.index('m32')] = EVENTS[1]['dx']; dm = np.abs(J @ dx); sd = np.maximum(np.sqrt(var), 1e-6)
                pred_E2 = {L for L in IDX if any(dm[i] > 4 * sd[i] for i in IDX[L])}; EVENTS[1]['pred'] = pred_E2
            if not kicked and t >= E2T[1]: x[K.index('m32')] += EVENTS[1]['dx']; kicked = True
            if kicked is True and t >= E2T[2]: x[K.index('m32')] -= EVENTS[1]['dx']; kicked = 'done'
        for L, keys in STREAM_OF.items():
            nr = 5 if esc[L] else 3
            for k in keys: est[k] = 0.95 * est[k] + 0.05 * float(np.median(truth[k] + sig[k] * rng.standard_normal(nr)))
        if p % (1 if any(esc.values()) else 10) == 0: J = jac(x, est); lensK = {L: lens_knobs(J, L) for L in range(1, 10)}
        Mcur = flat(margins_rt(state(x), est)); Mfresh = Mcur.copy()
        # referee pass, layers 1 -> 9
        for L in range(1, 10):
            if L not in IDX: continue
            lk, r = lensK[L]
            if r == 0:
                status[L] = 'OPAQUE'; continue
            m = Mcur[IDX[L]]; good = bool(np.all(m >= 0))
            ok_run[L] = ok_run[L] + 1 if good else 0; bad_run[L] = 0 if good else bad_run[L] + 1
            old = status[L]
            if old == 'RESONANT' and bad_run[L] >= 3: status[L] = 'LOST'
            elif old != 'RESONANT' and ok_run[L] >= 3: status[L] = 'RESONANT'
            elif old not in ('RESONANT', 'LOST', 'STUCK') and not good: status[L] = 'NO LOCK'
            if status[L] != old: transitions.append((p, round(t, 4), L, old, status[L])); res_since[L] = t if status[L] == 'RESONANT' else None
            if m.min() < 0.05 and status[L] != 'STUCK':   # balance on free bounded knobs
                inner = set().union(*[lensK[l][0] for l in range(1, L) if status[l] == 'RESONANT' and lensK[l][0]]) if L > 1 else set()
                free = [K.index(k) for k in K if k not in HELD and k not in inner]
                g = J[IDX[L][int(np.argmin(m))]].copy(); mask = np.zeros(NK); mask[free] = 1; g *= mask
                if np.linalg.norm(g) == 0: nofree[L] += 1
                if np.linalg.norm(g) > 0:
                    step = 0.002 * g / np.linalg.norm(g); xn = np.clip(x + step, LO, HI); step = xn - x; x = xn
                    Mcur = Mcur + J @ step; base = base + J @ step
                    if np.linalg.norm(step) < 1e-12:   # P1.3 STUCK: clipped on every needed knob
                        if stuck_since[L] is None: stuck_since[L] = t
                        elif t - stuck_since[L] >= 1.0 and status[L] != 'STUCK': transitions.append((p, round(t, 4), L, status[L], 'STUCK')); status[L] = 'STUCK'; res_since[L] = None
                    else: stuck_since[L] = None
        if np.any(np.isclose(x, LO, atol=1e-9) | np.isclose(x, HI, atol=1e-9)): bound_hits += 1
        for i, k in enumerate(K):
            if (abs(x[i]) > math.log(1.01) if k in LOG else abs(x[i]) > 1e-9): fits_seen.add(k)
        # detection: whitened residuals -> CUSUM (live), shadows on iid N(0,1)+probes, calibration banks
        rA = Mfresh - Mlast; Mlast = Mcur.copy()                      # detector A: exact explained-change residual (deterministic margins)
        evA = np.zeros(NM, bool); evA[DET] = armA[DET] & (np.abs(rA[DET]) > 1e-3); armA[DET] = np.where(evA[DET], False, np.where(np.abs(rA[DET]) < 1e-4, True, armA[DET]))
        sd = np.maximum(np.sqrt(var), 1e-6); z = (Mcur - base) / sd; w = (z - PHI * zprev) / math.sqrt(1 - PHI ** 2); zprev = z
        med[STO] += 0.001 * np.sign(np.abs(w[STO]) - med[STO]); med = np.maximum(med, 1e-3)
        wn = w / (1.4826 * med); wn[DET] = 0.0
        var = np.where(np.abs(z) < 3, 0.99 * var + 0.01 * (Mcur - base) ** 2, var); base = 0.99 * base + 0.01 * Mcur
        al = live.step(wn)[0] | evA
        if calib and t >= 2.0: calA += int(evA.sum())
        for i in np.nonzero(al)[0]: alarms.append((p, round(t, 4), LAYER_OF[int(i)])); win_al[LAYER_OF[int(i)]] += 1
        if pbt:
            ws = srng.standard_normal((4, NM)); ws[:, DET] = 0.0
            if probe is None and p % 2000 == 0: probe = [int(srng.choice(STO)), p]
            if probe: ws[:, probe[0]] += 0.32
            sh.Sp = np.maximum(0, sh.Sp + ws - sh.k); sh.Sn = np.maximum(0, sh.Sn - ws - sh.k); als = (sh.Sp > sh.h) | (sh.Sn > sh.h); sh.Sp[als] = 0; sh.Sn[als] = 0
            for c in range(4):
                hit = als[c].copy()
                if probe:
                    if hit[probe[0]] and not getattr(sh, 'got', {}).get(c):
                        sh_stats[c, 0] += p - probe[1]; sh_stats[c, 1] += 1; sh.__dict__.setdefault('got', {})[c] = True
                    hit[probe[0]] = False
                sh_stats[c, 2] += hit.sum()
            if probe and p - probe[1] >= 400:
                for c in range(4):
                    if not getattr(sh, 'got', {}).get(c): sh_stats[c, 0] += 800; sh_stats[c, 1] += 1
                sh.got = {}; probe = None
            if t - last_pbt >= 5.0 and sh_stats[:, 1].min() > 0:
                n_mp = max(p, 1) * len(STO); adm = [c for c in range(4) if sh_stats[c, 2] / n_mp <= 1e-5]
                fit = sh_stats[:, 0] / sh_stats[:, 1] + 1000 * sh_stats[:, 2]
                if adm:
                    best = min(adm, key=lambda c: fit[c]); worst = int(np.argmax(fit))
                    if tuple(shadows[best]) != tuple(live_cfg): live_cfg[:] = shadows[best]; live.k[:] = live_cfg[0]; live.h[:] = live_cfg[1]
                    if worst != best:
                        shadows[worst] = [shadows[best][0] * float(srng.choice([0.8, 1.25])), shadows[best][1] * float(srng.choice([0.8, 1.25]))]
                        sh.k[worst] = shadows[worst][0]; sh.h[worst] = shadows[worst][1]; sh_stats[worst] = 0; sh.Sp[worst] = 0; sh.Sn[worst] = 0
                    pbt_log.append(dict(t=round(t, 2), live=list(map(lambda v: round(v, 3), live_cfg)), shadows=[[round(a, 3), round(b, 3)] for a, b in shadows],
                                        mean_delay=[round(float(v), 1) for v in sh_stats[:, 0] / np.maximum(sh_stats[:, 1], 1)], fa=[int(v) for v in sh_stats[:, 2]]))
                last_pbt = t
        if calib and t >= 2.0:
            cal[:, 0] += cb.step(wn).sum(axis=1)
            wp = wn.copy()
            if cprobe is None and p % 1000 == 0: cprobe = [int(rng.choice(STO)), p, np.zeros(len(GRID), bool)]
            if cprobe: wp[cprobe[0]] += 0.32
            hp = cbp.step(wp)
            if cprobe:
                newly = hp[:, cprobe[0]] & ~cprobe[2]; cal[newly, 1] += p - cprobe[1]; cal[newly, 2] += 1; cprobe[2] |= hp[:, cprobe[0]]
                if p - cprobe[1] >= 400: cal[~cprobe[2], 3] += 1; cal[~cprobe[2], 1] += 800; cal[~cprobe[2], 2] += 1; cprobe = None
        if p % 200 == 0:
            d = float(np.max(np.abs(flat(margins_rt(state(x), NOM)) - flat(margins_ref(state(x)))))); a1_max = max(a1_max, d); a1_n += 1
            if d >= 1e-9: win_a1 = True
        # goalposts, live every pulse (static ones are constant)
        st = state(x)
        for g in GP:
            if g['live'] or g['id'] not in gp_last:
                r, v = score(g, st, est, Mcur); lab = label(g, r)
                if g['live'] and g['kind'] == 'PRED' and lab == 'PASS' and (DEP.get(g['live'], set()) & fits_seen): lab = 'PASS (FIT)'   # P1.1
                gp_last[g['id']] = (lab, v); c = gp_counts[g['id']]; c[lab] = c.get(lab, 0) + 1
        for L in range(1, 10):   # node DONE (strict, DEVIATIONS 2)
            mine = [g for g in GP if g['layer'] == L]
            ok = status[L] == 'RESONANT' and res_since[L] is not None and t - res_since[L] >= 3 and \
                 all(gp_last[g['id']][0] in ('PASS', 'PASS (null)', 'PASS (bound)', 'TRUST', 'UNSCORED') for g in mine) and not any(g['kind'] == 'FIT' for g in mine) and \
                 not any(k in fits_seen for k in (lensK[L][0] or set()))
            if ok and done_since[L] is None: done_since[L] = t
            if not ok and done_since[L] is not None: done_time[L] += t - done_since[L]; done_since[L] = None
        rows_t.append(t); rows_s.append([SC[status[L]] for L in range(1, 10)]); win_p += 1
        if t - last_sample >= 0.5: last_sample = t; gp_samples.append((round(t, 2), {g['id']: gp_last[g['id']][0] for g in GP if g['live']}, {k: float(est[k]) for k in est}))
        if t - win_t0 >= 1.0:   # controller (locked rules + event-window precision trigger)
            quiet = any(a <= win_t0 and t <= b for a, b in QUIET); inev = [E for E in EVENTS if E['t0'] <= t < E['t1'] and E['pred'] is not None] if events else []
            for L in IDX:
                badq = win_a1 or (quiet and win_al[L] / max(win_p, 1) > 1e-3)
                bade = bool(inev) and win_al[L] > 0 and all(L not in E['pred'] for E in inev)
                if (badq or bade) and esc[L] == 0:
                    esc[L] = 1; clean[L] = 0; throttle = min(throttle * 2, 64); ctl.append(dict(t=round(t, 2), layer=L, action='ESCALATE', why='A1' if win_a1 else ('quiet false alarms' if badq else 'alarm outside predicted set')))
                elif not (badq or bade):
                    clean[L] += 1
                    if esc[L] and clean[L] >= 5: esc[L] = 0; throttle = max(1, throttle // 2); ctl.append(dict(t=round(t, 2), layer=L, action='DE-ESCALATE'))
            win_al = {L: 0 for L in range(1, 10)}; win_p = 0; win_t0 = t; win_a1 = False
        if base_period is None and p > 200: base_period = (time.perf_counter() - t0) / p
        if throttle > 1 and base_period:
            slack = min(base_period * throttle, 1 / 60) - (time.perf_counter() - tp)
            if slack > 0: time.sleep(slack)
    for L in range(1, 10):
        if done_since[L] is not None: done_time[L] += T_total - done_since[L]
    return dict(p=p, T=T_total, tt=np.array(rows_t), ST=np.array(rows_s, np.int8), alarms=alarms, transitions=transitions, ctl=ctl, pbt=pbt_log,
                a1_max=a1_max, a1_n=a1_n, calA=calA, bound_frac=bound_hits / max(p, 1), fits=sorted(fits_seen), x=x, live_cfg=live_cfg, cal=cal,
                gp_counts=gp_counts, gp_last=gp_last, gp_samples=gp_samples, nofree=nofree, done_time=done_time, status=status, pred_E2=pred_E2)
def calibrate():
    tot = np.zeros((len(GRID), 4)); pulses = 0; fa_A = 0
    for s in range(1, 6):
        o = engine(7.0, s, events=False, calib=True, pbt=False); tot += o['cal']; pulses += int((o['tt'] >= 2.0).sum()); fa_A += o['calA']
    rows = []
    for i, (k, h) in enumerate(GRID):
        far = tot[i, 0] / (pulses * len(STO)); dl = tot[i, 1] / max(tot[i, 2], 1); miss = tot[i, 3] / max(tot[i, 2], 1)
        rows.append(dict(k=k, h=h, far=float(far), mean_delay=round(float(dl), 1), misses=int(tot[i, 3]), probes=int(tot[i, 2]), miss_frac=round(float(miss), 3), admissible=bool(far <= 1e-5 and miss <= 0.2)))
    far_A = fa_A / (pulses * len(DET)); A_ok = far_A <= 1e-5
    adm = [r for r in rows if r['admissible']]; start = min(adm, key=lambda r: r['mean_delay']) if (adm and A_ok) else None
    out = dict(pulses=pulses, data_margin_pulses=pulses * len(STO), detector_A=dict(false_alarms=fa_A, far=far_A, admissible=bool(A_ok)), grid=rows, start=start)
    json.dump(out, open('field_tests/results/d1987_calibration.json', 'w'), indent=1); return out
def scored(T=60.0, seed=2026, out_name='d1989_woven_run.json', archive=True):
    f = T / 60.0   # D1989 DEVIATIONS 1: schedule scales with run length
    for E, base in zip(EVENTS, ((10, 20), (25, 35), (45, 55))): E['t0'], E['t1'] = base[0] * f, base[1] * f
    E2T[0], E2T[1], E2T[2] = 24 * f, 25 * f, 35 * f
    QUIET[:] = [(max(2, 2 * f), 10 * f), (20.5 * f, 25 * f), (35.5 * f, 45 * f), (55.5 * f, 60 * f)]
    cal = json.load(open('field_tests/results/d1987_calibration.json')); s0 = cal['start']
    if s0 is None: raise SystemExit('D1987: no admissible detector config; scored run NOT performed (as locked)')
    o = engine(T, seed, events=True, live_cfg=(s0['k'], s0['h']), pbt=True)
    tt, ST = o['tt'], o['ST']; al = o['alarms']; sc = {}
    for E in EVENTS:
        E['pred'] = E['pred'] or set()
        fast = {L for _, t, L in al if E['t0'] <= t < E['t0'] + 0.5}; full = {L for _, t, L in al if E['t0'] <= t < E['t1']}
        lat = {L: round(1000 * min(t - E['t0'] for _, t, l in al if l == L and t >= E['t0']), 2) for L in E['pred'] if any(l == L and t >= E['t0'] for _, t, l in al)}
        i0 = max(np.searchsorted(tt, E['t0']) - 1, 0); i1 = min(np.searchsorted(tt, E['t1'] + 3.0 * T / 60.0) - 1, len(tt) - 1)
        before = {L for L in range(1, 10) if ST[i0, L - 1] == 3}
        rec = {L: bool(ST[i1, L - 1] == 3) for L in before}
        sc[E['name']] = dict(pred=sorted(E['pred']), fast=sorted(fast), full=sorted(full), recall_fast=(len(E['pred'] & fast) / len(E['pred'])) if E['pred'] else None,
                             prec_fast=(len(fast & E['pred']) / len(fast)) if fast else 1.0, prec_full=(len(full & E['pred']) / len(full)) if full else 1.0,
                             latency_ms=lat, recovery_checked=sorted(before), recovered=rec)
    qp = sum(int(((tt >= a) & (tt < b)).sum()) for a, b in QUIET)
    qa = {L: sum(1 for _, t, l in al if l == L and any(a <= t < b for a, b in QUIET)) for L in IDX}; far = {L: qa[L] / max(qp, 1) for L in IDX}
    tf = sum(len(set(s['fast']) & set(s['pred'])) for s in sc.values()); nf = sum(len(s['fast']) for s in sc.values())
    tu = sum(len(set(s['full']) & set(s['pred'])) for s in sc.values()); nu = sum(len(s['full']) for s in sc.values())
    nrec = sum(len(s['recovered']) for s in sc.values())
    A = dict(A1=o['a1_max'] < 1e-9, A2_recall=all(s['recall_fast'] == 1 for s in sc.values() if s['recall_fast'] is not None),
             A2_prec_fast=(tf / nf if nf else 1.0) >= 0.9, A2_prec_full=(tu / nu if nu else 1.0) >= 0.9,
             A3=all(v <= 1e-3 for v in far.values()), A4=nrec >= 1 and all(all(s['recovered'].values()) for s in sc.values()), A5=o['bound_frac'] <= 0.10)
    stuck = {L: sum(1 for tr in o['transitions'] if tr[2] == L and tr[4] == 'STUCK') for L in range(1, 10)}
    board = {}
    for g in GP:
        lab = o['gp_last'][g['id']][0]; v = o['gp_last'][g['id']][1]
        board.setdefault(g['layer'], []).append(dict(id=g['id'], name=g['name'], kind=g['kind'], open_problem=g['open_problem'], final=lab,
                                                     value=None if v is None else float(v), live=bool(g['live']), share={k: round(c / o['p'], 4) for k, c in o['gp_counts'][g['id']].items()}))
    flips = {L: sum(1 for tr in o['transitions'] if tr[2] == L and tr[3] == 'RESONANT') for L in range(1, 10)}
    res_share = {L: round(float((ST[:, L - 1] == 3).mean()), 3) for L in range(1, 10)}
    tally = {}
    for g in GP:
        lab = o['gp_last'][g['id']][0]; tally[lab] = tally.get(lab, 0) + 1
    surviving_pred = [g['id'] for g in GP if g['kind'] == 'PRED' and o['gp_last'][g['id']][0] == 'PASS']
    out = dict(prereg='PREREG_D1989_complete_field.md (+ D1986/D1987)', seed=seed, stuck_events=stuck, no_free_knob_share={L: round(v / o['p'], 3) for L, v in o['nofree'].items()}, seconds=T, pulses=o['p'], pulses_per_s=round(o['p'] / T, 1), start_cfg=cal['start'], final_live_cfg=o['live_cfg'],
               accuracy=A, verdict='PASS' if all(A.values()) else 'FAIL', events=sc, false_alarm_rate=far, quiet_pulses=qp, precision_fast=round(tf / nf, 3) if nf else None,
               precision_full=round(tu / nu, 3) if nu else None, bound_frac=round(o['bound_frac'], 4), fits_spent=o['fits'], final_knobs={k: state(o['x'])[k] for k in K},
               final_status=o['status'], resonant_share=res_share, lost_flips=flips, done_seconds={L: round(v, 2) for L, v in o['done_time'].items()},
               goalpost_tally=tally, surviving_predictions=surviving_pred, scoreboard=board, controller=o['ctl'], pbt=o['pbt'][-6:], pbt_n=len(o['pbt']),
               alarms=[dict(p=a, t=b, layer=c) for a, b, c in o['alarms']][:400], n_alarms=len(o['alarms']), a1_max=o['a1_max'], a1_checks=o['a1_n'], pred_E2=sorted(o['pred_E2'] or []))
    json.dump(out, open('field_tests/results/' + out_name, 'w'), indent=1, default=str)
    if archive:
     with open('field_tests/loom/method_archive.jsonl', 'a') as f:   # O5: keep every variant
        f.write(json.dumps(dict(version='engine_v4_D1989', parent='engine_v3_D1987', config=dict(start=cal['start'], final=o['live_cfg']), train=dict(calibration='d1987_calibration.json'),
                                heldout=dict(seed=2026, accuracy=A, pulses_per_s=out['pulses_per_s'], precision_fast=out['precision_fast'], precision_full=out['precision_full']))) + '\n')
    if archive: np.savez_compressed('field_tests/results/' + out_name.replace('.json', '_status.npz'), t=tt.astype(np.float32), status=ST)
    return out
REPLAY = {  # P2: published history (recalled from PDG / collaboration papers; order and values locked in PREREG_D1989)
 'ns': [(0, 0.9608, 0.0080), (10, 0.9603, 0.0073), (20, 0.9655, 0.0062), (30, 0.9649, 0.0042), (40, 0.9743, 0.0034), (50, 0.9684, 0.0030), (60, 0.9728, 0.0027)],
 'as_': [(0, 0.1184, 0.0007), (10, 0.1185, 0.0006), (20, 0.1181, 0.0011), (30, 0.1181, 0.0011), (40, 0.1179, 0.0010), (50, 0.1179, 0.0009), (60, 0.1180, 0.0009)],
 'wino': [(0, 460.0, 20.0), (25, 660.0, 20.0), (50, 700.0, 20.0)],
 'Y': [(0, 0.88e-10, 0.0088e-10), (30, 0.87e-10, 0.0087e-10)]}
STREAM_LAYER = {'ns': 6, 'as_': 7, 'wino': 5, 'Y': 8}
def replay_run(T=70.0, seed=2028):
    cal = json.load(open('field_tests/results/d1987_calibration.json')); s0 = cal['start']
    o = engine(T, seed, events=False, live_cfg=(s0['k'], s0['h']), pbt=True, replay=REPLAY)
    al = o['alarms']; rel = []
    for key, rels in REPLAY.items():
        for (t0, v, sg), prev in zip(rels[1:], rels[:-1]):
            d = abs(v - prev[1]) / sg; L = STREAM_LAYER[key]
            det = any(l == L and t0 <= t < t0 + 1.0 for _, t, l in al)
            rel.append(dict(stream=key, t=t0, value=v, delta_over_sigma=round(d, 2), detectable=d >= 1, quiet_expected=d < 0.25, detected=det))
    rc = [r for r in rel if r['detectable']]; sp = [r for r in rel if r['quiet_expected']]
    timeline = [dict(t=t, labels=lab, est=est) for t, lab, est in o['gp_samples'] if any(abs(t - (r[0] + 9.5)) < 0.26 for rels in REPLAY.values() for r in rels)]
    out = dict(prereg='PREREG_D1989_complete_field.md P2', seed=seed, seconds=T, pulses=o['p'], releases=rel,
               recall=round(sum(r['detected'] for r in rc) / len(rc), 3) if rc else None, n_detectable=len(rc),
               specificity=round(sum(not r['detected'] for r in sp) / len(sp), 3) if sp else None, n_quiet_expected=len(sp),
               fits_spent=o['fits'], final_knobs={k: state(o['x'])[k] for k in K}, final_status=o['status'], no_free_knob_share={L: round(v / o['p'], 3) for L, v in o['nofree'].items()},
               final_live_goalposts={g['id']: o['gp_last'][g['id']][0] for g in GP if g['live']}, timeline=timeline, bound_frac=round(o['bound_frac'], 4))
    json.dump(out, open('field_tests/results/d1989_replay.json', 'w'), indent=1, default=str); return out
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'run'
    if cmd == 'calibrate':
        c = calibrate(); print(json.dumps(c, indent=1))
    elif cmd == 'replay':
        o = replay_run(); print(json.dumps({k: o[k] for k in ('pulses', 'recall', 'n_detectable', 'specificity', 'n_quiet_expected', 'fits_spent', 'final_status', 'final_live_goalposts', 'bound_frac')}, indent=1, default=str))
        for r in o['releases']: print(r)
        sys.exit()
    else:
        o = scored(float(sys.argv[2]) if len(sys.argv) > 2 else 60.0, seed=int(sys.argv[3]) if len(sys.argv) > 3 else 2027)
        print(json.dumps({k: o[k] for k in ('pulses', 'pulses_per_s', 'accuracy', 'verdict', 'precision_fast', 'precision_full', 'bound_frac', 'fits_spent', 'final_status',
                                             'resonant_share', 'lost_flips', 'stuck_events', 'done_seconds', 'goalpost_tally', 'surviving_predictions', 'pred_E2', 'start_cfg', 'final_live_cfg')}, indent=1, default=str))
        for n, s in o['events'].items(): print(n, s)
