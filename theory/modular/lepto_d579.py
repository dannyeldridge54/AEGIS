"""D579 (locked PREREG_D579_NONTHERMAL_LEPTO). AI-assisted."""
import re, math
m3=0.05e-9; v=174.; Yt=8.75e-11
pref=(8/23)*(3/4)*2
for f in (1/3,1/2): print(f"T_RH,min (M1=m*{f:.3f}, Br=1, DI bound) = {Yt/(pref*(3/(16*math.pi))*f*m3/v**2):.2e} GeV")
for line in open('field_tests/results/osc_nstar_d578.txt'):
    g=re.search(r"^(\S+ \S+) c_G=(\d+) \[(.*?)\]: m=(\S+) GeV .*?T_RH=(\S+) GeV",line)
    if not g: continue
    name,cG,lab,m,T=g.groups(); m=float(m); T=float(T)
    out=[]
    for f in (1/3,1/2):
        eps=3*f*m*m3/(16*math.pi*v**2); Y=pref*(T/m)*eps; out.append(f"M1=m/{round(1/f)}: eps1<={eps:.1e} Y_B<={Y:.2e} {'PASS' if Y>=Yt else 'FAIL'}")
    print(f"{name} c_G={cG} [{lab}] m={m:.2e} T_RH={T:.2e}: "+" | ".join(out))
