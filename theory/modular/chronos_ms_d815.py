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
n,r,a=obs(1.3e-4,46.08); print(f"K4 eps=1.3e-4 N*=46.08: n_s={n:.4f} alpha_s={a:.2e} r={r:.3e}",flush=True)
print("(a) D729 rows",flush=True)
for e,Nl in ((1.3e-4,(49.95,48.38,50.31,48.75)),(1.6e-4,(49.93,48.40,50.30,48.76))):
    for Ns in Nl:
        n,r,a=obs(e,Ns); print(f"eps={e:.2e} N*={Ns}: n_s={n:.4f} r={r:.3e} alpha_s={a:.2e} inband={0.970<=n<=0.975 and 4.8e-4<=r<=5.7e-4}",flush=True)
print("(b) eps window",flush=True)
for Ns in (48.38,50.31):
    for e in (1.30e-4,1.35e-4,1.40e-4,1.45e-4,1.50e-4,1.55e-4,1.60e-4):
        n,r,a=obs(e,Ns); print(f"N*={Ns} eps={e:.2e}: n_s={n:.4f} r={r:.3e} inband={0.970<=n<=0.975 and 4.8e-4<=r<=5.7e-4}",flush=True)
