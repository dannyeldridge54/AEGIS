"""D649 (locked PREREG_D649_M32_POSITIVITY). AI-assisted."""
import mpmath as mp, math
src=open('theory/modular/m32_bound_d648.py').read().split('H=3.7e12')[0]
exec(src)
H=3.7e12
for y in (23,24.5,26,28,30):
    y=mp.mpf(y); t=1j*y
    dLL=L(t)-Li; br=mp.e**dLL*(4*y**2*abs(dL(t))**2-3)
    b=mp.sqrt(3*Vpl(y,1.3e-4)/br)
    print(f"y={float(y)}: e^(L-Li)={mp.nstr(mp.e**dLL,4)}, bracket={mp.nstr(br,4)} -> m3/2/H < {mp.nstr(b,3)}, m3/2 < {float(b)*H:.2e} GeV",flush=True)
