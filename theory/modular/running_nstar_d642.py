import math
src=open('theory/modular/running_d632.py').read().splitlines()
exec('\n'.join(src[:41]))
for name,e in (('Kairos',0.0),('two-term 1.3e-4',1.3e-4),('two-term 1.6e-4',1.6e-4)):
    B=background(e)
    for Ns in (46.08,49.21):
        S=[-0.1,-0.05,0,0.05,0.1]; lp=[math.log(spectra(B,Ns,math.exp(x))[0]) for x in S]
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
        a=(ns[2]-ns[0])/0.1; n0=ns[1]; att=-(1-n0)**2/2
        print(f"{name} N*={Ns}: n_s={n0:.4f} alpha_s={a:.2e} attractor={att:.2e} ratio={a/att:.2f}",flush=True)
