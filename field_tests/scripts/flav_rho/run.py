"""PREREG_FLAV_RHO.md — A4 (Gamma_3) weight-2 modular triplet at the inflation endpoint rho; Koide tests."""
import mpmath as mp, json, os
mp.mp.dps = 30
w = mp.e**(2j*mp.pi/3)
def dlogeta(t):  # d ln eta / d tau = (pi i/12) E2(tau)
    q = mp.e**(2j*mp.pi*t)
    s = mp.nsum(lambda n: n*q**n/(1-q**n), [1, mp.inf])
    return (mp.pi*1j/12)*(1-24*s)
def Y(t):  # Feruglio 1706.08749 eq. (forms of weight 2, level 3); eta'/eta(x) = d ln eta/dx
    a, b, c, d = dlogeta(t/3), dlogeta((t+1)/3), dlogeta((t+2)/3), dlogeta(3*t)
    Y1 = (1j/(2*mp.pi))*(a + b + c - 27*d)
    Y2 = (-1j/mp.pi)*(a + w**2*b + w*c)
    Y3 = (-1j/mp.pi)*(a + w*b + w**2*c)
    return [Y1, Y2, Y3]
def Q(sq):  # sq = sqrt(masses)
    sq = [abs(x) for x in sq]; return float(sum(x*x for x in sq)/sum(sq)**2)
out = {}
for name, t in [('omega', w), ('rho', w+1), ('i', 1j)]:
    y = Y(t); n = y[0]
    out[name] = dict(Y_over_Y1=[str(mp.nstr(v/n, 8)) for v in y], absY=[float(abs(v/n)) for v in y])
    C1 = Q([abs(v) for v in y])                       # sqrt(m_i) ∝ |Y_i|
    C2 = Q([mp.sqrt(abs(v)) for v in y])              # m_i ∝ |Y_i|
    lam = [y[0] + y[1]*w**k + y[2]*w**(2*k) for k in range(3)]
    C3 = Q(lam)                                       # sqrt(M) = circ(Y1,Y2,Y3)
    lam4 = [y[0] + y[2]*w**k + y[1]*w**(2*k) for k in range(3)]
    C4 = Q(lam4)                                      # circ(Y1,Y3,Y2)
    out[name].update(C1=C1, C2=C2, C3=C3, C4=C4)
# check: Y(omega) ∝ (1, omega, -omega^2/2)
yo = Y(w); chk = [complex(yo[1]/yo[0] - w), complex(yo[2]/yo[0] + w**2/2)]
out['check_omega'] = [abs(c) for c in chk]
# Koide phase from data: sqrt(m_k) = mu(1 + sqrt2 cos(delta + 2 pi k/3))
me, mm = 0.51099895, 105.6583755
for lab, mt in [('belle2', 1777.09), ('pdg', 1776.93)]:
    s = [mp.sqrt(me), mp.sqrt(mm), mp.sqrt(mt)]; mu = sum(s)/3
    # fit delta from tau (largest): cos(delta) = (s_tau/mu - 1)/sqrt2 with ordering k=0 -> tau
    A = mp.sqrt(2*(sum(x*x for x in s)/(3*mu*mu) - 1))  # amplitude (sqrt2 iff Q=2/3)
    dl = mp.acos((s[2]/mu - 1)/A)
    out['koide_'+lab] = dict(Q=Q(s), amplitude=float(A), delta=float(dl), two_ninths=2/9)
print(json.dumps(out, indent=1)); os.makedirs('field_tests/results/FLAV_RHO', exist_ok=True)
json.dump(out, open('field_tests/results/FLAV_RHO/out.json', 'w'), indent=1)
