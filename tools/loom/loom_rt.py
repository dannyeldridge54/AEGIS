#!/usr/bin/env python3
"""D1983 real-time layered pulsing (PREREG_D1983_realtime_pulse.md + DEVIATIONS). One process; every pulse runs layers 1->9 in order;
each layer's referee categorises its data, tracks resonance (3-pulse rule), flags LOST and unexplained shifts, balances on its free knobs,
and feeds the next layer in the same pulse. A per-layer controller adjusts work and pace during the run (never the bars).
Usage: python3 tools/loom/loom_rt.py [seconds=60]"""
import json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); os.chdir(ROOT)
ns_ = {}; exec(open('tools/loom/resonance.py').read().split("out = {'sweeps'")[0], ns_)
obs, margins_ref, D, LOG = ns_['obs'], ns_['margins'], ns_['D'], ns_['LOG']
K = ['u', 'MN', 'm32', 'TR', 'split']; NK = 5
NOM = dict(ns=0.9728, as_=0.1180, lep=0.0253, wino=700.0, Y=0.87e-10)
SIG = dict(ns=0.0027, as_=0.00107, lep=0.0003, wino=20.0, Y=0.0087e-10)
STREAM_OF = {4: ['lep'], 5: ['wino'], 6: ['ns'], 7: ['as_'], 8: ['Y']}
HELD = {'u'}                                     # N0: freeze the rung step (L1)
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
for L in range(1, 10):
    for a in sorted(margins_rt(state(np.zeros(NK)), NOM)[L]): IDX.setdefault(L, []).append(_i); _i += 1
NM = _i
def jac(x, T, h=1e-5):
    J = np.zeros((NM, NK))
    for j in range(NK):
        e = np.zeros(NK); e[j] = h; J[:, j] = (flat(margins_rt(state(x + e), T)) - flat(margins_rt(state(x - e), T))) / (2 * h)
    return J
def lens_knobs(J, L):
    if L not in IDX: return None, 0
    Jl = J[IDX[L]]; s = np.linalg.svd(Jl, compute_uv=False)
    r = int((s > 1e-3 * s.max()).sum()) if s.max() > 0 else 0
    if r == 0: return set(), 0
    vt = np.linalg.svd(Jl)[2][:r]; return {K[i] for i in range(NK) if np.abs(vt[:, i]).max() > 0.1}, r
EVENTS = [dict(name='E1 n_s +3 sigma', t0=10, t1=20, kind='data', key='ns', f=lambda v: v + 3 * SIG['ns'], pred={6}),
          dict(name='E2 m3/2 x1.05 kick', t0=25, t1=35, kind='knob', key='m32', dx=math.log(1.05), pred=None),
          dict(name='E3 Y_B -30 %', t0=45, t1=55, kind='data', key='Y', f=lambda v: v * 0.7, pred={8})]
QUIET = [(2, 10), (20, 25), (35, 45), (55, 60)]
def run(T_total=60.0, seed=1983):
    rng = np.random.default_rng(seed); x = np.zeros(NK); est = dict(NOM)
    J = jac(x, NOM); lensK = {L: lens_knobs(J, L) for L in range(1, 10)}
    M0 = flat(margins_rt(state(x), est)); base = M0.copy(); var = np.full(NM, 1e-4); exceed = np.zeros(NM, bool)
    ok_run = {L: 0 for L in range(1, 10)}; status = {L: ('WINDOW' if L not in IDX else 'NO LOCK') for L in range(1, 10)}
    esc = {L: 0 for L in range(1, 10)}; clean_windows = {L: 0 for L in range(1, 10)}; throttle = 1
    log_events, ctl_log, a1_max, a1_checks = [], [], 0.0, 0
    win_alarms = {L: 0 for L in range(1, 10)}; win_pulses = 0; win_start = 0.0; base_period = None
    rows_t, rows_status, rows_min = [], [], []; fits_seen = set(); kicked = False; pred_E2 = None; win_a1_fail = False
    SC = {'WINDOW': 0, 'OPAQUE': 1, 'NO LOCK': 2, 'RESONANT': 3, 'LOST': 4}
    t_start = time.perf_counter(); p = 0; tug = {}
    while True:
        tp = time.perf_counter(); t = tp - t_start
        if t >= T_total: break
        p += 1
        truth = dict(NOM)
        for E in EVENTS:
            if E['kind'] == 'data' and E['t0'] <= t < E['t1']: truth[E['key']] = E['f'](NOM[E['key']])
        # E2 prediction at t >= 24 s (from the lens, before the kick)
        if pred_E2 is None and t >= 24:
            dx = np.zeros(NK); dx[K.index('m32')] = EVENTS[1]['dx']; dm = np.abs(J @ dx); sd = np.sqrt(np.maximum(var, 1e-12)); sd = np.maximum(sd, 1e-6)
            pred_E2 = {L for L in IDX if any(dm[i] > 4 * sd[i] for i in IDX[L])}; EVENTS[1]['pred'] = pred_E2
        ext = np.zeros(NK)
        if not kicked and t >= 25: ext[K.index('m32')] += EVENTS[1]['dx']; kicked = True
        if kicked == True and t >= 35: ext[K.index('m32')] -= EVENTS[1]['dx']; kicked = 'done'
        x = x + ext                                           # external kick: NOT added to the baselines (unexplained)
        # data streams: 3 (or 5 when escalated) readings, median, running estimate
        for L, keys in STREAM_OF.items():
            nr = 5 if esc[L] else 3
            for k in keys:
                b = np.median(truth[k] + SIG[k] * rng.standard_normal(nr)); est[k] = 0.95 * est[k] + 0.05 * b
        # lens refresh: every pulse if any layer escalated, else every 10th
        if p % (1 if any(esc.values()) else 10) == 0: J = jac(x, est); lensK = {L: lens_knobs(J, L) for L in range(1, 10)}
        Mcur = flat(margins_rt(state(x), est))
        # layers 1 -> 9 in order (real time): referee + balance + feed forward (x updated in place)
        events_this = []; self_dx = np.zeros(NK); pulls = {}
        for L in range(1, 10):
            if L not in IDX: continue
            lk, r = lensK[L]
            if r == 0: status[L] = 'OPAQUE'; continue
            m = Mcur[IDX[L]]
            for i in IDX[L]:                                  # shift detector (rising edge; DEVIATIONS 2)
                dev = abs(Mcur[i] - base[i]); sd = max(math.sqrt(var[i]), 1e-6)
                if not exceed[i] and dev > 4 * sd: exceed[i] = True; events_this.append(L)
                elif exceed[i] and dev < 2 * sd: exceed[i] = False
                if not exceed[i]: var[i] = 0.99 * var[i] + 0.01 * (Mcur[i] - base[i]) ** 2
                base[i] = 0.99 * base[i] + 0.01 * Mcur[i]
            good = bool(np.all(m >= 0))
            ok_run[L] = ok_run[L] + 1 if good else 0
            if status[L] == 'RESONANT' and not good: status[L] = 'LOST'; log_events.append(dict(p=p, t=round(t, 4), layer=L, what='LOST'))
            elif ok_run[L] >= 3 and status[L] != 'RESONANT': status[L] = 'RESONANT'; log_events.append(dict(p=p, t=round(t, 4), layer=L, what='RESONANT'))
            elif not good and status[L] not in ('LOST',): status[L] = 'NO LOCK'
            # active balance on free knobs (DEVIATIONS 3)
            if m.min() < 0.05:
                inner = set().union(*[lensK[l][0] for l in range(1, L) if status[l] == 'RESONANT' and lensK[l][0]]) if L > 1 else set()
                free = [K.index(k) for k in K if k not in HELD and k not in inner]
                g = J[IDX[L][int(np.argmin(m))]].copy(); mask = np.zeros(NK); mask[free] = 1; g *= mask
                if np.linalg.norm(g) > 0:
                    step = 0.002 * g / np.linalg.norm(g); x = x + step; self_dx += step
                    for j in np.nonzero(step)[0]: pulls.setdefault(j, []).append((L, np.sign(step[j])))
                    Mnew = Mcur + J @ step; base += J @ step; Mcur = Mnew           # feed forward + self-move compensation (DEVIATIONS 1)
        for j, lst in pulls.items():                       # report only: opposing pulls on one knob in one pulse (a tug of war)
            if len({sg for _, sg in lst}) > 1: key = (K[j],) + tuple(sorted(L for L, _ in lst)); tug[key] = tug.get(key, 0) + 1
        for i, k in enumerate(K):
            if (abs(x[i]) > math.log(1.01) if k in LOG else abs(x[i]) > 1e-9): fits_seen.add(k)
        for L in set(events_this): log_events.append(dict(p=p, t=round(t, 4), layer=L, what='SHIFT')); win_alarms[L] += 1
        if p % 200 == 0:                                      # A1 validation against the reference code path
            d = float(np.max(np.abs(flat(margins_rt(state(x), NOM)) - flat(margins_ref(state(x))))))
            a1_max = max(a1_max, d); a1_checks += 1
            if d >= 1e-9: win_a1_fail = True
        rows_t.append(t); rows_status.append([SC[status[L]] for L in range(1, 10)]); rows_min.append([float(Mcur[IDX[L]].min()) if L in IDX else np.nan for L in range(1, 10)])
        win_pulses += 1
        if t - win_start >= 1.0:                              # the controller (locked rules), per 1 s window
            quiet = any(a <= t < b for a, b in QUIET)
            for L in IDX:
                bad = win_a1_fail or (quiet and win_alarms[L] / max(win_pulses, 1) > 1e-3)
                if bad and esc[L] == 0: esc[L] = 1; clean_windows[L] = 0; throttle = min(throttle * 2, 64); ctl_log.append(dict(t=round(t, 2), layer=L, action='ESCALATE', why='A1' if win_a1_fail else 'false alarms %d/%d' % (win_alarms[L], win_pulses)))
                elif not bad:
                    clean_windows[L] += 1
                    if esc[L] and clean_windows[L] >= 5: esc[L] = 0; throttle = max(1, throttle // 2); ctl_log.append(dict(t=round(t, 2), layer=L, action='DE-ESCALATE'))
            win_alarms = {L: 0 for L in range(1, 10)}; win_pulses = 0; win_start = t; win_a1_fail = False
        dt = time.perf_counter() - tp
        if base_period is None and p > 200: base_period = (time.perf_counter() - t_start) / p
        if throttle > 1 and base_period:
            target = min(base_period * throttle, 1 / 60.0); slack = target - dt
            if slack > 0: time.sleep(slack)
    tt = np.array(rows_t); ST = np.array(rows_status, dtype=np.int8); MN_ = np.array(rows_min, dtype=np.float32)
    # ---- scoring (locked bars)
    shifts = [e for e in log_events if e['what'] == 'SHIFT']; score = {}
    for E in EVENTS:
        E['pred'] = E['pred'] or set()
        det_fast = {e['layer'] for e in shifts if E['t0'] <= e['t'] < E['t0'] + 0.5}
        det_all = {e['layer'] for e in shifts if E['t0'] <= e['t'] < E['t1']}
        lat = {L: min((e['t'] - E['t0']) for e in shifts if e['layer'] == L and e['t'] >= E['t0']) for L in E['pred'] if any(e['layer'] == L and e['t'] >= E['t0'] for e in shifts)}
        latp = {L: int(np.searchsorted(tt, E['t0'] + lat[L]) - np.searchsorted(tt, E['t0'])) for L in lat}
        i0 = np.searchsorted(tt, E['t0']) - 1; i1 = np.searchsorted(tt, E['t1'] + 3.0) - 1
        rec = {L: bool(ST[i1, L - 1] == ST[i0, L - 1] or (ST[i0, L - 1] in (3,) and ST[i1, L - 1] == 3)) for L in E['pred']}
        score[E['name']] = dict(pred=sorted(E['pred']), detected_0p5s=sorted(det_fast), detected_window=sorted(det_all),
                                recall=(len(E['pred'] & det_fast) / len(E['pred'])) if E['pred'] else None,
                                precision=(len(det_all & E['pred']) / len(det_all)) if det_all else 1.0,
                                latency_ms={L: round(1000 * v, 2) for L, v in lat.items()}, latency_pulses=latp, recovered=rec)
    qpulses = sum(int(((tt >= a) & (tt < b)).sum()) for a, b in QUIET)
    qal = {L: sum(1 for e in shifts if e['layer'] == L and any(a <= e['t'] < b for a, b in QUIET)) for L in IDX}
    far = {L: qal[L] / max(qpulses, 1) for L in IDX}
    A = dict(A1=a1_max < 1e-9, A2=all(s['recall'] == 1 for s in score.values() if s['recall'] is not None) and
             (sum(len(set(s['detected_window']) & set(s['pred'])) for s in score.values()) / max(1, sum(len(s['detected_window']) for s in score.values()))) >= 0.9,
             A3=all(v <= 1e-3 for v in far.values()), A4=all(all(s['recovered'].values()) for s in score.values()))
    out = dict(prereg='PREREG_D1983_realtime_pulse.md', seconds=T_total, pulses=p, pulses_per_s=round(p / T_total, 1), a1_max=a1_max, a1_checks=a1_checks,
               events=score, false_alarm_rate=far, quiet_pulses=qpulses, controller=ctl_log, accuracy=A, verdict='PASS' if all(A.values()) else 'FAIL',
               final_status={L: [k for k, v in SC.items() if v == ST[-1, L - 1]][0] for L in range(1, 10)}, fits_spent=sorted(fits_seen),
               final_knobs={k: state(x)[k] for k in K}, resonance_log=[e for e in log_events if e['what'] != 'SHIFT'][:60], n_lost=sum(1 for e in log_events if e['what'] == 'LOST'),
               tug_of_war={'%s: layers %s' % (k[0], list(k[1:])): round(v / p, 4) for k, v in sorted(tug.items(), key=lambda kv: -kv[1])})
    np.savez_compressed('/tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/d1983_pulses.npz', t=tt, status=ST, minmargin=MN_)
    dec = slice(None, None, max(1, p // 600))
    json.dump(dict(t=[round(v, 4) for v in tt[dec]], status=ST[dec].tolist(), minmargin=np.round(MN_[dec], 4).tolist()), open('field_tests/results/d1983_pulses_decimated.json', 'w'))
    json.dump(out, open('field_tests/results/d1983_rt.json', 'w'), indent=1, default=str); return out
if __name__ == '__main__':
    o = run(float(sys.argv[1]) if len(sys.argv) > 1 else 60.0)
    print(json.dumps({k: o[k] for k in ('pulses', 'pulses_per_s', 'a1_max', 'accuracy', 'verdict', 'final_status', 'fits_spent', 'n_lost', 'tug_of_war')}, indent=1, default=str))
    for n, s in o['events'].items(): print(n, s)
    print('false alarms per layer-pulse:', {k: round(v, 6) for k, v in o['false_alarm_rate'].items()}); print('controller:', o['controller'][:12])
