"""D900 (locked PREREG_D900). tau=i LH_u AD window at corrected T_R with a D653-style thermal check. AI-assisted."""
import math
MP=2.435e18; v=174.0; tgt=8.7e-11
ok=True
for TR in (0.8e6,1e6,3e6):
    for qn,Q in (("median",0.020),("max",0.087)):
        m=2*(8/23)*TR*v**2*Q/(4*MP**2*tgt)   # GeV
        M=v**2/m
        line=f"T_R={TR:.1e} GeV, {qn} Q: m_nu1={m*1e9:.2e} eV"
        for ms in (2.5e5,1.1e6):
            T=(TR**2*ms*MP)**0.25; phi=math.sqrt(ms*2*M)
            r1=phi/T; r2=0.01*T**4/(ms**2*phi**2)
            ok = ok and r1>=1e3 and r2<=1e-3
            line+=f" | m_soft={ms:.1e}: T={T:.1e}, phi/T={r1:.1e}, thermal/soft={r2:.1e}"
        print(line)
print("thermal check:", "PASS" if ok else "FAIL")
