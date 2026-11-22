# Blind second implementation from p.tex / exc_table.tex (LaTeX parsed, not hand-typed).
import re, itertools, json, sys
from fractions import Fraction as Fr
import sympy as sp
TEX = open('/tmp/claude-0/z6p/exc_table.tex').read()
n, m, z = sp.symbols('n m z')
def clean(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('\\,', ' ').replace('\;', ' ')
    s = re.sub(r'z\^\{\(i\)\}_\{\\alpha\}|z_\{\\alpha\}', ' z ', s)
    s = s.replace('n^i', ' n ').replace('m^i', ' m ')
    return s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
def parse_cell(cell):
    cell = clean(cell); out = []
    # entries: ( A , B )_{\alpha=LIST}
    for A, B, L in re.findall(r'\(\s*([^,]*?(?:\([^()]*\)[^,]*?)*)\s*,\s*((?:[^()]|\([^()]*\))*?)\s*\)\s*_\{\\alpha=([0-9,]+)\}', cell):
        out.append((parse_expr(A, local_dict={'n': n, 'm': m, 'z': z}, transformations=TR),
                    parse_expr(B, local_dict={'n': n, 'm': m, 'z': z}, transformations=TR), [int(a) for a in L.split(',')]))
    return out
# split table into rows by parity label
rows = {}
parts = re.split(r'\\text\{\((odd|even),(odd|even);(odd|even),(odd|even)\)\}', TEX)
for idx in range(1, len(parts), 5):
    lab = ''.join(p[0].upper() for p in parts[idx:idx+4]); body = parts[idx+4]
    body = body.split('\\\\\\hline')[0]
    cells = body.split('&')[1:5]
    rows[lab] = [parse_cell(c) for c in cells]
assert len(rows) == 9, rows.keys()
for lab, cells in rows.items():
    for ci, c in enumerate(cells):
        labs = sorted(a for _, _, L in c for a in L); assert len(labs) == 3, (lab, ci, labs)
# alpha label formulas per block (from the table; block 3 alpha1 typo read as sigma^j, as recorded)
BLK = {1: lambda j, k: (1 + k*(3 + j), 2 + j*(3 - k), 3 + j + 2*k - 3*j*k),
       2: lambda j, k: (1 + k*(2 + j), 2 + j*(2 - k), 5 - 2*j - k + 3*j*k),
       3: lambda j, k: (1 + k*(4 - 2*j), 2 + j*(1 + 2*k), 4 + j - k)}
ROWBLK = {}
order = re.findall(r'\\text\{\((odd|even),(odd|even);(odd|even),(odd|even)\)\}', TEX)
for i, t in enumerate(order): ROWBLK[''.join(p[0].upper() for p in t)] = 1 + i//3
COL = {(0, 0): 0, (1, 0): 1, (0, 1): 2, (1, 1): 3}
def par(v): return 'O' if v % 2 else 'E'
def XY(w):
    N = (w[0], w[2], w[4]); M = (w[1], w[3], w[5]); cyc = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    X = N[0]*N[1]*N[2] - M[0]*M[1]*M[2] - sum(N[i]*M[j]*M[k] for i, j, k in cyc)
    Y = sum(N[i]*N[j]*M[k] + N[i]*M[j]*M[k] for i, j, k in cyc)
    return X, Y
def exc(w, eig, tau, sig):
    """eig: '+-' string Z2^(i) eigenvalues; Z2 eigenvalue acts as overall sign (z0 reading); (j,k) increasing."""
    E = {}
    for i in (1, 2, 3):
        j, k = [t for t in (1, 2, 3) if t != i]
        ni, mi = w[2*i-2], w[2*i-1]
        lab = par(w[2*j-2]) + par(w[2*j-1]) + par(w[2*k-2]) + par(w[2*k-1])
        sj, sk = sig[j-1], sig[k-1]; z0 = 1 if eig[i-1] == '+' else -1
        a1, a2, a3 = BLK[ROWBLK[lab]](sj, sk)
        zz = {a1: (-1)**tau[j-1], a2: (-1)**tau[k-1], a3: (-1)**(tau[j-1] + tau[k-1])}
        d = {a: (0, 0) for a in range(1, 6)}
        for A, B, L in rows[lab][COL[(sj, sk)]]:
            for a in L:
                sub = {n: ni, m: mi, z: zz[a]}
                d[a] = (int(z0*A.subs(sub)), int(z0*B.subs(sub)))
        E[i] = d
    return E
ETA = -1
def img(c):
    X, Y, E = c; E2 = {}
    for k, d in E.items():
        e = {}
        for a, (x, y) in d.items():
            ap = {4: 5, 5: 4}.get(a, a); e[ap] = (-ETA*x - ETA*y, ETA*y)   # eps->-eta eps', epst->eta(epst'-eps')
        E2[k] = e
    return (X + Y, -Y, E2)
def I(c1, c2):
    (X1, Y1, E1), (X2, Y2, E2) = c1, c2
    ex = sum(E1[k][a][0]*E2[k][a][1] - E1[k][a][1]*E2[k][a][0] for k in (1, 2, 3) for a in range(1, 6))
    return Fr(4*(X1*Y2 - Y1*X2) - 4*ex, 16)
def tad(stacks):
    bulk = sum(N*(2*c[0] + c[1]) for N, c in stacks); r = []
    for i in (1, 2, 3):
        for a in (1, 2, 3):
            r.append(sum(N*(c[2][i][a][0] - ETA*(c[2][i][a][0] + c[2][i][a][1])) for N, c in stacks))
            r.append(sum(N*(1 + ETA)*c[2][i][a][1] for N, c in stacks))
        r.append(sum(N*((2*c[2][i][4][0] + c[2][i][4][1]) - ETA*(2*c[2][i][5][0] + c[2][i][5][1])) for N, c in stacks))
        r.append(sum(N*(c[2][i][4][1] + ETA*c[2][i][5][1]) for N, c in stacks))
    return bulk, r
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
RND = {'r1': (1, (1,0,1,0,1,0), '-+-', (1,0,0), (0,1,1)), 'r2': (1, (1,1,0,1,1,-1), '+--', (0,1,0), (1,0,1)),
       'r3': (1, (-1,2,1,1,2,-1), '++-', (1,1,0), (0,0,1))}
C = {}
for k, (N, w, e, t, s) in {**T27, **RND}.items():
    X, Y = XY(w); C[k] = (X, Y, exc(w, e, t, s)); C[k+"'"] = img(C[k])
def vec(c): return [c[0], c[1]] + [c[2][k][a] for k in (1, 2, 3) for a in range(1, 6)]
out = {'cycles': {k: vec(C[k]) for k in list(T27) + list(RND)}}
b, r = tad([(T27[k][0], C[k]) for k in T27]); out['tadpole_bulk'] = b; out['twisted_residuals'] = r
names = list(T27) + [k+"'" for k in T27]
out['chi_T27'] = {x+'.'+y: str(I(C[x], C[y])) for x in T27 for y in names if I(C[x], C[y]) != 0}
out['chi_random'] = {x+'.'+y: str(I(C[x], C[y])) for x in RND for y in list(T27) + [k+"'" for k in T27] + [x+"'"]}
out['self_images_T27'] = {k: str(I(C[k], C[k+"'"])) for k in T27}
print(json.dumps(out))
json.dump(out, open('blind_out.json', 'w'), indent=0)
