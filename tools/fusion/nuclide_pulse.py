"""PULSE-NUCLIDES: NUBASE2020 catalogue + audit of Chronos half-lives and the fusion engine's masses."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SEC = dict(ys=1e-24, zs=1e-21, as_=1e-18, fs=1e-15, ps=1e-12, ns=1e-9, us=1e-6, ms=1e-3, s=1.0, m=60.0, h=3600.0, d=86400.0)
YR = 365.2422 * 86400.0
for k, p in dict(y=0, ky=3, My=6, Gy=9, Ty=12, Py=15, Ey=18, Zy=21, Yy=24).items(): SEC[k] = YR * 10 ** p
def parse(path=os.path.join(HERE, 'nubase', 'nubase_4.mas20.txt')):
    out = []
    for L in open(path):
        if L.startswith('#') or len(L) < 80: continue
        A = int(L[0:3]); Z = int(L[4:7]); iso = int(L[7]); name = L[11:16].strip() + L[16].strip()
        me = L[18:31].strip(); me_est = '#' in me; me = float(me.replace('#', '')) if me.replace('#', '') else None
        T = L[69:78].strip(); u = L[78:80].strip(); t12 = None; stable = T.startswith('stbl')
        if T and not stable and not T.startswith('p-unst'):
            try: t12 = float(T.replace('#', '').replace('>', '').replace('<', '').replace('~', '')) * SEC['as_' if u == 'as' else u]
            except (ValueError, KeyError): t12 = None
        modes = L[119:].strip()
        out.append(dict(A=A, Z=Z, iso=iso, name=name, me_keV=me, me_est=me_est, t12_s=t12, stable=stable, unst=T.startswith('p-unst'), modes=modes[:60]))
    return out
SYM = 'n H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr'.split()
def key(name):   # Chronos style "Tc-99m" -> (Z, A, isomer flag)
    m = re.match(r'([A-Za-z]+)-(\d+)(m?)$', name); el, A, isom = m.group(1), int(m.group(2)), m.group(3) == 'm'
    return SYM.index(el), A, isom
if __name__ == '__main__':
    pass
