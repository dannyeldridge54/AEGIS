import math
MP,gs,g=2.435e18,106.75,0.7; Ms=0.1*MP; MV=g*Ms; T=1.5e11; c=math.sqrt(2/3); xE=29.6
H=math.sqrt(math.pi**2*gs/90)*T**2/MP
G=g**4*T**5/MV**4
print(f"(a) M_V={MV:.2e} GeV; Gamma={G:.2e} GeV vs H={H:.2e} GeV -> ratio {G/H:.1e} (no thermal contact)")
rs=1e-5*0.75*T; print(f"(b) worst-case rho_phi/s={rs:.2e} GeV vs DM 4.3e-10 -> overclosure x{rs/4.3e-10:.1e}")
zp=2.4694e-3; dp=0.0100; xdot=c*xE*H*dp   # GeV (x per GeV^-1)
for ms in (1e4,1e5):
    for dx in (1e-3,1e-6,0.0):     # distance below x_E
        m2=ms**2+g**2*zp*dx*Ms**2
        dm2dt=g**2*zp*Ms**2*xdot
        A=abs(dm2dt)/(2*m2**1.5)
        print(f"(c) m_s={ms:.0e}, x_E-x={dx:.0e}: m_eff={math.sqrt(m2):.2e} GeV, A={A:.2e}")
