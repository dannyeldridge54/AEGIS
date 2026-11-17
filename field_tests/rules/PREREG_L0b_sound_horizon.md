# PREREG L0b — Janus-LT sound horizon at the drag epoch vs CAMB (massless ν first; massive ν = L0c)

Locked 2026-11-17 before any L0b number.

## Method
- r_d = ∫_{z_d}^∞ c_s(z)/H(z) dz with c_s = c/√(3(1+R)), R = 3ρ_b/(4ρ_γ) = (3ω_b/(4ω_γ))/(1+z), H from
  tools/janus_lt/background.py (validated D997; radiation incl. N_eff = 3.044 massless).
- Route 1 (fully Janus): z_d from Eisenstein & Hu 1998 Eq. 4 (fetched, astro-ph/9709112 via ar5iv):
  z_d = 1291 ω_m^0.251/[1 + 0.659 ω_m^0.828]·[1 + b1 ω_b^b2], b1 = 0.313 ω_m^−0.419[1 + 0.607 ω_m^0.674], b2 = 0.238 ω_m^0.223.
- Route 2 (integral check): same integral with CAMB's own zdrag → isolates our integral from the z_d model.
- CAMB 2.0.5 derived params rdrag, zdrag; same 50 random flat cosmologies as L0a (seeded identically), massless ν
  (mnu = 0, num_massive_neutrinos = 0).
## Tests
T1 Route 2: |r_d/rdrag − 1| ≤ 1e-3 on every cosmology (integral + background correctness).
T2 Route 1: |z_d − zdrag|/zdrag and |r_d/rdrag − 1| reported; pass if r_d median ≤ 1 % and max ≤ 2 % (EH98 is a
   1998 fit; recorded as its accuracy, not ours).
Verdict: L0b VALIDATED iff T1 passes; T2 recorded with its own PASS/FAIL.
