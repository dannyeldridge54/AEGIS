import sys, math, cmath; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
b0, b1, G0 = 19/6, -35/6, 8.0; G1 = 8*(70/9 - 2*math.pi**2/3); mZ, mW = 91.1876, 80.385
a2Z = 0.00780372/0.232486; psi = 1 - 1j*math.pi
a2 = lambda mu: 1/(1/a2Z + b0/(2*math.pi)*math.log(mu/mZ))
def Sig(m):
    muM, muZ = 2*m, mZ; z = a2(muZ)/a2(muM); lz = math.log(z)
    Om = (-2*math.pi*G0*(z*lz + 1 - z)/(b0**2*a2(muZ)) - G0*b1*(lz - z - lz**2/2 + 1)/(2*b0**3)
          - lz/(2*b0)*(8*(math.log(4*m*m/muM**2) - 1) - 2*b0) - G1*(z - lz - 1)/(2*b0**2))
    D = a2(muZ)/(2*math.pi)*math.log(4*m*m/muZ**2)*math.log(mW**2/muZ**2)
    e = cmath.exp(Om + D); zp = cmath.exp(-4*psi/b0*lz); zm = cmath.exp(2*psi/b0*lz)
    S1 = e/3*(2*zp + zm); S12 = 2*e/3*(zp - zm); return S1, S12, z, Om, D
out = []; ftree = {(660, 'LO'): (0.133, 0.189, 0.232), (660, 'NLO'): (0.144, 0.204, 0.250), (1000, 'LO'): (0.168, 0.237, 0.291), (1000, 'NLO'): (0.185, 0.262, 0.321)}
for m, f in ((660, 0.14), (1000, 0.26)):
    S1, S12, z, Om, D = Sig(m)
    out.append(f"m={m}: z={z:.4f} Omega={Om:.4f} D={D:.4f} |S1|={abs(S1):.4f} |S1-S2|={abs(S12):.4f}")
    for lab, nlo in (('LO', False), ('NLO', True)):
        s = N.wino_s_nlo(m, v=1e-3, nlo=nlo, off_factor=math.sqrt(2))
        R = abs(s[0]*S12 + math.sqrt(2)*s[1]*S1)**2/abs(math.sqrt(2)*s[1])**2
        fm = [x/math.sqrt(R) for x in ftree[(m, lab)]]
        out.append(f"   {lab}: R(resummed/tree-SE)={R:.3f} -> f_max HESS/McM17/MWP14 = " + "/".join(f"{x:.3f}" for x in fm) + f" vs f={f}: " + "/".join('PASS' if x >= f else 'FAIL' for x in fm))
open('field_tests/results/a2d_line_nll.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
