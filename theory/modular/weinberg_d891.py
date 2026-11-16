# D891 (W2.1): size of a Z3-allowed Weinberg term (L H_u)^2/Lambda at rho vs the m_nu1 LH_u AD needs. Arithmetic only.
vu=170.0          # GeV, v sin(beta) for moderate tan(beta)
for name,L in [("reduced M_P",2.435e18),("M_P",1.22e19),("M_s low",6e15),("M_s high",3e16)]:
    m=vu**2/L*1e9   # eV
    print(f"{name:12s} Lambda={L:.2e} GeV: m_W={m:.2e} eV; c needed for m_nu1=4e-9/1.7e-8/7e-8 eV: {4e-9/m:.1e} / {1.7e-8/m:.1e} / {7e-8/m:.1e}")
# AD yield if c=1 at reduced M_P (hep-ph/0102187 scaling, n_B/s = 1e-11 d (m/1e-8)^-1.5 (m32/TeV))
m=vu**2/2.435e18*1e9
for m32 in (2.5e5,7e5):
    print(f"c=1, M_P: n_B/s = {1e-11*(m/1e-8)**-1.5*(m32/1e3):.1e} * delta_eff (m32={m32:.1e} GeV); needed 8.7e-11")
