"""D216: is the locked shield fingerprint (PREREG_SHIELD item 2, derived for leaks falling as x^-p, p = 3-4) also the shape of the GROWING
leaks that today's string survey found generic (x^{+1} from a KK tower, D211; x^{3/2} from strong coupling, D204/D209)? AI-assisted.
Leak observable L(x) = x^{-p}; Delta(z) = L(x(z)) - L(x0); fingerprint = Delta(z)/Delta(z=1). x = x0 e^{lam (phi - phi0)}, lam = sqrt(2/3)."""
import math, sys
sys.path.insert(0, "/home/claude/aegis/theory/observables")
import importlib.util
spec = importlib.util.spec_from_file_location("lp", "/home/claude/aegis/theory/observables/late_predictions_d168.py")
lp = importlib.util.module_from_spec(spec)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(lp)
phi = lambda z: lp.S.sol(math.log(1 / (1 + z)))[0]
p0 = phi(0.0); lam = math.sqrt(2 / 3)
print(f"field moved since z=1: {p0 - phi(1):.3f} M_P; since z=3: {p0 - phi(3):.3f} M_P")
zs = (0.14, 0.5, 2, 3, 6)
print("p      " + "  ".join(f"z={z:<4}" for z in zs))
for p in (4, 3, 1, -1, -1.5, -3):
    L = lambda z: math.exp(-p * lam * (phi(z) - p0))           # (x/x0)^(-p)
    d1 = L(1) - 1
    print(f"{p:5}  " + "  ".join(f"{(L(z) - 1) / d1:6.3f}" for z in zs))
