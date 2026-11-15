import sys, math, cmath, random; sys.path.insert(0,'theory/modular'); import modular_lib as L
H=lambda J:(J-1728)**0.5*(J+1)   # arbitrary test H (any holomorphic H must give invariance)
rng=random.Random(1); worst=0
for _ in range(8):
    t=complex(rng.uniform(-0.5,0.5),rng.uniform(0.9,1.6))
    for g in (lambda z:z+1, lambda z:-1/z, lambda z:(2*z+1)/(z+1)):
        worst=max(worst,abs(L.lnV(g(t),H)-L.lnV(t,H)))
print(f"j(i) = {L.j(1j).real:.4f} (expect 1728); j(rho) = {abs(L.j(cmath.exp(1j*math.pi/3))):.2e} (expect 0)")
print(f"max |ln V(g tau) - ln V(tau)| over SL(2,Z) moves = {worst:.2e}  (invariance check)")
