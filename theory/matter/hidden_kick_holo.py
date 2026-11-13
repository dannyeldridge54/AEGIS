"""D33: hidden-axion kick with the holomorphy constraint. Any term periodic in the angle (Im T) must carry exp(-A Re T)
(an instanton or a hidden gauge coupling depending on T; minimal charge A = pi/4 from the Nieh-Yan period). D31 held the
hidden cosine's strength fixed; at its release (T ~ 1e13 GeV) Re T ~ 37, so the true factor is ~3e-13 and D31 fails.
Rescue tested here: a heavier hidden field (released earlier, where Re T ~ 1) with strength L4(x) = L4_0 exp(-A x),
L4_0 set so the cosine's energy share at release (H = m_sigma) is Omega_h. AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "hidden_kick_full.py")).read().split('if __name__ == "__main__":')[0]
src = src.replace("L4 * (1 - math.cos(A * y - s / fdec))", "L4x(p) * (1 - math.cos(A * y - s / fdec))")
src = src.replace("vp = (Vinf(p + h, y) - Vinf(p - h, y)) / (2 * h)",
                  "vp = (Vinf(p + h, y) - Vinf(p - h, y)) / (2 * h) + (L4x(p + h) - L4x(p - h)) / (2 * h) * (1 - math.cos(A * y - s / fdec))")
src = src.replace("+ L4 * A * math.sin(A * y - s / fdec)", "+ L4x(p) * A * math.sin(A * y - s / fdec)")
src = src.replace("- L4 / fdec * math.sin(A * y - s / fdec)", "- L4x(p) / fdec * math.sin(A * y - s / fdec)")
src = src.replace("mus = m_sigma / m_inf; L4 = Omega_h * 3 * mus ** 2; s0 = fdec",
                  "mus = m_sigma / m_inf; s0 = fdec\n    L4x = lambda p: Omega_h * 3 * mus ** 2 * math.exp(-A * (math.exp(c * p) - XREL))")
ns = {"__file__": os.path.join(HERE, "hidden_kick_full.py"), "XREL": 1.0}
exec(compile(src, "hidden_kick_holo_inner", "exec"), ns)
C = ns["C"]
if __name__ == "__main__":
    for m_sig, xrel in ((1.3e11, 1.1),):
        ns["XREL"] = xrel
        for Om in (0.01, 0.03, 0.1):
            o = ns["run"](Om, m_sigma=m_sig, Nafter=8.0)
            print(f"m_sigma {m_sig:.1e} GeV (release near Re T {xrel}), Omega_h {Om}: n_B/s {o['nBs']:.2e} (x{o['nBs'] / C.TARGET:.2g}); "
                  f"r at T {{{', '.join(f'{k:.0e}: {v:+.4f}' for k, v in o['r_at'].items())}}}; peak shares angle {o['peak_angle_share']:.1e} hidden {o['peak_hidden_share']:.1e}", flush=True)
