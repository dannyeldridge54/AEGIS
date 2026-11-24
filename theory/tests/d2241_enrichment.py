"""D2239 (PREREG_D2239_BREATHING_DESIGN): breathing-rotation optimiser over the coupled reactor engine."""
import json, math, sys, functools
import numpy as np
sys.path.insert(0, 'tools/fusion'); sys.argv = ['x']
src = open('theory/tests/d2236_helm.py').read().split('out = []')[0]; g = {}; exec(src, g)
F, X, EA, machine, I0, SHARE = g['F'], g['X'], g['EA'], g['machine'], g['I0'], g['SHARE']
import adas as AD
HTS = len(sys.argv) > 1 and False
BL = json.load(open('field_tests/results/d2238_blanket.json'))
BLK = [('Li6_50_fw10', 0.5), ('Li6_70_fw10', 0.7), ('Li6_90_fw10', 0.9), ('Li6_90_fw5', 0.9)]
LEGS=[1,2,3]
LAD = dict(R=[6.2, 7.0, 8.0, 9.0], B=[5.3, 6.0, 7.0, 8.0, 9.0], fAr=[0.0014, 0.003, 0.005, 0.008], leg=LEGS, blk=list(range(4)),
           Paux=[10.0, 20.0, 30.0, 50.0], dens=[0.7, 0.8, 0.85, 0.9], nu=[0.4, 0.5, 0.6], enr=[3, 5, 10])
K0 = 2390.0; TT = np.geomspace(5.0, 2000.0, 600); LZ = np.maximum(AD.L_interp('ar', TT / 1000.0), 0.0)
def lengyel(Psep, m, nav, leg, nuf=0.4):
    a = m['a']; Bp = 4e-7 * math.pi * m['Ip'] * 1e6 / (2 * math.pi * a * math.sqrt((1 + m['kappa'] ** 2) / 2)); lam = 0.63 * Bp ** -1.19 * 1e-3
    q = max(Psep, 1.0) * 1e6 * (2 / 3) * m['B'] / (2 * math.pi * m['R'] * lam * Bp); Lc = math.pi * 3.0 * m['R'] * leg
    Tu = (3.5 * q * Lc / K0) ** (2 / 7); s = TT <= Tu; I = np.trapezoid(np.sqrt(TT[s]) * LZ[s], TT[s]); nu = nuf * nav
    return q ** 2 / (2 * K0 * nu ** 2 * Tu ** 2 * I)
@functools.lru_cache(maxsize=None)
def evaluate(R, B, fAr, leg, blk, Paux, dens, nu, enr, coil_max):
    m = machine(R, B); m['line_model'] = 'adas'; nG = m['Ip'] / (math.pi * m['a'] ** 2) * 1e20; nav = dens * nG
    fcore = fAr; c = None; c0 = None
    for it in range(2):
        mm = dict(m, f_Ar=fcore)
        try: op = X.operating_point_fast(mm, EA, n_avg=nav, P_aux=Paux)
        except Exception: op = None
        if op is None: return dict(score=(-(c0 / 0.05) - 10.0) if c0 else -99.0, feasible=False, why='no_solution', c_SOL=c0)   # DEV-1
        Psep = op['P_alpha'] + Paux - op['P_rad_core']; c = lengyel(Psep, m, nav, leg, nu); c0 = c if c0 is None else c0; fcore = max(fAr, c / enr)
    b = BL[BLK[blk][0]]; tbr, tsem = b['TBR'], b['TBR_sem']
    wl = op['P_fus'] * SHARE / m['S']; coil = B * R / (R - m['a'] - 1.2)
    v = dict(greenwald=op['f_G'] / 0.94 - 1, betaN=op['beta_N'] / 2.8 - 1, LH=1.3 * op['P_LH'] / op['P_loss'] - 1, wall=wl / 2.0 - 1, coil=coil / coil_max - 1,
             seeding=c / 0.05 - 1, core_Ar=c / enr / fAr - 1 if fAr < c / enr else -1, TBR=(1.05 + 2 * tsem) / tbr - 1)
    viol = {k: x for k, x in v.items() if x > 0}
    pl = F.plant(op['P_fus'], Paux, dict(F.PLANT_DEMO, M=1.161))
    return dict(score=pl['P_net'] if not viol else -sum(viol.values()) - 1, feasible=not viol, P_net=pl['P_net'], P_fus=op['P_fus'], Q_e=pl['Q_e'],
                c_SOL=c, Psep_R=Psep / R, wall=wl, coil=coil, TBR=tbr, violations=sorted(viol))
def breathe(start, coil_max, max_rot=12):
    cur = dict(start); hist = []
    for rot in range(max_rot):
        changed = False
        for k in LAD:
            base = evaluate(*(cur[q] for q in LAD), coil_max); i = LAD[k].index(cur[k]); best = (base['score'], cur[k])
            for j in (i - 1, i + 1):
                if 0 <= j < len(LAD[k]):
                    t = dict(cur, **{k: LAD[k][j]}); e = evaluate(*(t[q] for q in LAD), coil_max)
                    if e['score'] > best[0] + 1e-9: best = (e['score'], LAD[k][j])
            if best[1] != cur[k]: cur[k] = best[1]; changed = True
        e = evaluate(*(cur[q] for q in LAD), coil_max); hist.append(dict(rotation=rot + 1, point=dict(cur), **{q: e.get(q) for q in ('score', 'feasible', 'P_net', 'violations')}))
        if not changed: break
    return cur, evaluate(*(cur[q] for q in LAD), coil_max), hist
starts = {'ITER': dict(R=6.2, B=5.3, fAr=0.0014, leg=1, blk=0, Paux=50.0, dens=0.85, nu=0.4, enr=3), 'R9B6': dict(R=9.0, B=6.0, fAr=0.0014, leg=1, blk=0, Paux=10.0, dens=0.8, nu=0.4, enr=3),
          'R8B8': dict(R=8.0, B=8.0, fAr=0.0014, leg=1, blk=0, Paux=10.0, dens=0.85, nu=0.4, enr=3)}
import copy
LAD0 = copy.deepcopy(LAD)

out={}
for tag,legs,nus,enrs in (('control',[1,2,3,4,5],[0.4,0.5,0.6],[3]),('main',[1,2,3,4,5],[0.4,0.5,0.6],[3,5,10])):
    LAD['leg']=legs; LAD['nu']=nus; LAD['enr']=enrs; evaluate.cache_clear(); res={}; print('==',tag)
    for cls, cm in (('Nb3Sn', 12.0), ('HTS', 20.0)):
        for s, p in starts.items():
            end, e, hist = breathe(p, cm); res[f'{cls}|{s}'] = dict(end=end, result=e, rotations=len(hist), history=hist)
            print(cls, s, '->', end, {q: (round(e[q], 3) if isinstance(e.get(q), float) else e.get(q)) for q in ('feasible', 'P_net', 'P_fus', 'c_SOL', 'Psep_R', 'wall', 'TBR', 'violations')}, 'rot', len(hist), flush=True)
    out[tag]=res
json.dump(out, open('field_tests/results/d2241_enrichment.json','w'), indent=1, default=float)
