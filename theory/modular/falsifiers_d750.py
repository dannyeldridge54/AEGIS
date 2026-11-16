"""D750 (locked PREREG_D750). AI-assisted."""
import math, numpy as np
d=math.radians; s12,s13=math.sin(d(33.4)),math.sin(d(8.6)); c12,c13=math.cos(d(33.4)),math.cos(d(8.6))
Ue=np.array([c12*c13, s12*c13, s13])          # |U_ei|; Dirac phase enters U_e3^2 as a phase, absorbed in the scan
a=np.linspace(0,2*math.pi,72,endpoint=False); A21,A31=np.meshgrid(a,a)
for m1 in (0,1e-4,1e-3,5e-3):
    m=np.array([m1, math.sqrt(m1**2+7.42e-5), math.sqrt(m1**2+2.5e-3)])
    mbb=np.abs(Ue[0]**2*m[0] + Ue[1]**2*m[1]*np.exp(1j*A21) + Ue[2]**2*m[2]*np.exp(1j*A31))
    mb=math.sqrt(float(np.sum(Ue**2*m**2)))
    print(f"m1={m1:g} eV: Sigma={m.sum():.4f} eV, m_bb={mbb.min()*1e3:.2f}-{mbb.max()*1e3:.2f} meV, m_beta={mb*1e3:.2f} meV")
