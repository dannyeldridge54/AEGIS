# Which dark matter feels the dilaton? (V3 check-in, 9 Nov 2026)

Note, not a rule. Settles the open question in the equation map (doc "The Twist equation map", tests table, V3 row)
and the mass-change sign left open at the V2 check-in.

## The two pictures

- **A, "all dark matter" (what the fits run).** Every dark-matter particle has m_c ∝ e^(βφ/M_P), β = 0.042–0.049
  (Spiral), 0.037–0.042 (S8-J), 0.050–0.053 (S8-L). Coupled AxiCLASS: `background.c` l. 448 and l. 3273 (V3 gate).
- **B, "angle share only".** Only the BI angle, a fraction f of the dark matter, couples, at full strength 0.816;
  the rest of the dark matter, like baryons and light, is blind to the dilaton.

## What the action implies

The action in the equation map:
S = ∫ √−g [ R/2 − ½(∂χ)² − ½ F_P² e^(λχ)(∂θ)² − V_early(θ) − V_late(χ) ] + S_baryons,light[g] + S_DM[g, m_c(χ)] + S_ν[g],
with λ = −2√(2/3).

1. The only place χ touches anything dark is the angle's kinetic factor e^(λχ). Write θ_c = F_P e^(λχ/2) θ
   (canonical). Near the bottom of its potential the angle oscillates with mass m_eff = m e^(−λχ/2) = m e^(0.816χ).
   Averaged over oscillations it is pressureless matter with conserved number, so ρ_θ ∝ m_eff n and
   **d ln m_θ/dχ = −λ/2 = √(2/3) = 0.816, for the angle only.** This is derived.
2. The term S_DM[g, m_c(χ)] with β = √(2/3)·f has no separate origin in the action. It is the angle's coupling
   spread over all the dark matter: the background back-reaction on χ is β ρ_DM = 0.816 f ρ_DM = 0.816 ρ_θ, the
   same in both pictures. So **for the expansion history A and B are identical** (that is why the fits can use A),
   but they are not the same physics for forces between clumps.
3. Ordinary (non-angle) dark matter appears in the action with no χ dependence. Unless f = 1, picture **B is what
   the action says.** The map's "dark matter feels the dilaton" row is the background stand-in and should say so.

## Force ratios (scalar exchange, χ light: its mass is ~H0, so no screening inside the Hubble scale)

Extra force between two particles with couplings β₁, β₂ (reduced Planck units): F = G m₁m₂/r² × (1 + 2β₁β₂).

| Pair | Picture A | Picture B |
|---|---|---|
| dark matter – dark matter | 1 + 2β² = 1.0036–1.0047 (Spiral) | bulk–bulk 1; angle–angle 1 + 2(0.816)² = **2.33** ; angle–bulk 1 |
| dark matter – star | 1 | 1 |
| star – star | 1 | 1 |
| Kesden–Kamionkowski β_KK (DM force = (1+β_KK²) G) | √2 β = 0.060–0.069 (Spiral), 0.053–0.075 all fits | see below |

Mean pull on a satellite's dark matter, B, **if the angle clusters like cold dark matter**: a fraction f of the
satellite feels 2(0.816)² × f extra from the host, so the mean extra is 1.333 f². With f = β/0.816 this is
exactly 2β², the same as A. The difference would be inside the satellite: its angle share alone is pulled ~7%
harder (1.333 f with f ≈ 5–6%) and would drift ahead of the rest of the dark matter.

**But the angle does not cluster in galaxies at the fitted mass.** S8-L fits the angle as an ultralight field with
mass 1.3–1.5 × 10⁻²⁵ eV (`field_tests/results/spiral_l_score.json`). Its de Broglie wavelength is ~420–480 kpc
at 200 km/s (Milky Way halo) and ~4 Mpc at 20 km/s (Sagittarius), larger than both objects. So in picture B the
angle is nearly smooth on galaxy scales, the host and satellite hold almost none of it, and **the stream signal is
β_KK ≈ 0** (below 10⁻² by the density contrast; not computed in detail). Only clusters (λ_dB ~ 90 kpc at
1000 km/s) could hold part of it.

## Consequence for the locked V3 rule (stated, nothing changed)

`PREREG_V3_STREAMS.md` (locked 8 Nov) predicts β_KK = 0.053–0.075. That is the picture-A prediction: it tests the
fitted effective model, not the action's own picture. Under B (with the S8-L mass) a future stream exclusion of
β_KK ≥ 0.053 would **fail the locked V3 rule while agreeing with the action**. The locked rule stands and is scored
as written; this note is the record that its prediction is the fits' and not the derived one.

A second inconsistency, stated plainly: S8-L's code puts the coupling on the 94% cold share and leaves the light
share uncoupled (PREREG_SPIRAL_L.md: "an ultralight field, uncoupled"). The action says the reverse: the light
angle is the coupled part. The background is the same (point 2); the growth of the light share is not. A build
with the coupling on the ultralight field is a new engine item, not done.

## The mass-change sign (open since V2): settled for the fitted models

- Code (V2 frozen numbers): cold dark matter per particle is 0.81–0.95% lighter today than at z = 1100; φ moved by
  Δφ = ln(ρa³ ratio)/β = −0.193 / −0.210 / −0.184 (P+ / Dovekie / Union3).
- The matter-era back-reaction (−β ρ_DM in the Klein–Gordon equation) pushes φ down; in this window it wins over the
  exponential's slope. Because the back-reaction is the same in A and B (point 2), the same Δφ applies under B,
  where it means **the angle particles are 14–16% lighter today than at z = 1100** (e^(0.816Δφ)), the bulk dark
  matter unchanged, total dark-matter mass −0.8 to −0.95% as before.
- The 7 Nov audit (F) said "grows". That was `spiral_w.py` at m = 100 H0, where the angle only becomes matter-like at
  z ~ 30, so the back-reaction acts late and the slope wins. It is not the fitted case (S8-L onset a_c ≈ 1.7 × 10⁻⁵,
  before recombination). **For the fitted models: shrinks.** Not checked by a direct solver run at the fitted mass
  (10⁷ oscillations; would need an averaged-fluid solver), and said so.
- Implication noted, not pursued: in Babu–Amendola's language a shrinking mass is their positive-β mode, not the
  phantom-crossing mode the audit matched to.

## Fixed-β value (for the simplification bracket, later)

The action fixes the angle's strength (0.816) but not f, so β = 0.816 f stays free until f is derived. No fixed-β
candidate is proposed. (SIMPLIFY-L already says so.)
