"""Chronos A3 branches (D2189): Ac-225 chain + Ac-227, Pu separation age, tritium, decay heat, cosmochronometry."""
import math, json
import numpy as np
from scipy.linalg import expm
from chronos import LAM as LAM0, MIN, H, D, Y

T12x = {'Ac-225': 9.920 * D, 'Fr-221': 4.801 * MIN, 'At-217': 32.6e-3, 'Bi-213': 45.61 * MIN, 'Po-213': 3.72e-6,
        'Tl-209': 2.162 * MIN, 'Pb-209': 3.234 * H, 'Ac-227': 21.772 * Y, 'H-3': 12.32 * Y,
        'Th-232': 1.40e10 * Y, 'U-238': 4.468e9 * Y, 'U-235': 7.04e8 * Y, 'Pu-241': 14.29 * Y, 'Am-241': 432.6 * Y}
LAM = dict(LAM0); LAM.update({k: math.log(2) / v for k, v in T12x.items()})
AC_CHAIN = ['Ac-225', 'Fr-221', 'At-217', 'Bi-213', 'Po-213', 'Tl-209', 'Pb-209', 'Bi-209']
AC_LINKS = [('Ac-225', 'Fr-221', 1.0), ('Fr-221', 'At-217', 1.0), ('At-217', 'Bi-213', 1.0),
            ('Bi-213', 'Po-213', 0.978), ('Bi-213', 'Tl-209', 0.022), ('Po-213', 'Pb-209', 1.0),
            ('Tl-209', 'Pb-209', 1.0), ('Pb-209', 'Bi-209', 1.0)]

def network(nucs, links, N0, t):
    idx = {k: i for i, k in enumerate(nucs)}; n = len(nucs); M = np.zeros((n, n))
    for k in nucs:
        if k in LAM: M[idx[k], idx[k]] = -LAM[k]
    for a, b, br in links: M[idx[b], idx[a]] += br * LAM[a]
    return expm(M * t) @ np.asarray(N0, float)

def ac225_activities(t, A0_Bq=1.0):
    N0 = np.zeros(len(AC_CHAIN)); N0[0] = A0_Bq / LAM['Ac-225']
    N = network(AC_CHAIN, AC_LINKS, N0, t)
    return {k: (LAM[k] * N[i] if k in LAM else 0.0) for i, k in enumerate(AC_CHAIN)}, N

def ac227_fraction(t, ratio_eob):
    """Ac-227 / Ac-225 activity ratio after storage t, given the ratio at end of bombardment."""
    return ratio_eob * math.exp(-(LAM['Ac-227'] - LAM['Ac-225']) * t)

def pu_age(am_over_pu_activity):
    """Years since separation (Am-241 = 0 at separation) from the Am-241/Pu-241 ACTIVITY ratio."""
    lp, la = LAM['Pu-241'], LAM['Am-241']; br = 0.99998
    # A_Am/A_Pu = br*la/(la-lp) * (1 - exp(-(la-lp) t))   (la < lp)
    k = br * la / (la - lp); x = 1 - am_over_pu_activity / k
    return -math.log(x) / (la - lp) / Y

def pu_ratio(t_y):
    lp, la = LAM['Pu-241'], LAM['Am-241']; br = 0.99998
    return br * la / (la - lp) * (1 - math.exp(-(la - lp) * t_y * Y))

def tritium(N0_g, t_y):
    rem = N0_g * math.exp(-LAM['H-3'] * t_y * Y); return rem, (N0_g - rem) * 3.016029 / 3.016049  # He-3 grams (mass ratio)

def decay_heat_way_wigner(t_s, T_op_s):
    return 0.0622 * (t_s ** -0.2 - (t_s + T_op_s) ** -0.2)   # Way-Wigner approximation, not ANS-5.1

def cosmo_age(obs_ratio, prod_ratio, a='Th-232', b=None, stable_ref=True):
    """Age (Gyr) from N(a)/N(ref) now vs production. ref stable (e.g. Eu) -> lambda_a only; else lambda_a - lambda_b."""
    lam = LAM[a] - (0 if stable_ref else LAM[b])
    return math.log(prod_ratio / obs_ratio) / lam / Y / 1e9

if __name__ == '__main__':
    R = {}
    # T11
    A, N = ac225_activities(6 * H); A0 = ac225_activities(0.0)[0]
    lam_ac, lam_bi = LAM['Ac-225'], LAM['Bi-213']; eq = lam_bi / (lam_bi - lam_ac)   # transient equilibrium A_Bi/A_Ac
    frac6 = (A['Bi-213'] / A['Ac-225']) / eq
    tot = sum(N); N0tot = 1.0 / LAM['Ac-225']
    R['T11'] = dict(Bi213_over_eq_at_6h=frac6, atom_conservation_rel=abs(tot - N0tot) / N0tot,
                    pass_=bool(frac6 > 0.99 and abs(tot - N0tot) / N0tot < 1e-12))
    R['Ac227_example'] = {f'{d} d': ac227_fraction(d * D, 0.0015) for d in (0, 10, 20, 30)}
    err = max(abs(pu_age(pu_ratio(t)) - t) for t in (1, 10, 50)); R['T12'] = dict(max_err_y=err, pass_=bool(err < 1e-9))
    f = 1 - math.exp(-LAM['H-3'] * Y); R['T13'] = dict(annual_fraction=f, pass_=bool(abs(f - 0.0547) < 0.0005))
    R['T14_report'] = {lab: decay_heat_way_wigner(t, Y) for lab, t in (('1 h', H), ('1 d', D), ('1 y', Y))}
    rt = max(abs(cosmo_age(1.0 * math.exp(-LAM['Th-232'] * a * 1e9 * Y), 1.0) - a) for a in (5, 10, 13))
    R['T15'] = dict(roundtrip_err_Gyr=rt, pass_=bool(rt < 1e-9), note='no published example quoted; inversion test only')
    json.dump(R, open('d2189_a3.json', 'w'), indent=1); print(json.dumps(R, indent=1))
