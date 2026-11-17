import sys, math, cmath; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
b0, b1, G0 = 19/6, -35/6, 8.0; G1 = 8*(70/9 - 2*math.pi**2/3); mZ, mW = 91.1876, 80.385
a2Z = 0.00780372/0.232486; psi = 1 - 1j*math.pi
a2 = lambda mu: 1/(1/a2Z + b0/(2*math.pi)*math.log(mu/mZ))
def Sig(m, muM, muZ):
    z = a2(muZ)/a2(muM); lz = math.log(z)
    Om = (-2*math.pi*G0*(z*lz + 1 - z)/(b0**2*a2(muZ)) - G0*b1*(lz - z - lz**2/2 + 1)/(2*b0**3)
          - lz/(2*b0)*(8*(math.log(4*m*m/muM**2) - 1) - 2*b0) - G1*(z - lz - 1)/(2*b0**2))
    D = a2(muZ)/(2*math.pi)*math.log(4*m*m/muZ**2)*math.log(mW**2/muZ**2)
    e = cmath.exp(Om + D); zp = cmath.exp(-4*psi/b0*lz); zm = cmath.exp(2*psi/b0*lz)
    return e/3*(2*zp + zm), 2*e/3*(zp - zm)
m = 1000.0; ftree = {'LO': (0.168, 0.237, 0.291), 'NLO': (0.185, 0.262, 0.321)}; out = []
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(m, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); Rs = []
    for km in (1, 2, 4):
        for kz in (0.5, 1, 2):
            S1, S12 = Sig(m, km*m, kz*mZ); Rs.append(abs(s[0]*S12 + math.sqrt(2)*s[1]*S1)**2/abs(math.sqrt(2)*s[1])**2)
    lo, hi = min(Rs), max(Rs); line = f"{lab}: R in [{lo:.3f}, {hi:.3f}] (central 2m,mZ)"
    for h, ft in zip(('HESS', 'McM17', 'MWP14'), ftree[lab]):
        fa, fb = ft/math.sqrt(hi), ft/math.sqrt(lo); v = 'PASS' if fa >= 0.26 else ('FAIL' if fb < 0.26 else 'SCALE-DEPENDENT')
        line += f"; {h} f_max [{fa:.3f},{fb:.3f}] {v}"
    out.append(line)
open('field_tests/results/a2f_line_scale.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
