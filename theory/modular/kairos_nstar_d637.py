import math
src=open('theory/modular/exact_ns_d588.py').read().splitlines()
exec('\n'.join(src[:42]))
B=background(0.0)
for Ns in (46.08,47.60,49.21):
    Pm,_,_=spectra(B,Ns,math.exp(-0.05)); Pp,_,_=spectra(B,Ns,math.exp(0.05)); P0,Pt,ys=spectra(B,Ns,1.0)
    ns=1+(math.log(Pp)-math.log(Pm))/0.1; r=Pt/P0
    print(f"Kairos N*={Ns}: y*={ys:.2f} n_s={ns:.4f} r={r:.2e} | SPA {(ns-0.9684)/0.003:+.1f}σ, SPA+DESI {(ns-0.9728)/0.0027:+.1f}σ | CMB(2512.10613) {(ns-0.9682)/0.0032:+.1f}σ, CMB+DESI {(ns-0.9728)/0.0029:+.1f}σ",flush=True)
