"""D531 (locked PREREG_D531_LAMBDA_AXION). AI-assisted."""
import math
MP=2.435e18; hbar=6.582e-25; Mpc=3.0857e19  # GeV s ; km
H0=67.7/Mpc*hbar  # GeV
Lam=3*H0**2*MP**2*0.69
SW=121.6; ok=True
for m_over in (2,1e4):
    for f in (3.7e12,7.6e12):
        Va=(m_over*H0)**2*f**2; dS=-math.log(Va/Lam); Sp=SW+dS; Sa=SW+Sp
        p=dS>0 and 242<=Sa<=267; ok&=p
        print(f"m={m_over:g} H0, f={f:.1e}: V_a/Lambda={Va/Lam:.2e}, dS={dS:.1f}, S'={Sp:.1f}, V-level axion action={Sa:.1f} {'in' if 242<=Sa<=267 else 'OUT of'} 242-267")
print(f"H0={H0:.3e} GeV, Lambda={Lam:.3e} GeV^4, S_Lambda(V-level)={2*SW:.1f}"); print("PASS" if ok else "FAIL")
