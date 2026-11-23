# PREREG D2136: the 10th layer. Resonance pulsing plus breathing, three shapes (Danny 19:13–19:14 CT, 22 Nov 2026)
Locked before any run.

**Danny's ask:** extend the resonance (tools/loom/resonance.py, 9 layers from the centre outwards) by one more rung. He proposed three shapes:
- **A, the outer data shell:** a 10th ring outside the late universe, carrying the big-questions tests.
- **B, the negative-space shell:** a second ring wrapped around the outer field, built from the things that must NOT be seen.
- **C, the spine:** a line up and down the centre and across. It ties the centre to the outer shell through one shared hub number.

## Physics content (labels: S standard, E estimate, D data)
- **New knob:** ΔN_eff, dark radiation from the hidden sector. Derived value 0 (UFE v4). The PS seed model (D2128/D2128a) gives 0.11 to 0.76 if its massless hidden states thermalise (CONDITIONAL).
- **The Weave's baseline H0** is the median of D2131 W (66.84, 68.39, 67.79) = **67.79** (D).
- **H0 response to ΔN_eff:** H0 = 67.79 + s·ΔN_eff, with three readings s = 5.0, 6.2 and 7.0 km/s/Mpc per unit ΔN_eff (E: the size of the CMB+BAO degeneracy direction in the literature). The **median** is used.

## Margins (log headroom, or 2 − |pull|; a margin > 0 passes)
**Shell A (data, the big questions):**
- H0 vs SH0ES, 73.04 ± 1.04 (D; quoted in 2512.19633): 2 − |H0 − 73.04|/1.04.
- H0 vs CCHP TRGB/JAGB, 69.96 ± 1.53 (D, Freedman 2024; total error, stat and sys in quadrature): reported as a **second reading, not used for the lock**.
- Σm_ν vs DESI DR2 + CMB, < 0.064 eV (D): ln(0.064/0.0587).

**Shell B (negative space, the no-shows):**
- ΔN_eff < 0.14 at 95% (D, ACT DR6 P-ACT free-streaming): ln(0.14/max(ΔN_eff, 1e-6)).
- **No phantom crossing:** the thread has w ≥ −1 by construction. This is a TRUST line with no knob and no margin. DESI's crossing remains a pull the Weave cannot answer.
- **No thread–DM coupling:** b = 0 (D2134 NOT ADOPTED). Fixed, no margin.
- **α-drift null:** a leak of ≤ 1e-9 against 1e-6. Margin ln(1e-6/1e-9), which is a constant.

**Spine C (the hub through the centre):**
- **Chosen hub (stated now): ΔN_eff.** The same ΔN_eff must also pass layer 8 (cosmology / BBN): ΔN_eff < 0.3 from Y_p (D, BBN-only bound, conservative), margin ln(0.3/ΔN_eff).
- **The PS floor:** if the PS hidden sector is the matter sector, ΔN_eff ≥ 0.11, margin ln(ΔN_eff/0.11). This tests whether the centre's matter content and the outer negative space can coexist.

## Procedure
**Base:** the D1972 resonance (9 layers, three sweeps; lock = 3 consecutive passing solver passes), unchanged.

**Variant runs:**
| run | layers |
|---|---|
| V0 | 9 layers |
| VA | 9 + A |
| VB | 9 + A + B |
| VC | 9 + A + B + C |

**Breathing:** each variant runs three breaths.
1. **Inhale:** the new knob is frozen at its derived value of 0.
2. **Exhale:** the new knob is free.
3. Repeat 3 times.

A layer counts only if it locks on the exhales and no previously locked inner layer unlocks. Unlocking an inner layer is "unbalanced": the change goes back.

**Pulse:** inside each exhale, coordinate search maximises the minimum margin, and stops after 7 null pulses.

## Verdicts (fixed now)
- **"Solves the Hubble tension"** only if shell A's SH0ES margin is ≥ 0 with the shells locked.
- **"Eases"** if the pull drops by ≥ 1σ while B stays locked.
- **"Does not solve"** otherwise.
- **The PS-floor test** reports whether a window exists: 0.11 ≤ ΔN_eff < 0.14.

This is a **deterministic consistency map, not evidence** (D1948). No reruns to chase results.
