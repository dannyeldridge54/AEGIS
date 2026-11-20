import numpy as np
w=np.exp(2j*np.pi/3); fits={'A':0.03188+0.02151j,'B':0.01779+0.02926j,'C':0.00318+0.02792j}
print("fits: "+", ".join(f"{k}: |e|={abs(v):.4f} arg={np.degrees(np.angle(v)):.1f}" for k,v in fits.items()))
best={}
for m in range(1,8):
    u=0.0145/(m+0.0625)*np.exp(-2j*np.pi/9); e=1j*np.sqrt(3)*u
    d={k:abs(e-v)/abs(v) for k,v in fits.items()}
    print(f"m={m}: eps={e.real:+.5f}{e.imag:+.5f}i |e|={abs(e):.4f} arg={np.degrees(np.angle(e)):.1f}  rel.dist A {d['A']:.2f} B {d['B']:.2f} C {d['C']:.2f}")
for m,t in ((1,-0.484+0.884j),(2,-0.492+0.875j),(3,-0.495+0.872j)):
    e=t-w; print(f"listed m={m}: eps={e.real:+.5f}{e.imag:+.5f}i |e|={abs(e):.4f} arg={np.degrees(np.angle(e)):.1f}")
