# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 094993a24f2ddf26
"""Seed the AEGIS Method claim store with everything tested up to 26 October 2026 (run from ufe-v2/).
Every number here was recomputed by the guardrails or the research scripts; this file only files them by tier."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aegis import method as M

S = {"claims": {}, "threads": []}
CMB = "Planck 2018 + DESI DR2 + Pantheon+ (no SH0ES)"
ev = lambda *a, **k: M.add_claim(S, *a, tier="evidence", **k)
hy = lambda *a, **k: M.add_claim(S, *a, tier="hypothesis", **k)

# ---- evidence: tested against data with a locked rule ----
ev("locked_twist", statement="The Locked Twist: the field wakes at matter-radiation equality and beats the standard model on the fair score",
   status="untestable", mechanism="early energy shrinks the sound ruler; switch-on fixed by the measured amounts of light and matter",
   data=CMB, prereg="cmb-fit/PREREGISTRATION_ZEQ.md",
   result="Split verdict on the rule (Δχ² < −4): χ²_eff −4.15 (ΔAIC −0.15, pass), likelihood-only χ² −3.96 (ΔAIC +0.04, fail); CAMB best of 8 vs best-of-8 ΛCDM",
   source="cmb-fit/results: cmp_edelock8.json vs cmp_lcdm8.json",
   note=("Sits exactly on the line; the gap is smaller than the optimizer's restart noise (0.2–0.4), so these data cannot decide. "
         "The earlier pass (Δχ² −6.5, ΔAIC −2.5) came from one unconverged AxiCLASS evaluation and is superseded. "
         "Locking costs only 0.03 in χ² against the free fit (z_c 3,788 free vs 3,495 locked), so z_c is weakly constrained and the lock is a weak test. "
         "Not blind. Decider: same rule on Planck PR4 + ACT DR6."))
ev("pure_torsion_width", statement="The field's width equals the pure-torsion value F = 1.2247 M_Pl",
   status="failed", mechanism="period set by the Immirzi field normalisation √(3/2)", data=CMB,
   prereg="cmb-fit/PREREGISTRATION_ZEQ.md", result="Δχ² = +13.8 (worse than the standard model)", source="cmb-fit results: ede_noshoes_F1.2247_zeq")
ev("whole_number_width", statement="The width is the torsion value divided by a whole number (instanton charge)",
   status="untestable", mechanism="torsional instantons giving cos(Nθ)", data=CMB, prereg="cmb-fit/PREREGISTRATION_N.md",
   result="best N ≈ 8.9; 7.7 to 10.1 fit within Δχ² = 1 (rule needed ±0.5); controls 8.5 and 9.5 only 0.15 and 0.5 worse than N = 9 (rule needed 1)", source="cmb-fit results: ede_noshoes_F*_zeq",
   note="1.2247 ÷ F = 8.97 was seen before the rule was written.")
ev("dodecahedral_space", statement="Space is a Poincaré dodecahedral space (needs curvature Ω_k ≈ −0.013)",
   status="failed", mechanism="closed curved space with opposite faces joined", data=CMB, prereg="cmb-fit/PREREGISTRATION_OMK.md",
   result="Δχ² = +163 against flat space (rule: excluded above 9)", source="cmb-fit results: lcdm_noshoes_omk-0.013")
ev("curved_space", statement="Space is measurably curved", status="failed", mechanism="spatial curvature Ω_k in the expansion history",
   data=CMB, prereg="cmb-fit/PREREGISTRATION_OMK.md", result="Ω_k = 0.0002 with curvature free; Δχ² = −0.9 for one extra setting (rule needed 9): flat",
   source="cmb-fit results: lcdm_noshoes_omkfree, ede_noshoes_zeq_omkfree")
ev("exoplanet_locks", statement="Planet pairs sit just wide of simple rhythms (2:1, 3:2, 4:3, 5:4) more often than chance",
   status="passed", mechanism="convergent migration while planets were still in their birth disc",
   data="NASA Exoplanet Archive: 1,153 adjacent pairs in 1,067 systems", prereg="research/exoplanet_locks/PREREG_EXO.md",
   result="lock excess E = 2.11, p < 0.0001", source="research/exoplanet_locks",
   note=("A known effect (Lithwick & Wu 2012; Fabrycky et al. 2014): this confirms the method and standard disc-migration "
         "physics. It is consistent with the Sigil Model but not unique support for it."))
ev("tidal_locks", statement="Locks are stronger where tides are strongest (inner period under 10 days)",
   status="failed", mechanism="tidal dissipation", data="NASA Exoplanet Archive", prereg="research/exoplanet_locks/PREREG_EXO.md",
   result="compact E = 1.90 vs wide E = 2.42 (the wrong way)", source="research/exoplanet_locks")
ev("impact_rhythm", statement="Large impact craters repeat on a ~30-million-year rhythm",
   status="failed", mechanism="the Sun's passages through the galactic disc stirring comets", data="45 dated craters ≥ 5 km, 2–260 Myr",
   prereg="research/impacts/PREREG_IMPACTS.md", result="best 27.7 Myr, p = 0.33 (chance does as well 1 time in 3)", source="research/impacts")

# ---- hypotheses: ideas, lenses and computed consequences, not yet decided ----
hy("twist_free", statement="The Twist with all three settings free", status="open", data=CMB,
   result="CAMB best of 8: Δχ² = −3.99 (χ²_eff −4.13), ΔAIC = +2.0: a tie at best (AxiCLASS earlier: −6.5)",
   source="cmb-fit/results: cmp_ede8.json vs cmp_lcdm8.json")
hy("pr4_improvement", statement="The Twist improves the fit to Planck PR4", status="withdrawn", data="Planck PR4 CamSpec",
   result="the claimed −3.4 came from foreground priors; the data's own Δχ² is +0.1", note="Caught by an outside reviewer (Copilot).")
hy("fingerprint", statement="The potential repeats in 1/γ (the lopsided Fingerprint)", status="open",
   prereg="cmb-fit/axiclass/torsion_shape/PREREGISTRATION_SINH.md", note="Rule written; fit not yet run.")
hy("cosmic_bell", statement="The Twist keeps the seven acoustic peaks in place and shrinks the sound ruler 2.9%", status="open",
   result="peaks at ℓ = 220, 536, 813, 1127, 1421, 1727, 2011 in both; ruler 144.9 → 140.7 Mpc", source="cmb-fit/acoustic/notes.py",
   note="A computed consequence, not a test against the standard model.")
hy("stacked_spot", statement="Stacking hot spots can tell the Twist from the standard model", status="untestable",
   result="patterns differ by 0.6%; ring switches at 0.30°, 0.84°, 2.17° in both", source="cmb-fit/acoustic/stack_predict.py")
hy("metatron_ratios", statement="Our fitted numbers match Metatron's Cube ratios more than chance", status="failed",
   result="2 of 5 matched; chance alone gives 2.7", source="cmb-fit/metatron/metatron_test.py", note="Rule written in the script header before running.")
hy("solar_cycle_planets", statement="Venus, Earth and Jupiter's tides pace the 11-year sunspot cycle", status="open",
   result="mean minima 11.070 yr = V-E-J 11.07 yr, but 281 planet periods fall in 9–13 yr", source="research/planets_sun")
hy("mixmaster_trigger", statement="Early-universe axis flips (the Mixmaster) set when the field wakes", status="open", note="A lens.")
hy("spin_trigger", statement="The field couples to the spin of matter and stirs when matter takes over", status="open",
   note="Open problem 2; would explain the lock.")

# ---- threads ----
for a, b, k, part in [("locked_twist", "twist_free", "solid", "lock"), ("locked_twist", "cosmic_bell", "solid", "wave"),
                      ("cosmic_bell", "stacked_spot", "solid", "wave"), ("pure_torsion_width", "locked_twist", "solid", "layers"),
                      ("whole_number_width", "locked_twist", "solid", "layers"), ("tidal_locks", "exoplanet_locks", "solid", "tide"),
                      ("exoplanet_locks", "locked_twist", "dashed", "lock"), ("mixmaster_trigger", "locked_twist", "dashed", "lens"),
                      ("spin_trigger", "locked_twist", "dashed", "lens"), ("metatron_ratios", "dodecahedral_space", "dashed", "lens")]:
    M.link(S, a, b, k, part)

# the wall must hold: these must be refused
for bad in [lambda: M.link(S, "metatron_ratios", "locked_twist", "supports"),
            lambda: M.add_claim(S, "x", "evidence", "a claim with no rule", status="passed")]:
    try:
        bad(); raise SystemExit("WALL FAILED: a forbidden write was accepted")
    except M.WallError:
        pass

M.save(S)
print(M.check(S)["detail"])
