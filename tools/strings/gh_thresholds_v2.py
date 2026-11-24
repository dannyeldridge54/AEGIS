"""Gmeiner-Honecker 0910.0843v2 thresholds, Z6' SM (eqs. 128, 129, 133), coefficients read from the source PDF. Calibrated in D2232/D2233."""
import mpmath as mp
def eta(t): q = mp.exp(2j*mp.pi*t); return mp.exp(2j*mp.pi*t/24)*mp.qp(q)
def th1(z, t): return mp.jtheta(1, mp.pi*z, mp.exp(1j*mp.pi*t))
def Lt(s, tau, v):
    t = 1j*v
    if s == 0 and tau == 0: return float(mp.log(2*mp.pi*v*abs(eta(t))**4))
    return float(mp.log(abs(mp.exp(-mp.pi*s*s*v/4)*th1(tau/2 - 1j*s*v/2, t)/eta(t))**2))
L5, L3, L2 = mp.log(5), mp.log(3), mp.log(2)
CASE = {'h3': (1, 0, -5, 9, 0), 'h1': (1, -7, -20, 0, -mp.mpf(7)/2), 'none': (2, 0, 0, 0, 0)}   # omega, d_L00, d_ln2, d_ln5, d_ln3 (eq. 129)
def D2(v, case, sc=0.5, tc=0):
    w, dL, d2, d5, d3 = CASE[case]
    return ((-12*w - 19 + dL)*Lt(0,0,v) + (2*w + 12)*Lt(0,0,2*v) - 3*Lt(1, w-1, v) - 2*Lt(sc, tc, v)
            + (-24*w + 28 + d2)*L2 - (36 + 3*w + d5)*L5 - 18*mp.log(w) + (mp.mpf(29)/2 - 5*w + d3)*L3)
def D3(v, w): return 4*Lt(0,0,v) + 4*Lt(0,0,2*v) - 6*(2-w)*Lt(1,1,v) - 7*L5 + 30*L2 + 6*mp.log(w) - 4*L3
if __name__ == '__main__':
    for v in (28.6, 30):
        print(v, 'SU3', [round(float(D3(v,w))/(4*mp.pi),2) for w in (1,1,2)], 'paper -34 -34 -26 | SU2', [round(float(D2(v,c))/(4*mp.pi),2) for c in CASE], 'paper -9 +6 +7')
