"""D194: T-duality vs the Twist's rim/centre, and a Gamma0(9) cusp escape. AI-assisted.
If T_het has full SL(2,Z) duality, V(T) = V(-1/T): the small-x plateau and the large-x tail would be the same physics. Under Gamma0(N)
without the Fricke involution, the cusps 0 (small T) and i*inf (large T) are inequivalent. Gamma0(9) has genus 0, hauptmodul
h(T) = (eta(T)/eta(9T))^3 (24/(N-1) = 3). Test s = 1/(1 + c h): s -> 0 at i*inf (h ~ 1/q), s -> 1 at the cusp 0 (h ~ 27 e^{-2pi/(9y)})."""
import mpmath as mp
mp.mp.dps = 30
def eta(tau):
    q = mp.e ** (2j * mp.pi * tau)
    return mp.e ** (2j * mp.pi * tau / 24) * mp.qp(q)
h = lambda y: (eta(1j * y) / eta(9j * y)) ** 3
print("  y=Im T_het     h(y) (real)       27 e^{-2pi/(9y)}     e^{2pi y}")
for y in (0.02, 0.05, 0.1, 0.2, 1/3, 0.5, 1, 2):
    hv = h(mp.mpf(y)).real
    print(f"  {y:8.4f}   {float(hv):14.6e}   {float(27*mp.e**(-2*mp.pi/(9*y))):14.6e}   {float(mp.e**(2*mp.pi*y)):12.4e}")
# where s = 1/(1+h) crosses 1/2 (c = 1): the cliff's location in a Gamma0(9)-covariant E
y_half = mp.findroot(lambda y: h(y).real - 1, 0.3)
print(f"s = 1/2 at Im T_het = {float(y_half):.4f} -> x = 8 T_het = {float(8*y_half):.3f} (the Twist's cliff is at x ~ 0.01)")
yc = mp.mpf(0.01) / 8
print(f"to keep the cliff at x = 0.01 needs c ~ 1/h = {mp.nstr(1/h(yc).real, 5)}")
