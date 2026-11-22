#!/usr/bin/env python3
"""CubeMind Ramsey engine, hardware-adaptive (PC edition).
It detects the machine at start-up and sizes itself from that:
  - cores: all logical cores, for numba parallel loops;
  - RAM: keeps every bitset table in memory and refuses to start if they would not fit;
  - GPU: computes the big 'which sets does A miss' tables on CUDA (torch or cupy) when one is present.
Jobs:
  hw          report hardware and the plan it will use
  glue K      exhaustive degree-4 gluing for a (3,K)-graph on 40 vertices (D2002/D2003 replication, K = 10)
  control     positive controls: K = 11 and K = 12 must find solutions, each verified by an independent alpha check
  all         hw + controls + glue 10, writing results/cm_ramsey_<host>.json
This is the same logic as glue4.c / sat_deg4.py (cloud), re-implemented here as a third independent check."""
import os, sys, json, time, platform, itertools, ctypes, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, 'results'); os.makedirs(RES, exist_ok=True)

# ---------------- hardware ----------------
def ram_bytes():
    try:
        if os.name == 'nt':
            class M(ctypes.Structure):
                _fields_ = [('l', ctypes.c_ulong), ('load', ctypes.c_ulong), ('tot', ctypes.c_ulonglong), ('avail', ctypes.c_ulonglong),
                            ('tp', ctypes.c_ulonglong), ('ap', ctypes.c_ulonglong), ('tv', ctypes.c_ulonglong), ('av', ctypes.c_ulonglong), ('ae', ctypes.c_ulonglong)]
            m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); return int(m.tot), int(m.avail)
        tot = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'); av = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES'); return tot, av
    except Exception: return 0, 0

def gpu_info():
    g = {'backend': None, 'name': None, 'mem_gb': None}
    try:
        import torch
        if torch.cuda.is_available():
            p = torch.cuda.get_device_properties(0); g.update(backend='torch', name=p.name, mem_gb=round(p.total_memory / 2**30, 1)); return g
    except Exception: pass
    try:
        import cupy
        if cupy.cuda.runtime.getDeviceCount() > 0:
            p = cupy.cuda.runtime.getDeviceProperties(0); g.update(backend='cupy', name=p['name'].decode(), mem_gb=round(p['totalGlobalMem'] / 2**30, 1)); return g
    except Exception: pass
    try:
        out = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'], capture_output=True, text=True, timeout=10).stdout.strip()
        if out: g['name'] = out.splitlines()[0]; g['note'] = 'GPU present but no torch/cupy with CUDA in this Python: install one to use it (pip install cupy-cuda12x)'
    except Exception: pass
    return g

def hw():
    tot, av = ram_bytes(); cores = os.cpu_count() or 1
    try:
        import numba; nb = numba.__version__
    except Exception: nb = None
    return {'host': platform.node(), 'os': platform.platform(), 'python': platform.python_version(), 'logical_cores': cores,
            'ram_total_gb': round(tot / 2**30, 1), 'ram_avail_gb': round(av / 2**30, 1), 'numba': nb, 'gpu': gpu_info()}

# ---------------- the unique (3,9,35)-graph H and its independent sets ----------------
N = 35; S = (1, 7, 11, 16)
NB = [0] * N
for v in range(N):
    for d in S: NB[v] |= 1 << ((v + d) % N) | 1 << ((v - d) % N)

def indep_sets(lo, hi):
    out = {k: [] for k in range(lo, hi + 1)}
    def rec(mask, size, cand):
        if size >= lo: out[size].append(mask)
        if size == hi: return
        c = cand
        while c:
            v = (c & -c).bit_length() - 1; c &= c - 1
            rec(mask | 1 << v, size + 1, c & ~NB[v])
    rec(0, 0, (1 << N) - 1)
    return out

def miss_table(cands, sets, plan):
    """GPU result is trusted only after it matches the CPU result on a sample of rows; otherwise CPU is used."""
    out = _miss_table(cands, sets, plan)
    if plan['gpu']:
        C = np.array(cands[:3000], dtype=np.int64); T = np.array(sets, dtype=np.int64); ref = _miss_cpu(C, T, (len(T) + 63) // 64)
        if not np.array_equal(out[:3000], ref):
            print('GPU table disagrees with CPU on the check rows: using CPU'); plan['gpu_check'] = 'FAIL'
            return _miss_cpu(np.array(cands, dtype=np.int64), T, (len(T) + 63) // 64)
        plan['gpu_check'] = 'PASS'
    return out

def _miss_table(cands, sets, plan):
    """bitset M[c, w]: bit s set when candidate c misses (is disjoint from) set s. GPU when available, else numba/numpy."""
    C = np.array(cands, dtype=np.int64); T = np.array(sets, dtype=np.int64); W = (len(T) + 63) // 64
    if plan['gpu'] == 'torch':
        import torch; dev = 'cuda'; Ct = torch.tensor(C, device=dev); Tt = torch.tensor(T, device=dev)
        out = torch.zeros((len(C), W), dtype=torch.int64, device=dev); step = max(1, int(plan['gpu_rows']))
        pad = W * 64 - len(T); Tt = torch.cat([Tt, torch.full((pad,), (1 << 40) - 1, dtype=torch.int64, device=dev)]) if pad else Tt  # pad sets never missed
        for i in range(0, len(C), step):
            m = ((Ct[i:i + step, None] & Tt[None, :]) == 0).view(-1, W, 64).to(torch.int64)
            out[i:i + step] = (m << torch.arange(64, device=dev, dtype=torch.int64)).sum(-1)   # bit 63 wraps to sign: fine, used only as raw bits
        return out.cpu().numpy().view(np.uint64)
    if plan['gpu'] == 'cupy':
        import cupy as cp; Ct = cp.asarray(C); pad = W * 64 - len(T); Tt = cp.asarray(np.concatenate([T, np.full(pad, (1 << 40) - 1, np.int64)]))
        out = cp.zeros((len(C), W), dtype=cp.uint64); sh = cp.arange(64, dtype=cp.uint64); step = max(1, int(plan['gpu_rows']))
        for i in range(0, len(C), step):
            m = ((Ct[i:i + step, None] & Tt[None, :]) == 0).reshape(-1, W, 64).astype(cp.uint64)
            out[i:i + step] = (m << sh).sum(-1)
        return cp.asnumpy(out)
    return _miss_cpu(C, T, W)

try:
    from numba import njit, prange
except Exception:
    njit = None

if njit:
    @njit(parallel=True, cache=True)
    def _miss_cpu(C, T, W):
        out = np.zeros((len(C), W), dtype=np.uint64)
        for c in prange(len(C)):
            x = C[c]
            for s in range(len(T)):
                if (x & T[s]) == 0: out[c, s >> 6] |= np.uint64(1) << np.uint64(s & 63)
        return out

    @njit(cache=True)
    def _and0(a, b):
        for w in range(len(a)):
            if a[w] & b[w]: return False
        return True

    @njit(cache=True)
    def _and0_3(a, b, c):
        for w in range(len(a)):
            if a[w] & b[w] & c[w]: return False
        return True

    @njit(cache=True)
    def _and0_4(a, b, c, d):
        for w in range(len(a)):
            if a[w] & b[w] & c[w] & d[w]: return False
        return True

    @njit(parallel=True, cache=True)
    def _glue(C, A1idx, MP, MT, MQ, cap):
        """For each A1 (contains vertex 0): count A2<A3<A4 that are disjoint, with no pair missing a P-set, no triple missing a T-set,
        and no quadruple missing a Q-set. Returns per-A1 (pairs tried, solutions) and up to cap example solutions per A1."""
        n1 = len(A1idx); stats = np.zeros((n1, 3), dtype=np.int64); ex = -np.ones((n1, cap, 3), dtype=np.int64)
        for t in prange(n1):
            a = A1idx[t]; xa = C[a]; P = np.empty(len(C), dtype=np.int64); np_ = 0
            for b in range(len(C)):
                if (C[b] & xa) == 0 and _and0(MP[a], MP[b]): P[np_] = b; np_ += 1
            found = 0; stats[t, 2] = np_
            for i in range(np_):
                b = P[i]; xb = C[b]
                for j in range(i + 1, np_):
                    c = P[j]; xc = C[c]
                    if (xb & xc) or not _and0(MP[b], MP[c]) or not _and0_3(MT[a], MT[b], MT[c]): continue
                    stats[t, 0] += 1
                    for k in range(j + 1, np_):
                        d = P[k]; xd = C[d]
                        if (xd & (xb | xc)) or not _and0(MP[b], MP[d]) or not _and0(MP[c], MP[d]): continue
                        if not (_and0_3(MT[a], MT[b], MT[d]) and _and0_3(MT[a], MT[c], MT[d]) and _and0_3(MT[b], MT[c], MT[d])): continue
                        if not _and0_4(MQ[a], MQ[b], MQ[c], MQ[d]): continue
                        if found < cap: ex[t, found, 0] = b; ex[t, found, 1] = c; ex[t, found, 2] = d
                        found += 1; stats[t, 1] += 1
                        if cap > 0 and found >= cap: break
                    if cap > 0 and found >= cap: break
                if cap > 0 and found >= cap: break
        return stats, ex

# ---------------- independent alpha check on the glued 40-vertex graph ----------------
def glued(Amasks):
    adj = [0] * 40
    for v in range(N): adj[v] = NB[v]
    for i, A in enumerate(Amasks):
        w = 36 + i; adj[35] |= 1 << w; adj[w] |= 1 << 35
        for h in range(N):
            if A >> h & 1: adj[w] |= 1 << h; adj[h] |= 1 << w
    return adj

def alpha(adj):
    best = [0]
    def rec(size, cand):
        if size + bin(cand).count('1') <= best[0]: return
        if not cand: best[0] = size; return
        v = (cand & -cand).bit_length() - 1
        rec(size + 1, cand & ~adj[v] & ~(1 << v)); rec(size, cand & ~(1 << v))
    rec(0, (1 << len(adj)) - 1); return best[0]

def triangle_free(adj):
    return all(not (adj[u] & adj[v]) for u in range(len(adj)) for v in range(u) if adj[u] >> v & 1)

# ---------------- plan + jobs ----------------
def make_plan(h, n_sets):
    g = h['gpu']['backend']; plan = {'threads': h['logical_cores'], 'gpu': g}
    table_gb = 73435 * ((n_sets + 63) // 64) * 8 / 2**30
    plan['table_gb'] = round(table_gb, 2)
    if h['ram_avail_gb'] and table_gb > 0.8 * h['ram_avail_gb']: raise SystemExit('not enough free RAM for the tables (%.1f GB needed)' % table_gb)
    plan['gpu_rows'] = int(max(64, min(8192, (h['gpu']['mem_gb'] or 1) * 2**30 * 0.5 / (n_sets * 9)))) if g else 0   # half the GPU memory per chunk
    return plan

def run_glue(K, h, cap=0, log=print, max_a1=None):
    from numba import set_num_threads; t0 = time.time()
    I = indep_sets(3, 8); cands = [m for k in range(3, 9) for m in I[k]]
    groups = {2: [], 3: [], 4: []}
    for j in (6, 7, 8):
        m = K - j            # j-set may be missed by at most K-1-j of the A's; so no m of them may all miss it
        if 2 <= m <= 4: groups[m] += I[j]
        elif m <= 1: raise SystemExit('K too small for this program')
    plan = make_plan(h, sum(len(v) for v in groups.values())); set_num_threads(plan['threads'])
    log('K=%d: %d candidates; pair/triple/quad set counts %s; plan %s' % (K, len(cands), {k: len(v) for k, v in groups.items()}, plan))
    C = np.array(cands, dtype=np.int64)
    M = {m: (miss_table(cands, groups[m], plan) if groups[m] else np.zeros((len(C), 1), dtype=np.uint64)) for m in (2, 3, 4)}
    t1 = time.time(); log('miss tables built in %.1fs (%s)' % (t1 - t0, plan['gpu'] or 'cpu'))
    A1 = np.array([i for i, m in enumerate(cands) if m & 1], dtype=np.int64)
    if max_a1: A1 = A1[:max_a1]   # controls only need a few examples
    stats, ex = _glue(C, A1, M[2], M[3], M[4], cap)
    sols = int(stats[:, 1].sum()); res = {'K': K, 'A1_sets': len(A1), 'partner_pairs_A1b': int(stats[:, 2].sum()), 'triples_A1bc': int(stats[:, 0].sum()), 'solutions': sols, 'plan': plan,
                                          'secs_tables': round(t1 - t0, 1), 'secs_search': round(time.time() - t1, 1)}
    checked = []
    for t in range(len(A1)):
        for e in ex[t]:
            if e[0] < 0 or len(checked) >= 3: continue
            adj = glued([cands[A1[t]]] + [cands[x] for x in e]); checked.append({'triangle_free': triangle_free(adj), 'alpha': alpha(adj)})
    res['verified_examples'] = checked; log(json.dumps(res)); return res

def main():
    job = sys.argv[1] if len(sys.argv) > 1 else 'all'; h = hw(); out = {'hw': h, 'started': time.strftime('%Y-%m-%d %H:%M:%S')}
    print(json.dumps(h, indent=1))
    if njit is None: raise SystemExit('numba is required: pip install numba')
    if job == 'hw': return
    if job in ('control', 'all'):
        out['control_K11'] = run_glue(11, h, cap=1, max_a1=4 * h['logical_cores']); out['control_K12'] = run_glue(12, h, cap=1, max_a1=4 * h['logical_cores'])
        ok = all(r['solutions'] > 0 and r['verified_examples'] and all(v['triangle_free'] and v['alpha'] == r['K'] - 1 for v in r['verified_examples'])
                 for r in (out['control_K11'], out['control_K12']))
        out['controls_pass'] = ok; print('CONTROLS', 'PASS' if ok else 'FAIL')
        if not ok and job == 'all': raise SystemExit('controls failed: not running the main search')
    if job in ('glue', 'all'):
        K = int(sys.argv[2]) if job == 'glue' and len(sys.argv) > 2 else 10
        out['main_K%d' % K] = run_glue(K, h, cap=3)
        print('MAIN K=%d: %d solutions' % (K, out['main_K%d' % K]['solutions']))
    fn = os.path.join(RES, 'cm_ramsey_%s.json' % h['host']); json.dump(out, open(fn, 'w'), indent=1); print('wrote', fn)

if __name__ == '__main__':
    main()
