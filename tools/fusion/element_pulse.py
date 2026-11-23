"""PULSE-ELEMENTS: coronal atomic data for every element in the public ADAS set (side pulse beside the fusion goalpost)."""
import json, math, os, sys, time
import numpy as np
from scipy.interpolate import RectBivariateSpline
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import adas as A
ALL = os.path.join(HERE, 'adas', 'all'); MAN = json.load(open(os.path.join(ALL, 'MANIFEST.json')))
Z_OF = dict(h=1, he=2, li=3, be=4, b=5, c=6, n=7, o=8, f=9, ne=10, al=13, si=14, s=16, cl=17, ar=18, cr=24, fe=26, ni=28, cu=29, ge=32, kr=36, mo=42, xe=54, w=74)

def load(el):
    return {k: A.read_adf11(os.path.join(ALL, v['file'])) for k, v in MAN[el].items()}

def spl(d):
    return {z: RectBivariateSpline(d['logn'], d['logT'], b, kx=1, ky=1) for z, b in d['blocks'].items()}

def table(el, nes=(1e19, 1e20, 1e21), Ts=None):
    Ts = np.geomspace(1e-3, 20.0, 41) if Ts is None else Ts; D = load(el); S = {k: spl(d) for k, d in D.items()}; Z = D['scd']['iz0']
    out = {}
    for ne in nes:
        x = math.log10(ne * 1e-6); rows = []
        for T in Ts:
            y = math.log10(T * 1e3)
            def c(kind, z1):
                d = D[kind]; xx = min(max(x, d['logn'][0]), d['logn'][-1]); yy = min(max(y, d['logT'][0]), d['logT'][-1])
                return 10 ** float(S[kind][z1](xx, yy)[0, 0])
            logr = np.zeros(Z + 1)
            for z in range(Z): logr[z + 1] = logr[z] + math.log(c('scd', z + 1)) - math.log(c('acd', z + 1))
            logr -= logr.max(); f = np.exp(logr); f /= f.sum()
            Lp = sum(f[z] * c('plt', z + 1) for z in range(Z)) * 1e-6
            Lr = sum(f[z + 1] * c('prb', z + 1) for z in range(Z)) * 1e-6   # PRB block Z1 = recombining ion charge
            rows.append(dict(T_keV=float(T), mean_z=float(np.dot(np.arange(Z + 1), f)), z_dom=int(f.argmax()), sum_err=float(abs(f.sum() - 1)), L_line=float(Lp), L_rb=float(Lr)))
        out[f'{ne:.0e}'] = rows
    return Z, out

def checks(Z, tab):
    c1 = max(r['sum_err'] for rows in tab.values() for r in rows) <= 1e-10
    c2 = all(rows[i + 1]['mean_z'] >= rows[i]['mean_z'] - 1e-6 for rows in tab.values() for i in range(len(rows) - 1))
    c3 = True if Z > 18 else all(rows[-1]['mean_z'] >= 0.9 * Z for rows in tab.values())
    def ok(key):
        for rows in tab.values():
            v = [r[key] for r in rows]
            if not all(math.isfinite(x) and x > 0 for x in v): return False
            if any(max(a, b) / min(a, b) > 30 for a, b in zip(v, v[1:])): return False
        return True
    return dict(C1=c1, C2=c2, C3=c3, C4_line=ok('L_line'), C4_rb=ok('L_rb'))

if __name__ == '__main__':
    t0 = time.time(); cat = {}
    for el in Z_OF:
        try:
            Z, tab = table(el); ch = checks(Z, tab); status = 'OK' if all(ch.values()) else 'FLAGGED'
        except Exception as e:
            Z, tab, ch, status = Z_OF[el], {}, {'error': f'{type(e).__name__}: {e}'}, 'FLAGGED'
        cat[el] = dict(Z=Z, files=MAN[el], checks=ch, status=status, table=tab)
        print(f'{el:3s} Z={Z:3d} {status} {ch}', flush=True)
    meta = dict(source='OPEN-ADAS ADF11 via ProjectTorreyPines/ADAS.jl', grid='n_e 1e19,1e20,1e21 m^-3; T 1 eV-20 keV (41 log points)',
                units='L in W m^3 (coronal, per impurity ion per electron)', seconds=round(time.time() - t0, 1))
    json.dump(dict(meta=meta, elements=cat), open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'element_catalog.json'), 'w'))
    print('done', meta['seconds'], 's;', sum(v['status'] == 'OK' for v in cat.values()), 'OK of', len(cat))
