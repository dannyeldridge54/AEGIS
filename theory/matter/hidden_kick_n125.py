"""D35: Development 34 with the realistic cliff (n = 125, the drop to today's dark energy). Natural hidden-cosine strength
at Re T = 0, suppressed by exp(-A Re T); scan the hidden mass. AI-assisted."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hidden_kick_holo as Hh
ns = Hh.ns; ns["XREL"] = 0.0; ns["N"] = 125.0
if __name__ == "__main__":
    for m in (3e9, 1e10, 3e10):
        o = ns["run"](0.05, m_sigma=m, p0=-13.0, Nafter=9.0)
        print(f"n=125, m_sigma {m:.0e} GeV: N_end {o['N_end']:.1f}; n_B/s {o['nBs']:.2e} (x{o['nBs'] / Hh.C.TARGET:.2g}); "
              f"peak shares angle {o['peak_angle_share']:.1e} hidden {o['peak_hidden_share']:.1e}", flush=True)
