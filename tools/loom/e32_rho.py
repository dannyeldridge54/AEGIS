"""D2164: exact non-holomorphic Eisenstein E(S,3/2) with the D-instanton sum, at the knot rho and at i."""
import mpmath as mp, json
mp.mp.dps = 30
def parts(S, M=60):
    x, y = mp.re(S), mp.im(S)
    pert1, pert2 = 2*mp.zeta(3)*y**1.5, 4*mp.zeta(2)*y**-0.5
    I = mp.mpf(0)
    for m in range(1, M+1):
        for n in range(1, M//m + 2):
            if m*n > M: break
            I += 2 * (mp.mpf(m)/n) * mp.cos(2*mp.pi*m*n*x) * mp.besselk(1, 2*mp.pi*m*n*y)   # m and -m together
    I *= 8*mp.pi*mp.sqrt(y)
    return pert1, pert2, I
def E(S): a, b, c = parts(S); return a + b + c
S0 = mp.mpc(0.31, 0.83)
inv = abs(E(S0) - E(-1/S0)); print('SL2Z check |E(S)-E(-1/S)| =', mp.nstr(inv, 5))
out = {'sl2z_check': float(inv)}
for name, S in [('rho', mp.exp(1j*mp.pi/3)), ('i', mp.mpc(0, 1))]:
    a, b, c = parts(S); d = c / b
    A = mp.mpf(8)/3 * 2*mp.zeta(2)/mp.zeta(3)
    out[name] = dict(pert_leading=float(a), pert_sub=float(b), instanton=float(c), delta=float(d), A=float(A), A_eff=float(A*(1+d)), E_total=float(a+b+c))
    print(name, {k: round(v, 6) for k, v in out[name].items()})
d = abs(out['rho']['delta'])
out['verdict'] = 'PROTECTED' if d < 0.05 else ('SHIFTED' if d < 0.3 else 'NOT PROTECTED')
print('verdict at rho:', out['verdict'])
json.dump(out, open('field_tests/results/d2164_e32_rho.json', 'w'), indent=1)
