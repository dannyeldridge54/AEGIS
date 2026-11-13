"""D212: the Twist's tail slope against the Trans-Planckian Censorship bound (Bedroya-Vafa 1909.11063, eq. 19:
(|V'|/V)_inf >= 2/sqrt((d-1)(d-2)) = sqrt(2/3) in d = 4). Tail slope on rung 3alpha = k (V ~ 1/t, K = -k ln t): lambda = sqrt(2/k). AI-assisted."""
import math
tcc = 2 / math.sqrt(3 * 2)
print(f"TCC asymptotic lower bound in 4d: {tcc:.6f};  sqrt(2/3) = {math.sqrt(2/3):.6f}")
for k in range(1, 8):
    lam = math.sqrt(2 / k); p = (k - 1) / 2
    print(f"rung {k}: tail slope {lam:.4f}  TCC {'OK' if lam >= tcc - 1e-12 else 'VIOLATED'}"
          f"{' (saturates)' if abs(lam - tcc) < 1e-12 else ''};  plateau W ~ S T^{p:g} {'integer' if p == int(p) else 'half-integer'}")
