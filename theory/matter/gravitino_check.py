"""H-GRAV test: can a superheavy gravitino be the dark matter at the reheating the Twist's matter formation needs?
Thermal abundance (Dudas, Mambrini & Olive, arXiv:1704.03008, Eq. 9; valid for m_3/2 < T_RH < M_SUSY):
    Omega h^2 = 0.11 (0.1 EeV / m_3/2)^3 (T_RH / 2.0e10 GeV)^7.
The paper's allowed window (Eq. 13): 2.7e10 <~ T_RH <~ 1.1e12 GeV. AI-assisted."""
EEV = 1e9
for T in (1e12, 1e13, 1e14, 1e15):
    m = 0.1 * EEV * (T / 2.0e10) ** (7 / 3)            # m_3/2 giving Omega h^2 = 0.11
    print(f"T_RH {T:.0e} GeV: gravitino DM needs m_3/2 = {m:.1e} GeV -> {'OK (m < T_RH)' if m < T else 'NOT POSSIBLE: m_3/2 > T_RH, no thermal production'}")
