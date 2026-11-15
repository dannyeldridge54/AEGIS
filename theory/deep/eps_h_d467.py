import sys; sys.path.insert(0,'theory/deep'); from capture_ext_d460 import run
for ms in (1e-9,1.0,1e4):
    refl,xmin,ret,xf,rem=run(ms,1.43e-4,32.0)
    e=rem*(4/3)/1.5e11
    print(f"m_s={ms:.0e} GeV: hits {len(refl)}, rem rho/s={rem:.2e} GeV, eps_h={e:.2e} -> {'ok' if e<=5.5e-5 else 'EXCEEDS'}",flush=True)
