"""D792 (locked PREREG_D792). AI-assisted. D781 rows hard-coded from results/late_reheat_d781.txt."""
import math
rows={1.0e-6:{3e2:(45.12,0.9669,5.200e-4),3e4:(46.64,0.9686,4.950e-4)},
      1.15e-6:{3e2:(45.12,0.9683,5.371e-4),3e4:(46.65,0.9700,5.124e-4)},
      1.3e-6:{3e2:(45.13,0.9698,5.549e-4),3e4:(46.66,0.9715,5.306e-4)}}
def interp(C,T):
    a=rows[C][3e2]; b=rows[C][3e4]; f=(math.log10(T)-math.log10(3e2))/2
    return tuple(a[i]+f*(b[i]-a[i]) for i in range(3)), f<0
MP=2.435e18; pref=(90/(math.pi**2*106.75))**0.25
ok=False
for M in (4.3e11,1e12):
    for eta in (0.3,0.6,1.0):
        T2=8.75e-11*M/((28/79)*0.75*eta)
        sph=T2>130
        if not sph: T2=8.75e-11*M/(0.75*eta)
        G=(T2/pref)**2/MP; L=(M**5/(192*math.pi**3*G))**0.25
        line=f"M={M:.1e} eta={eta}: T2={T2:.0f} GeV (sphalerons {'on' if sph else 'OFF'}), Lambda={L:.2e} GeV (M_P={MP:.1e})"
        for C in rows:
            (N,ns,r),ext=interp(C,T2)
            inside=0.970<=ns<=0.975 and 4.55e-4<=r<=5.12e-4
            line+=f" | C={C:.2e}: N*={N:.2f} n_s={ns:.4f} r={r:.2e}{'*' if ext else ''} {'IN' if inside else 'out'}"
        print(line)
        if T2>=130 and L<=MP: ok=True
print("(* = extrapolated below 3e2)")
print("VERDICT:","CONSISTENT post-hoc alternative; P5 not needed" if ok else "NOT CONSISTENT")
