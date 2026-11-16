"""D732 (locked PREREG_D732). AI-assisted."""
import math
MP=2.435e18; gdec=10.75; cm3s=1/1.167e-17   # 1 cm^3/s in GeV^-2
for TR in (3.2e8,3.0e9):
    Y32=1.9e-12*TR/1e10
    for m32 in (2.5e5,1.1e6):
        G=193/(384*math.pi)*m32**3/MP**2; tau=6.582e-25/G
        Td=math.sqrt(G*MP/(1.66*math.sqrt(gdec)))
        print(f"T_R={TR:.1e}: Y_3/2={Y32:.2e}; m3/2={m32:.1e}: tau={tau:.1e} s, T_dec={Td*1e3:.0f} MeV")
        for M2 in (660,1000,1850):
            sv=3e-24*cm3s*(1000/M2)**2; H=1.66*math.sqrt(gdec)*Td**2/MP; s=2*math.pi**2/45*gdec*Td**3
            Yann=H/(s*sv); Yw=min(Y32,Yann); Onth=2.74e8*M2*Yw; Oth=0.12*(M2/2900)**2; tot=Onth+Oth
            print(f"   M2={M2} GeV: Y_ann={Yann:.1e}, Y_w={Yw:.1e}, Omega_nonth={Onth:.3f}, Omega_th={Oth:.3f}, total={tot:.3f} {'PASS' if tot<=0.124 else 'FAIL'}")
