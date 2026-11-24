"""D2232 tool (Gmeiner-Honecker 0910.0843 eqs. 62/128/129/133): N=2 lattice sums Lambda~(sigma,tau,v) and the Z6-prime SM SU(3)_a, SU(2)_b thresholds.
Coefficients transcribed via text extraction (SU(2) bracket layout ambiguous) - see D2232 for calibration status."""
import mpmath as mp
def eta(t): q = mp.exp(2j*mp.pi*t); return mp.exp(2j*mp.pi*t/24)*mp.qp(q)
def th1(z, t): return mp.jtheta(1, mp.pi*z, mp.exp(1j*mp.pi*t))
def Lt(s, tau, v):
    t = 1j*v
    if s == 0 and tau == 0: return float(mp.log(2*mp.pi*v*abs(eta(t))**4))
    return float(mp.log(abs(mp.exp(-mp.pi*s*s*v/4)*th1(tau/2 - 1j*s*v/2, t)/eta(t))**2))
def D3(v, w): return 4*Lt(0,0,v) + 4*Lt(0,0,2*v) - 6*(2-w)*Lt(1,1,v) - 7*mp.log(5) + 30*mp.log(2) + 6*mp.log(w) - 4*mp.log(3)
for v in (28.6, 30):
    print(v, [round(float(D3(v,w))/(4*mp.pi),2) for w in (1,2)])
print('v=1', [round(float(D3(1,w))/(4*mp.pi),3) for w in (1,2)], 'Lt(0,0,1)',Lt(0,0,1),'Lt(1,1,1)',Lt(1,1,1))
L5, L3, L2 = mp.log(5), mp.log(3), mp.log(2)
SU2 = {'h3': (-31, 14, (1, 0), -2, -1, mp.mpf(19)/2, -48, 1), 'h1': (-38, 14, (1, 0), -2, -16, 6, -39, 1), 'none': (-43, 16, (1, 1), -2, -20, mp.mpf(9)/2, -42, 2)}
def D2(v, case):
    a, b, (s, t), cc, c2, c3, c5, w = SU2[case]
    return a*Lt(0,0,v) + b*Lt(0,0,2*v) - 3*Lt(s,t,v) + cc*Lt(1,0,v) + c2*L2 + c3*L3 + c5*L5 - 18*mp.log(w)
for v in (28.6, 30):
    print('SU2', v, {c: round(float(D2(v,c))/(4*mp.pi),2) for c in SU2}, ' paper: h3 -9, h1 +6, none +7')
