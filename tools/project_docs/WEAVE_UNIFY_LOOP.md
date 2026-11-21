# The Weave — unification loop and its postulates (from 21 Nov 2026)
Danny 08:23: "don't ask me — start whenever you have a postulation stage; mirror SERAPIS; make just as many postulations; set the loop just like SERAPIS's equation is set up and test every direction until we unify the field."
Companion docs: WEAVE_OBSERVATION_LEDGER.md (what is observed), WEAVE_TEST_PLAN.md (how each is tested), WEAVE_POSTULATES.md (the A–D postulate tables of 19 Nov).

## The loop has the SERAPIS shape (twin ladder + centre balance)
Each tick climbs one rung on BOTH ladders and balances them at the centre, exactly like the SERAPIS equation (left = early/UV, right = late/IR, Ma'at = the 4D centre):
- **LEFT ladder (UV → down): string scale → gauge couplings → flavour → inflation/reheating → genesis.** Rungs: L1 couplings at ρ, L2 twisted thresholds, L3 rung placement of the quarks, L4 reheating on the corrected brane picture, L5 leptogenesis/η_B, L6 Λ and the hierarchy from the throat.
- **RIGHT ladder (IR → up): today's universe → dark sector → nuclei, atoms, chemistry.** Rungs: R1 thread identity (birefringence vs α drift), R2 dark matter (self-interaction, detection, dark photon), R3 neutrinos (0νββ, JUNO, δ_CP), R4 nuclear window (Hoyle, deuteron), R5 atoms/molecules, R6 the late-time tensions (H0, S8).
- **CENTRE (Ma'at):** every postulate from both ladders is pushed through the same filters (α drift ζ ≲ 3.6e-6, moduli/BBN, n_s/r, isocurvature, DM lifetime, ΔN_eff, EDMs, proton decay, fifth forces) and the joint audit (every shared number agrees on both sides). A postulate survives only if BOTH ladders still pass.
- **Directions:** every rung is tested both ways — forward (does the postulate reproduce data?) and in the negative space (what must NOT be seen; nulls are predictions too), and before/after in time where it applies.

## Calculation pipeline (Danny 08:53: "make every tool … integrate into the main toolkits … every toolkit feeds CubeMind … CubeMind prepares and postulates itself, the toolkits run automatically with the derived math, and we check CubeMind against it")
1. Every calculation in the loop gets a tool in tools/weave_cm/weave_tools.py (kit) and, where it belongs, in the main toolkit (Weave Control engine, Janus, Hyperion, CERN+1); registered in CubeMind's aegis_tools/registry.py.
2. The same calculation is appended to CubeMind_janus/weave_data/calc_queue.jsonl (id, task text, tool, args, result key, tolerance). CubeMind's learn loop takes queued items FIRST: it derives the number itself (blind — it does not call the tool), then the toolkit runs automatically on the same inputs, and CubeMind is graded (derivation_checked / derivation_failed, weave_data/derivations.jsonl with the queue id; done ids in calc_done.txt).
3. The loop reports CubeMind's score on the queued items at each check-in.

## Postulation stage (automatic, no approval needed)
At every rung the loop writes a postulate (label **P** principle / **C** conjecture / **E** engineering), the test that can kill it, and then locks and runs that test. Postulates are candidates, never results. Publishing still needs Danny's "Publish".

## Loop-1 postulates (adopted as candidates, 21 Nov)
| # | ladder | postulate | kills it | status |
|---|---|---|---|---|
| U1 | L1/L2 | ~~P-twist (s_a Re M ≈ 1.07)~~ WITHDRAWN (D1757a: wrong by 4π; the twisted part would have to be 27–45× the dilaton's) → **U1′ C-geom:** visible gauge fields on a cycle whose volume gives α⁻¹ ≈ 24–40; C5's cold-dark-side mechanism must be re-derived on that picture | a consistent brane picture where the dilaton-inflaton still heats only our side | open (L4 next: reheating on the new picture) |
| U2 | L3 | **P-rung:** one up-quark rung satisfies both the mixing data and the mass ratios | PREREG_B6_RUNG: if no rung is jointly viable, the placement is in tension | running (B6) |
| U3 | R1 | ~~C-axion-thread~~ DOWNGRADED (D1760): an axion thread breaks the A = 7.30 hub; the thread stays sequestered (β = 0 from it) | — | superseded by U12 |
| U4 | R2 | **P-cold-DM (conditional):** collisionless (σ/m ≤ 1e-4 cm²/g) for α_D ≲ 5e-3; larger α_D not computed (referee D1761) | velocity-dependent SIDM if α_D is large | conditional (D1756, D1761) |
| U5 | R3 | **P-no-0νββ-yet:** m_ββ = 1.59–3.80 meV | a LEGEND-1000/nEXO signal > 7.6 meV | locked (D1755) |
| U6 | R3 | **P-no-light-new:** no 95 GeV scalar, no X17, no light sterile ν, no dark neutron decay | confirmation of any of them | prediction (D1753–D1754) |
| U7 | L1 | **P-flux3:** three generations = magnetised flux M = 4 on T²/Z₂ (Z₂-even triplet) | a fourth chiral generation; level-8 flavour group failing TM1 | open (D1697a) |
| U8 | L6 | **C-throat:** the electroweak hierarchy is a warped throat with K/M ≈ 20 at g_s = 1.155 | no consistent throat in the Weave compactification | estimate (D1757) |
| U9 | R1 | **E-no-walls:** no modular domain walls in our patch (jitter estimate, D1761 item 10) | a wall-shaped PTA spectrum | estimate |
| U10 | R2 | **E-no-EDM:** |d_e| ~ 1e-40 e·cm from heavy soft masses only (leptonic CP phases DO exist, D1761) | any electron EDM above the SM floor | estimate |
| U11 | L1/L4 | **C-magD7:** visible sector on magnetised D7 (f ∝ T + g²S, g = 3 generations), dark on unfluxed D7 (f = T) ⇒ Re T ≈ 16.5–32, T_R = 2.6–4.3e8 GeV (x = 0.19–0.32), the generation flux is the inflaton's only handle on our forces | genesis window (M_N ≥ 3.8–6.3e10 GeV needed), wino window redo, ΔN_eff with a fluxed/unfluxed split | derived (D1758), locks next |
| U12 | R1 | **C-photon-axion:** β = 0.277° from an axion on a lepton/U(1)-only cycle (no gluon coupling), m_a ≈ 1e-33–1e-28 eV ⇒ Re T_ℓ ≈ 20–22 (≈ visible cycle), f ≈ 0.04 M_P, c_γ ≈ 0.26 | scale-dependent β; β_reio/β_rec ≠ 0.997–0.999 (LiteBIRD); any α drift | estimate (D1760) |
| U13 | L6 | **C-smallW0:** |W₀| ≈ 2e-9 – 1e-7 from 𝒱 = 1.4e4–3e5 (inflation tilt) and m₃/₂ = 2.5–7e5 GeV (winos); M_P/m₃/₂ explained by small W₀ + volume; v/m_SUSY stays tuned (~4e6) | no flux vacuum with that volume and g_s giving |W₀| ≲ 1e-7 | estimate (D1764) |
| U14 | R2/L6 | **P-split:** split spectrum — winos 0.67–1.0 TeV, scalars/higgsinos 0.25–0.7 PeV, gluino ≳ 4.8 TeV, tan β ≈ 1–4 (m_h = 125) | any superpartner other than wino/chargino below ~0.2 PeV; m_h with tan β ≫ 4 | estimate (D1763) |
| U22 | CENTRE | **P-fractal (Danny 11:11):** the equation's edge is infinite and self-similar — the SL(2,Z) Farey edge. Every Weave ladder is a PARABOLIC (arithmetic, cusp) orbit ending on an ELLIPTIC knot (ρ or i); no hyperbolic (fixed-ratio geometric) ladder is ever needed | a derived observable that requires a hyperbolic geometric ladder; the next ladder (neutrino scale, D1820) not arithmetic in an integer label | postulate (D1817) |
| U22′ | CENTRE | **Inside/outside map (Danny 11:13):** outside = the cusp only (one infinite knob: the inflation plateau / towers); inside = knots ρ (still point) and i (crossing hub) plus the golden/silver/Markov closed loops. Test D1818: all Markov loops pass through i and avoid ρ; τ_ν, τ_d, τ_u are OFF the loops | a derived ladder that is neither cusp-arithmetic nor a Markov multiplier | structure confirmed; no fit yet (D1818) |
| U23 | R3 | **C-neutrino-rung (post hoc, D1821):** ratio m₂/m₃ natural from magnetised Z₂ overlaps at i (1.3 %); scale = one e^{−π Im τ_ν} rung below gauge strength ⇒ y₃ = 0.029, M_N ≈ 4e11 GeV (inside the leptogenesis window) | a mechanism-free factor; M_N outside 4.5e10–2.5e12 from any future proxy | candidate (post hoc) |
