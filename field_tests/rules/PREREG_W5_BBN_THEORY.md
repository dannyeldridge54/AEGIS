# PREREG_W5_BBN_THEORY — theory errors on the Hyperion BBN pulls (locked 20 Nov 2026, before computing)
Item C/W5 of tools/weave_control/LOOP_STATE.md; answers referee R2 (BBN pulls used observational σ only).

## Theory σ (sourced, relative, applied to Hyperion's own Y_p and D/H)
- PRIMAT (the table Hyperion uses, so it sets the STATUS):
  · Y_p: 0.00017 absolute (Pitrou et al., arXiv:1801.08023: Y_p = 0.24709 ± 0.00017);
  · D/H: 1.5% (Paris/PRIMAT D/H = (2.439 ± 0.037) × 10⁻⁵, as quoted in arXiv:2011.13874).
- Yeh, Olive & Fields 2021 (arXiv:2011.13874; MC over rates with LUNA d(p,γ)³He), SHOWN as a second convention:
  · Y_p: 0.00018 absolute; D/H: 0.110/2.506 = 4.39% (their σ includes the ω_b error, so it is a conservative upper edge).

## Pull
pull = (model − data) / √(σ_obs² + σ_th²), for every stored measurement (Y_p: LBT2026, Aver2021; D/H: Cooke2018). Observational-only pulls stay visible.

## Status (fixed now)
Use the PRIMAT convention: pass if all |pull| < 2, tension 2–3, fail ≥ 3. The Yeh+ convention and the obs-only pulls are reported beside it, never used to set the status.

## Not done here
No Monte Carlo over individual rates (that needs bbn_net.py; queued separately). No change to ω_b or ΔN_eff to move any pull.
