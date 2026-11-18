"""D815 (locked PREREG_D815). D632 MS code unchanged. AI-assisted."""
import math
src=open('theory/modular/running_d632.py').read().splitlines()
exec('\n'.join(src[:41]))
BG={}
def obs(e,Ns):
    if e not in BG: BG[e]=background(e)
    B=BG[e]; S=[-0.1,-0.05,0,0.05,0.1]; out=[spectra(B,Ns,math.exp(x)) for x in S]
    lp=[math.log(o[0]) for o in out]; ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
    return ns[1], out[2][1]/out[2][0], (ns[2]-ns[0])/0.1
# NA12 driver (locked PREREG_NA12)
print("NA12: N*(eps) = 50.31 + 0.5 ln(m(eps)/1.9e11)", flush=True)
for e in (1.30e-4,1.35e-4,1.40e-4,1.45e-4,1.50e-4):
    m=2.28e11+(e-1.3e-4)/(0.3e-4)*(2.65e11-2.28e11); Ns=50.31+0.5*math.log(m/1.9e11)
    n,r,a=obs(e,Ns); print(f"eps={e:.2e} m={m:.3e} N*={Ns:.3f}: n_s={n:.5f} r={r:.4e} alpha_s={a:.3e} inband={0.970<=n<=0.975 and 4.8e-4<=r<=5.7e-4}",flush=True)
print(f"D861 check: ImS = 0.1125/0.232 = {0.1125/0.232:.3f}; C = {15*4/(64*math.pi**6*781):.4e}", flush=True)
