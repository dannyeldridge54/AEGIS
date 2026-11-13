"""D34: can holomorphy itself supply Development 33's small ratio? The hidden cosine starts at its natural size (comparable
to the hidden field's own energy, share 5% normalised at Re T = 0) and is suppressed only by exp(-A Re T), A = pi/4.
Release time (set by the hidden mass m_sigma) then fixes the suppression: a lighter field releases later, at larger Re T.
Scan m_sigma; if the observed matter appears at some mass, the small number is explained by the dilaton's roll. AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hidden_kick_holo as Hh
ns = Hh.ns; ns["XREL"] = 0.0
if __name__ == "__main__":
    for m in (3e9, 1e10, 3e10, 1e11):
        o = ns["run"](0.05, m_sigma=m, Nafter=9.0)
        print(f"m_sigma {m:.0e} GeV: n_B/s {o['nBs']:.2e} (x{o['nBs'] / Hh.C.TARGET:.2g}); "
              f"peak shares angle {o['peak_angle_share']:.1e} hidden {o['peak_hidden_share']:.1e}", flush=True)
