import math
c=math.sqrt(3)*0.0145; e=lambda m: c/(m+1/16)
def g(m1,m2,m3): ea,eb=m2/m3,math.sqrt(m1/m3); return ea,eb,math.sqrt(ea*eb)
S={'down':(2.80e-3,55.7e-3,2.794),'up':(1.29e-3,0.629,169.0),'charged leptons':(0.51099895,105.6583755,1776.93)}
for n,v in S.items():
    ea,eb,gg=g(*v); ok=all(e(1)/3<=x<=3*e(1) for x in (ea,eb))
    print(f"T1 {n}: e_a={ea:.4f} e_b={eb:.4f} g={gg:.4f} on rung 1: {ok}")
gd=g(*S['down'])[2]; gu=g(*S['up'])[2]; ms=(1+1/16)*gd/gu-1/16; d=abs(ms-round(ms))
print(f"T2 m_u* = {ms:.3f}; nearest {round(ms)}; |dev| = {d:.3f}; chance of being this close = {2*d:.2f}")
gl=g(*S['charged leptons'])[2]; ml=(1+1/16)*gd/gl-1/16; print(f"T2' charged-lepton rung from down anchor = {ml:.3f}")
ea=8.65e-3/50.1e-3; print(f"T3 neutrinos e_a = {ea:.3f} vs 3 e(1) = {3*e(1):.4f} -> {'OFF ladder' if ea>3*e(1) else 'on ladder'}")
print("T4 e(m):", " ".join(f"{m}:{e(m):.4f}" for m in (1,2,4,8,16,24,32,48,64)), "| first m with e<1e-3:", next(m for m in range(1,200) if e(m)<1e-3))
