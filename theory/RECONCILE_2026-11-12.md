# Reconciling the 12 Nov matter/inflation work with the base theory (12 Nov 2026, 21:10 CT)

Note, not a rule. Danny asked to "check all our history" after the evening's theory work (matter doc Developments
13–24, paper "The Twist: inflation, matter and dark energy from one supergravity field"). AI-assisted (Claude).

| Base theory (repo) | 12 Nov evening work | Verdict |
|---|---|---|
| λ = −2√(2/3) from the Gates–Ketov–Yunes BI superfield, K_ΦΦ̄ = 3/(Φ+Φ̄)² (`DERIVATION_CHAIN.md` §1, `bi_kahler_lambda.py`, audit 7 Nov) | Matter-doc Development 17, "the Twist's field space is no-scale supergravity" | **Not new: a rediscovery of the base theory's foundation.** Credit GKY (arXiv:0906.4978) and the 7 Nov derivation. |
| Constant W gives no angle potential (∂V/∂a = 0); other symmetry-breaking sectors not excluded (§2, §8) | Stabiliser model W = √3 m S F(T), F with plateau, cliff, √(2/3) tail and a non-perturbative e^{−aT} term periodic in the angle (`theory/inflation/sugra_*.py`) | **Progress on §2/§8:** an explicit sector that gives both the dilaton potential and an angle dependence. Not derived from a microscopic theory. |
| Dark energy = V_late(χ), the dilaton (`DM_COUPLING_PICTURE.md` action) | Dark energy = the dilaton's tail of slope √(2/3) | Consistent. |
| β = 0.816 f, f = share of dark matter that is the (ultralight) angle; picture B is what the action says | PURE-TWIST (β = 0) PREFERRED | Consistent: the data prefer f ≈ 0. Order-of-magnitude: the angle's charge left after matter-making, Y = n_θ/s ≈ 6 × 10² at T = 10¹³ GeV (F = 1.559 M_P, r = 0.022), gives Ω_θ ~ 10⁻²² for m = 1.4 × 10⁻²⁵ eV (kinetic misalignment), against Y ~ 10²³ needed for f = 5%. So the chain itself predicts f ≈ 0. Caveat: ignores the dilaton-dependent metric factor between reheating and today. |
| Nieh–Yan wormhole instantons give the cosine shape; at F = 1.559 M_P one instanton has S ≈ 1.2, far too little suppression (`INSTANTON_HEIGHT.md`) | The kick needs δ ≈ 10⁻⁴–10⁻⁵, i.e. S ≈ 9–11 | Same open problem: the kick term is naturally this instanton, with the same height issue. |
| Nieh–Yan period → F = (4/π)√(3/2) M_P = 1.559 M_P (derived) | Kick exponent a left free | New constraint to apply: the kick's period in the angle must equal the Nieh–Yan period, which fixes a. Next calculation. |
| Early boost field and late angle "look like different fields" (`INSTANTON_HEIGHT.md` §5) | Angle makes matter early; dilaton is dark energy late | Consistent with that split. |

Corrections made the same evening: matter doc Development 17 and the paper's Section 2 now credit GKY and the base
derivation.
