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
CONV = 0.389379e-27*2.99792458e10; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
halos = {'bench': 1.0, 'McM17': 0.494, 'GaiaDR3': 0.427, 'MWP14': 0.325}; out = []
for lab, nlo in (('LO', False), ('NLO', True)):
    for M in (1100.0, 1200.0, 1300.0, 1500.0):
        s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv0 = 2*s[1]**2*math.pi*N.ALPHA**2/M**2*CONV*k
        Rs = [abs(s[0]*S12 + math.sqrt(2)*s[1]*S1)**2/abs(math.sqrt(2)*s[1])**2 for S1, S12 in (Sig(M, km*M, kz*mZ) for km in (1, 2, 4) for kz in (0.5, 1, 2))]
        flo, fhi = (M/2842)**2, (M/2207)**2; line = f"{lab} M={M/1e3:.1f}: f [{flo:.3f},{fhi:.3f}] R [{min(Rs):.2f},{max(Rs):.2f}]"
        for h, jr in halos.items():
            pes = math.sqrt(2.3e-28/(sv0*max(Rs)*jr)); opt = math.sqrt(6.5e-28/(sv0*min(Rs)*jr))
            v = 'PASS' if pes >= fhi else ('FAIL' if opt < flo else 'UND')
            line += f" | {h} [{pes:.3f},{opt:.3f}] {v}"
        out.append(line)
open('field_tests/results/a2k_upper_edge.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
