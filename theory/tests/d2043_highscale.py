import math
H = 5.69e12; m32 = H/10; at, aG = 21.10, 1/28.0; gG2 = 4*math.pi*aG; b = (33/5, 1.0, -3.0); g2 = (0.211, 0.42, 1.106); A = m32/(16*math.pi**2)
def shift(wino, glu): return -(1/(2*math.pi))*(2.0*math.log(glu/4930.) + (-4/3 - (4/3)*(4/5.6))*math.log(wino/687.))
for name, M0 in (('mirage', m32/at), ('pure AMSB', 0.0)):
    M = [abs(g2[i]*(M0/gG2 + b[i]*A)) for i in range(3)]; d = shift(M[1], M[2]); a_s = 1/(1/0.1142 + d)
    need = (1/(1/0.1180 - d) - 0.1142)/0.0864
    print('%-9s wino %.2e gluino %.2e GeV | d(1/a_s) %+.2f -> alpha_s %.4f (z %.1f) | Delta3 shift needed %+.3f -> %s'
          % (name, M[1], M[2], d, a_s, (a_s-0.1180)/0.0009, need, 'PASS' if abs((a_s-0.1180)/0.0009) <= 2 else 'FAIL'))
