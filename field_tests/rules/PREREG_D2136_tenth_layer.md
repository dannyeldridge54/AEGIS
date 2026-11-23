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

## ADDENDUM (referee R36-1…R36-4), written before any run; no output exists yet
1. **R36-4: baseline H0.** Newest data only: the median of three independent b = 0 Weave fits on DES-Dovekie and Pantheon+:
   - D2134 Dovekie: 67.43
   - D2134 Pantheon+: 67.63
   - D2133 referee Dovekie: 67.42

   That gives **H0_BASE = 67.43** (median). It replaces 67.79, which included the superseded DES-Y5 fit.
2. **R36-1: two dark-radiation readings.**
   - **(FS) free-streaming:** the linear map H0 = H0_BASE + s·ΔN_eff with s = median(5.0, 6.2, 7.0) [E]. The negative-space bound is ΔN_eff < 0.14 (95%, ACT DR6 P-ACT free-streaming, as quoted in 2512.19633, which cites the ACT DR6 extended-models paper).
   - **(FL) fluid/self-interacting:** the PS hidden radiation is self-interacting gauge bosons. Its reading is taken directly from a published fit, not from our linear map: the stepped fluid model WZDR on P-ACT-LBS without SH0ES gives **H0 = 68.75 +0.92/−0.71** (2512.19633).
     - Margin_FL = 2 − (73.04 − 68.75)/hypot(1.04, 0.92), computed in code and reported alongside the FS run.
     - For the fluid case the negative-space shell is the data fit itself, which already includes the CMB penalty.
3. **R36-2: the PS floor is removed from the spine.** It belongs to the type IIA seed model, not to UFE v4, and it is conditional. It is reported only as a side test: does a window 0.11 ≤ ΔN_eff < 0.14 exist?
   - vectors only: 0.11
   - with fermions: 0.50
   - all massless states: 0.76

   **The spine** now carries ΔN_eff against the ACT bound plus the BBN bound. The BBN bound is redundant and is kept for completeness; it is noted as never binding.
4. **R36-3: citations and the expected outcome.**
   - **SH0ES:** 73.04 ± 1.04 (Riess+2022, as quoted in 2512.19633).
   - **CCHP:** 69.96 ± 1.53 (Freedman+2024, stat and sys in quadrature).
   - **Expected outcome (pre-registered):** reaching margin ≥ 0 needs ΔN_eff ≳ 0.5 (FS). Expected verdict: **"does not solve"**.
   - **Referee's knob audit:**
     - u_i lowers H0;
     - b is not adopted and moves H0 by ≲ +0.4;
     - α or m_e at recombination is effectively zero (ζ_α ≈ 4e-10);
     - curvature is 0.

     No Weave-native knob reaches 73 without moving a scored item. The run is the map that shows this.
