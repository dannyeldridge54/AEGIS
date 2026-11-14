"""D383 (locked): n_s, r for n = 125 vs 125 - dn (dn from Λ = V(x_E=30) instead of V(x=89)). AI-assisted."""
import math, runpy, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path("/home/claude/aegis/theory/review/gs_alpha_ns_d325.py")
dn = 0.5 * math.log((1 + 89) / (1 + 30)); print(f"dn = {dn:.4f}")
for nn in (125.0, 125.0 - dn):
    g["obs"].__globals__["n"] = nn
    ns, r, xs = g["obs"](1.0)
    print(f"n {nn:.3f}: n_s {ns:.5f}, r {r:.5f}")
