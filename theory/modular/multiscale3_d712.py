"""D712 (locked PREREG_D712). AI-assisted."""
import math
lo,hi=0.66,2.9; m_lo,m_hi=2.5e5,1.1e6; g_lo,g_hi=4.7,21.0
k=m_hi/hi; kg=g_hi/hi
print(f"T14 wino window {lo}-{hi} TeV; Fermi excludes 1.85-2.86 TeV (any fraction) and thermal 100% DM")
new_hi=1.85
print(f"  surviving wino window {lo}-{new_hi} TeV -> m3/2 {lo*k:.2e}-{new_hi*k:.2e} GeV (ratio check {m_lo/lo:.3e} vs {k:.3e}), gluino {lo*kg:.1f}-{new_hi*kg:.1f} TeV")
print(f"  fraction of window (log) removed: {math.log(hi/new_hi)/math.log(hi/lo):.2f}")
print("  wino below 2.8 TeV is thermally underabundant => SERAPIS needs a non-wino DM component")
print(f"T15 colliders: wino lower end {lo*1000:.0f} GeV vs CMS 650 / ATLAS 660 GeV: at the edge (window lower end set by ATLAS itself); gluino {lo*kg:.1f} TeV vs ~2.3 TeV: factor {lo*kg/2.3:.1f} margin")
for d in (4.62,9.41): print(f"T16 ordering: NO input favoured, Δχ²(IO-NO)={d} -> ~{math.sqrt(d):.1f}σ")
print(f"T17 birefringence: predicted 0 from inflaton sector vs 0.277±0.057 deg: {0.277/0.057:.1f}σ -> needs another light axion")
print("T18 isocurvature ~1e-8 of zeta vs Planck beta_iso < ~few e-2: consistent")
