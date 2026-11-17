# DEVIATIONS C7 (written before any rerun) — 2026-11-17
D1: The McMillan17 potentials in galpy have physical output turned ON. vcirc, evaluatePotentials and jeans.sigmar already return km/s or (km/s)², so the script's extra ×vo (and the ×vo after the √ for v_esc) multiplied by 233.1 a second time. Proof: v_c(r0) printed as 54358.7 = 233.1 × 233.2. Inputs as plain floats are still natural units (r/ro), which is correct. halo.mvir with ro/vo was already in physical M_⊙ (1.315e12 is plausible).
Fix: drop the ×vo factors in C3, C6 and C2. No other change.
