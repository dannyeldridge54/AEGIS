import math
eps=lambda m: math.sqrt(3)*0.0145/(m+0.0625)
S={'up':(1.29e-3,0.629,169.0),'down':(2.80e-3,55.7e-3,2.794)}
for n,(m1,m2,m3) in S.items():
    ea,eb=m2/m3,math.sqrt(m1/m3); g=math.sqrt(ea*eb)
    match=[m for m in range(1,17) if all(eps(m)/3<=e<=3*eps(m) for e in (ea,eb))]
    best=min(range(1,17),key=lambda m: abs(math.log(eps(m)/g)))
    print(f"{n}: e_a={ea:.4f} e_b={eb:.4f} geo={g:.4f}  matching m={match}  closest m={best} (|eps|={eps(best):.4f}{', EXTRAPOLATED' if best>7 else ''})")
print("|eps(m)|:", " ".join(f"{m}:{eps(m):.4f}" for m in range(1,17)))
