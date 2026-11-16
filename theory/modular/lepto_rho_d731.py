"""D731 (locked PREREG_D731). AI-assisted. Cases/T_R from results/tr_2p1_d725.txt."""
import math
m=2.2e13; mnu=0.05e-9; v=174.; Yobs=8.75e-11
ratio={0.3:0.082343/0.38817, 1:0.274478/0.38817, 3:0.38817/0.823433}   # light/heavy (c=3: the single state is lighter)
cases=[(0.3,1e12,3.175e8),(0.3,1e13,3.033e9),(0.3,5e13,2.076e9),(1,1e12,4.287e8),(1,1e13,2.543e9),(3,1e12,9.459e8)]
for c,MH,TR in cases:
    ML=ratio[c]*MH
    for lab,M in (("light",ML),("heavy",MH)):
        if M>=m/2 and lab=="heavy": continue
        eDI=3*M*mnu/(16*math.pi*v**2); Y=(8/23)*(3/4)*(TR/m)*2*eDI
        print(f"c={c} M_H={MH:.0e}: decaying {lab} M={M:.2e}, T_R={TR:.2e}, M/T_R={M/TR:.0f}, eps_DI={eDI:.2e}, Y_B(max)={Y:.2e}, need sin(delta)>={Yobs/Y:.2f} {'PASS' if Y>=Yobs and M/TR>=10 else 'fail'}")
