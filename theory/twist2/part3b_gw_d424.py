"""D424 (locked PREREG_D424_PART3B): second pass Part 3 — primordial GWs boosted by the Twist's kination, with r = 0.0046 (Route A, D419).
Radiation-era plateau Ω_GW h² ≈ (r A_s / 24) Ω_r h² (Ω_r h² = 4.2e-5); modes entering during kination are boosted ∝ f (w = 1) up to the
end-of-inflation mode, by a factor ≈ a_kin_end / a_end = e^{ΔN_kin} (ΔN_kin ≈ 3.5, D367c). Frequencies: f ≈ 2.65e-8 Hz (T/GeV)(g*/106.75)^{1/6}
for the mode entering at T. ΔN_eff(GW) ≈ Ω_GW,peak h² / (5.6e-6) × ln-width (conservative: width 1). AI-assisted."""
import math
r, As, Orh2, dN = 0.0046, 2.1e-9, 4.2e-5, 3.5
plateau = r * As / 24 * Orh2; peak = plateau * math.exp(dN)
f_kin_end = 2.65e-8 * 1.33e13; f_end = f_kin_end * math.exp(dN)
print(f"plateau Ω_GW h² = {plateau:.2e};  kination-boosted peak = {peak:.2e} at f ≈ {f_end:.1e} Hz (boost starts at {f_kin_end:.1e} Hz)")
print(f"ΔN_eff(GW) ≈ {peak/5.6e-6:.1e}  (bound 0.14)")
print("detector bands: LISA ~1e-3 Hz (sens ~1e-12), ET ~10–1e3 Hz (~1e-12), proposed MHz–GHz high-frequency searches (≫1e-10)")
