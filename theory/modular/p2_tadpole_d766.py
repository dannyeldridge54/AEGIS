"""D766 (locked PREREG_D766). Reuses the D764 j-test. AI-assisted."""
import math, statistics, importlib.util
spec=importlib.util.spec_from_file_location("d764",__file__.replace("p2_tadpole_d766","second_modulus_cp_d764"))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
s,reduce=m.s,m.reduce
om=complex(-0.5,math.sqrt(3)/2)
for lab,U2 in (("U2=i",1j),("U2=omega",om)):
    v=[]; seen=set()
    for a in range(1,7):
        for b in range(1,13):
            r=b/a
            if r in seen: continue
            seen.add(r); u=(-r)/U2
            if reduce(u).imag<0.2: continue
            v.append(s(u))
    print(f"{lab}: N ratios={len(v)} fraction s_CP>0.1={sum(x>0.1 for x in v)/len(v):.2f} max s_CP={max(v):.3f} median={statistics.median(v):.3f}")
nflux=12; nD3max=(32-nflux)//2
print(f"n_flux=12 -> n_D3 <= {nD3max}")
for N in range(1,6):
    for k in (0,1):
        tot=3*N+k
        if tot<=nD3max: print(f"N={N} per half-period, origin {k}: total {tot} D3 fits; Im S*Im rho = {375*N/5:.0f}-{1220*N/5:.0f}")
