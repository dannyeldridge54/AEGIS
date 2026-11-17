"""R2c-b (PREREG_R2c_b_alls): full LO Sommerfeld thermal sigma_eff, all sectors (Hisano hep-ph/0610249 Eqs 2-8, 13)."""
import sys, math, numpy as np
from multiprocessing import Pool
sys.path.insert(0, 'tools/janus_astro')
import sommerfeld_nlo as N, sommerfeld as Sm
G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]])            # Gamma*2 in units pi a2^2/M^2 (c folded below)
FREE = False
def A(): return 0.0 if FREE else N.ALPHA
def A2(): return 0.0 if FREE else N.ALPHA2
def Vcc(r):  # coupled (00, +-) without 2dm
    off = -math.sqrt(2)*A2()*math.exp(-N.MW*r)/r
    return np.array([[0.0, off], [off, -A()/r - A2()*N.CW2*math.exp(-N.MZ*r)/r]])
def V_pm1(r): return -A()/r - A2()*N.CW2*math.exp(-N.MZ*r)/r
def V_0c(r):  return -A2()*math.exp(-N.MW*r)/r
def V_cc(r):  return +A()/r + A2()*N.CW2*math.exp(-N.MZ*r)/r
def job(a):
    kind, M, v = a
    if kind == 'row0open':
        s = Sm.two_channel_open(M, v, Vcc, N.DM, tails=(0.0, A()))[0]; return float(np.real(s @ G @ s.conj()))/2   # Gamma_hat
    if kind == 'row0closed':
        if FREE: N.ALPHA, N.ALPHA2 = 0.0, 0.0
        s = np.asarray(N.wino_s_nlo(M, v, nlo=False)); return float(s @ G @ s)/2
    if kind == 'row1':   # chi+chi- incoming, own relative v; total E from 00 threshold
        v00 = 2*math.sqrt((M*v*v/4 + 2*N.DM)/M)
        s = Sm.two_channel_open(M, v00, Vcc, N.DM, tails=(0.0, A()))[1]; return float(np.real(s @ G @ s.conj()))/2
    if kind == 'pm1': return Sm.single_channel(M, v, V_pm1, alpha_tail=A())
    if kind == '0c':  return Sm.single_channel(M, v, V_0c, alpha_tail=0.0)
    if kind == 'cc':  return Sm.single_channel(M, v, V_cc, alpha_tail=-A())
def run(Ms, xs, ns, free=False):
    global FREE; FREE = free
    out = {}
    for M in Ms:
        vth = 2*math.sqrt(2*N.DM/M)
        og = {n: np.geomspace(1.001*vth, 2.0, n) for n in ns}
        cg = {n: np.linspace(1e-3*vth, 0.999*vth, 5*n) for n in ns}
        sg = {n: np.geomspace(1e-3, 2.0, n) for n in ns}
        tasks = []
        for n in ns:
            tasks += [('row0open', M, v) for v in og[n]] + [('row0closed', M, v) for v in cg[n]]
            tasks += [(k, M, v) for k in ('row1', 'pm1', '0c', 'cc') for v in sg[n]]
        tasks = list(dict.fromkeys(tasks))
        with Pool(2, initializer=_init, initargs=(free,)) as p: res = dict(zip(tasks, p.map(job, tasks)))
        for x in xs:
            w = lambda v: v**2*np.exp(-x*v**2/4); Zf = math.sqrt(math.pi)*(4/x)**1.5/4
            av = lambda kind, g: np.trapezoid(np.array([res[(kind, M, v)] for v in g])*w(g), g)/Zf
            avB = lambda g: np.trapezoid(w(g), g)/Zf         # Born (S=1) on the same grid
            w1 = (1 + N.DM/M)**1.5*math.exp(-x*N.DM/M); w2 = w1*w1
            for n in ns:
                S00 = av('row0open', og[n]) + av('row0closed', cg[n]); B00 = avB(og[n]) + avB(cg[n])
                s00 = 0.25*2*S00; b00 = 0.25*2*1.0*B00
                spm = 0.25*av('row1', sg[n]) + 0.75*25/24*av('pm1', sg[n]); bpm = (0.25*1.5 + 0.75*25/24)*avB(sg[n])
                s0c = (0.25*0.5 + 0.75*25/24)*av('0c', sg[n]); b0c = (0.25*0.5 + 0.75*25/24)*avB(sg[n])
                scc = 0.25*2*0.5*av('cc', sg[n]); bcc = 0.25*2*0.5*avB(sg[n])
                tot = s00 + 4*w1*s0c + 2*w2*spm + 2*w2*scc; totB = b00 + 4*w1*b0c + 2*w2*bpm + 2*w2*bcc
                out[(M, x, n)] = (tot/totB, s00/b00, spm/bpm, s0c/b0c, scc/bcc)
    return out
def _init(free):
    global FREE; FREE = free
    if free: N.ALPHA, N.ALPHA2 = 0.0, 0.0
if __name__ == '__main__':
    t1 = run([2000.0], [25], [40], free=True)[(2000.0, 25, 40)]
    print(f"T1 free: R_eff={t1[0]:.7f} parts={[round(q, 7) for q in t1[1:]]} -> {'PASS' if abs(t1[0]-1) <= 1e-4 else 'FAIL'}", flush=True)
    r = run([2000.0, 2842.0], [20, 25, 30], [40, 80])
    for M in (2000.0, 2842.0):
        for x in (20, 25, 30):
            a, b = r[(M, x, 40)], r[(M, x, 80)]; c = abs(a[0]/b[0] - 1)
            print(f"M={M:.0f} x={x}: R_eff={b[0]:.4f} (n40 {a[0]:.4f}, conv {c:.1e} {'OK' if c <= 0.01 else 'NOT CONV'}) | R00={b[1]:.3f} R+-={b[2]:.3f} R0c={b[3]:.3f} Rcc={b[4]:.3f}", flush=True)
