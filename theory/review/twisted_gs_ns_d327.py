"""D327 (locked, PREREG_D327_TWISTED_GS): n_s, r for alpha = 1 + delta^2/3 from twisted-moduli GS. Reuses D325's obs(). AI-assisted."""
import math, runpy, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    ns_ = runpy.run_path("/home/claude/aegis/theory/review/gs_alpha_ns_d325.py")
obs = ns_["obs"]; base = obs(1.0)
print(f"alpha 1 (baseline): n_s {base[0]:.4f}, r {base[1]:.4f}")
for s in (1, 2, 0.5):
    d = (33 / 5) / (8 * math.pi ** 2) / s; al = 1 + d * d / 3
    ns, r, xs = obs(al)
    print(f"s {s}: delta {d:.4f}, alpha {al:.5f}: " + ("NO 57-efold solution" if ns is None else f"n_s {ns:.4f} (dn_s {ns - base[0]:+.4f}), r {r:.4f}"))
