import math
m32, at, aG = 2.58e5, 21.10, 1/28.0; gG2 = 4*math.pi*aG; M0 = m32/at
b = (33/5, 1.0, -3.0); g2 = (0.211, 0.42, 1.106); A = m32/(16*math.pi**2)
print('M0 = %.0f GeV, anomaly unit m32/16pi^2 = %.0f GeV' % (M0, A))
for s in (+1, -1):
    M = [g2[i]*(s*M0/gG2 + b[i]*A) for i in range(3)]
    wino, glu = abs(M[1]), abs(M[2]); dl_g, dl_w = math.log(glu/4930.), math.log(wino/687.)
    d = -(1/(2*math.pi))*((2.0 - 0)*dl_g + ((0 - 4/3) - (4/3 - 0)*(4/5.6))*dl_w)
    a_new = 1/(1/0.1142 + d)
    print('sign %+d: M1 %.0f  M2(wino) %.0f  M3(gluino) %.0f GeV | d(1/alpha_s) %+.3f -> alpha_s %.4f (PDG z %.1f) | wino in bar 0.67-0.70: %s'
          % (s, abs(M[0]), wino, glu, d, a_new, (a_new-0.1180)/0.0009, 670 <= wino <= 700))
x, Aw, MP = 21.10, 0.54, 2.435e18; a = 2*math.pi/6; sig = x/a
mT = a*a*Aw*math.exp(-x)*MP/math.sqrt(2*sig); H = (4.9e15)**2/(math.sqrt(3)*MP)
print('B0b: sigma %.2f, m_T ~ %.2e GeV vs H_inf %.2e GeV: ratio m_T/H = %.1e -> %s' % (sig, mT, H, mT/H, 'PASS' if mT >= H/10 else 'FAIL'))
