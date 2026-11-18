# DEVIATIONS for PREREG_LHC7 (written before the scored run)
1. First runs returned NaN: the root bracket [300 GeV, 0.29√s] left the τ₀ range of the 13 TeV table (σ_scaling raises outside it).
   Fix (code bounds only, no physics change): bracket = τ₀ range of the table, m ∈ [√s·100/13000, √s·2000/13000]. A run with only the
   upper bound fixed gave HL-LHC 0.974/0.801 TeV and HE-LHC 1.684/1.360 TeV; FCC-hh still NaN (lower bound). Scored run = after both fixes.
