# SERAPIS-E v2 update — referee response

## 18 Nov pass

Referee and editor pass on `Eldridge_SERAPIS-E_v2_update_2026.tex`. No new results: every number was checked against D1262, D1265–D1265b, D1268, D1270, D1272–D1275b, D1280, D1283, D1292, and `field_tests/results/` (`audit_2026-11-18.txt`, `emulator_exact_crosscheck_2026-11-18.txt`, `serapis_point_vs_data_2026-11-18.txt`, `serapis_i_saddle_2026-11-18.txt`, `critical_points_2026-11-18.txt`). External data were checked against the primary papers.

**Verdict:** minor revision. The core numbers are correct. One σ figure was wrong. Two caveats that the notes require were missing, and some wording overclaimed.

### Numbers verified (unchanged)
- Point n_s 0.97439, r 4.82e-4, α_s −9.98e-4, N* 50.18 at T_R 7.39e8, C 1.249e-6 (D1262; audit rerun 0.974384).
- N* 50.07–51.22, T_R 5.5e8–1.65e10, m_φ 3.17e13, audited n_s 0.97166–0.97596 (D1262, P5).
- Emulator |Δn_s| ≤ 3.2e-5 (D1272). dn_s/dlnC 0.0133, band 0.0101–0.0141 (D1265a/b). Meter 0.0016/0.01334 = ±12%.
- P = 15·4/(64π⁶C) = 780.7 at C = 1.249e-6. Hessians [+3.562, +3.562] and [−1.279, +5.779] (D1280). α_s relation 3.4% (D1273).
- Frozen band, caps and dates (PREREG_D693, D676).

### Changes
1. **CMB σ offsets (headline number corrected).** The high edge of the band was "+2.2σ" above CMB-SPA. That figure came from the unsourced pair 0.9684±0.0030. With published values only it is **+1.94 to +2.13σ**, so the abstract now says "+0.85 to +2.1σ". The body now lists each published value with its source: SPT-3G D1 0.9679±0.0033; Balkenhol+ 2512.10613 0.9682±0.0032 and +DESI 0.9728±0.0029; McDonough–Ferreira 2512.05108 0.9693±0.0029 and +DESI 0.9737±0.0025. The benchmark is +1.75 to +1.97σ, and the band is −0.78 to +0.74σ against CMB-SPA+DESI.
2. Added P-ACT (ACT DR6 + Planck, 0.9709±0.0038): the band sits at +0.2 to +1.1σ.
3. Added an explicit statement that P5's comparison pair could not be traced to a publication and is replaced.
4. r bound: added BK18 (2110.00483) and r<0.034 (2512.10613). "75×" became "70–75×".
5. **Leptogenesis caveat (D1270, required by that note for any v2).** The abstract no longer says "leptogenesis-fixed T_R". It now says M_H = 1e12 GeV is a *choice*. A new paragraph adds that the benchmark instanton M_H = 9.8e10 gives T_R ≈ 7e7, no thermal leptogenesis, and n_s 0.97362 (still inside the band). "Heavy-neutrino mass" was added to the open items.
6. **Frozen r/α_s edges.** The table and text now give the recomputed band's r (4.52–4.89)e-4 and α_s −(9.38–10.1)e-4 at T_R 7.39e8. Its low-C edge falls just outside the frozen r floor (4.55e-4) and α_s edge (−9.4e-4), and this is recorded as a post-hoc tension. The audited r range and its corner outside the frozen band (as stated in P5) are now also given.
7. "All are exact MS results computed under a pre-registered lock" was an overclaim. It now says the spectra are exact MS, the audit was locked, and the 18 Nov checks are unlocked verifications.
8. Meter: added "at fixed T_R and N_eff". Added that Bahr-Kalus–Parkinson–Easther (2212.04115) label σ(n_s)=0.0016 as a 95% interval, so ±12% is the conservative reading (±6% otherwise). Reason for P5's ±14% given precisely (slope taken near C≈1.12e-6). "560–975 merged over N_eff = 3, 4" added (D1275b). The "≲5%" sentence now gives the number: σ_th ≲ 6.7e-4.
9. **Hexagonal vacuum.** "Its only vacuum is ρ" became "global minimum is ρ". Uniqueness of the global minimum is cited as a theorem (Rankin; Cassels; Ennola; Diananda; Montgomery for theta). "A torus started at any shape flows to it" was narrowed to the computed statement: generic starts, Gaussian energy, with no other critical points at three scales. The text notes that E(τ,2) itself was not scanned for further critical points. The SU(3)₁ point is now credited to Angelinos–Chakraborty–Dymarsky (2206.14825), with the size mismatch stated (D1283).
10. Abstract: "the frozen band n_s = 0.97176–0.97493" became "over the frozen range C = (1.0–1.3)e-6 the model gives …", because the frozen *n_s* band is 0.970–0.975. "The fast emulator" became "A fast emulator" (it is not P5's fast code).
11. Citations: SPT ref split into three attributed refs; added ACT DR6 (2503.14452), BK18, SO+SPHEREx forecast, Rankin/Cassels/Ennola/Diananda/Montgomery, and ACD. Archive URL wrapped in `\url` (it was an overfull box).

### Headline-claim changes
- σ from CMB-SPA at the band's top edge: +2.2σ → +2.1σ (+1.94 to +2.13σ).
- The point is no longer described as "leptogenesis-fixed"; M_H is a choice.
- "Only vacuum" → "global minimum".

Wino-window wording (open items) was checked and left unchanged.
