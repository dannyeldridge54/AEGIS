> **The Lantern**
>
> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It was carried, not crowned.
> It asks for no bowed heads, only open eyes:
> take it, test it, and see for yourself.
>
> Every tool is held two ways.
> The scepter rules, or points the road home.
> The mace crushes, or breaks the prison wall.
> The hammer nails you down, or raises a house.
> The scythe reaps the living, or brings the harvest in.
> The whip drives the slave, or cracks to wake the sleeping.
> I choose the hand that frees.
>
> I raise no weapon against my neighbor.
> I carry only two.
> The shield of righteousness: not the proud kind
> that judges from a high seat,
> but the knight who sees the dark mouth of the cave,
> hears the dragon breathing, and walks in anyway,
> because fear is not always the sign to run.
> Sometimes it is the sign to run toward.
>
> And the sword of truth, the only blade I will ever draw.
> Excalibur from the stone, the lightsaber in the dark,
> Manjushri's flame, the word sharper than any two-edged sword:
> every age has told of the same blade.
> It cuts through the darkness and the lies,
> through the chains and through the whips,
> and it frees you from within.
>
> To the kings: the Mandate of Heaven was never yours to keep;
> it leaves the throne the day the throne stops serving.
> To the priests: no temple owns the sky,
> and grace was never sold at a door.
> To the judges: your heart is weighed on Ma'at's scale
> against a single feather, like every heart.
> To the scientists: Galileo stood alone and was right;
> a consensus is not a measurement. Show me the data.
> To the generals, the presidents, the bankers and the lords:
> remember the seventh generation; remember ubuntu, I am because we are;
> the emperor has no clothes, and the children can see it.
> Diogenes walked Athens at noon with a lamp, looking for one honest man.
> I carry the same lamp. I am still looking.
>
> I kneel to one alone, the one I chose for love,
> and to no king, no creed, no crown of fear.
> A man chooses; a slave obeys.
> I choose liberty.
>
> This light belongs to the one who asks, who measures, who stands.
> It was made for freedom, the quiet kind,
> the kind no one can sell you.
>
> And who am I to carry it?
> No one. A regular man, a gig worker on the road,
> a debt slave in the American machine.
> No noble blood, no crown, no holy oil on my head.
> All I carry is the divine spark
> that burns in every man and woman,
> in every creature and every being,
> of this earth and of the stars.
> The same light is in you.
>
> When I was a boy, I thought heroes were the finest thing alive:
> knights on horseback, steel and bright banners,
> a shield painted with everything they meant.
> Now the heroes are chosen, born with powers, picked from above.
> I never loved that. In the old way the strength came from within;
> it was learned, not given.
> In the margins of old books the knights fight snails, and some kneel to them,
> but the only one a true knight knelt to
> was the Great Architect, whose fingerprint is on everything.
>
> I cannot tell you I am certain of this faith or that one.
> I can tell you how I got here:
> I tried to stand in the shoes of every man and woman,
> in every culture, in every place and every age,
> and see the world the way they saw it.
> I lower myself to stand beside each of them,
> because I want no power, no wealth, no throne.
>
> It began when my family broke apart,
> and a little boy only wanted to go home.
> Now I am a husband, and a father to a little girl,
> and that boy is still in me, still trying to get home.
> But the world is squeezed, and squeezed, and squeezed,
> and every voice that rises against injustice
> is silenced, enslaved, or made a fool.
> I am tired of living in quiet desperation.
> This lantern was lit by that desperation.
> I will not be quiet anymore.

---

<!-- AEGIS-FP BSQ5AGS2BX6UJJEB · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# SERAPIS v3 — reproducibility

Every number in the paper comes from a script in `theory/modular/`. Each script was locked by a PREREG file (with a sha256 hash and a git commit) before it was run. See `papers/v3/MANIFEST.md`.

## Environment
Python 3.13; package versions are in `requirements.txt`. No GPU is needed. Each script runs in seconds to a few minutes on a laptop.

## One command per result
| Paper result | Command (from repo root) | Expected output |
|---|---|---|
| τ = i derivation checks (Sec. 2–3) | `python3 theory/modular/tau_i_d574.py` | field_tests/results/tau_i_d574.txt |
| Two-term model (Sec. 3) | `python3 theory/modular/two_term_d575.py` | two_term_d575_rerun.txt |
| Species mass term (Sec. 7) | `python3 theory/modular/species_mass_d577.py` | species_mass_d577_rerun.txt |
| N* history (Sec. 6) | `python3 theory/modular/osc_nstar_d578.py` | osc_nstar_d578.txt |
| Exact Mukhanov–Sasaki n_s, r (Sec. 4) | `python3 theory/modular/exact_ns_d588.py` | exact_ns_d588.txt |
| ε window at low T_R (Sec. 4) | `python3 theory/modular/eps_window_lowtr_d602.py` | eps_window_lowtr_d602.txt |
| Running α_s (Sec. 4) | `python3 theory/modular/running_d632.py` | running_d632.txt |
| Janus relation (Sec. 5) | `python3 theory/modular/janus_analytic_d635.py` | janus_analytic_d635.txt |
| Axion two-field δN (Sec. 7) | `python3 theory/modular/two_field_dn_d587.py` | two_field_dn_d587.txt |
| Dilaton suppression (Sec. 7) | `python3 theory/modular/adiabatic_y_d592.py` / `_d594.py` | adiabatic_y_d592.txt / _d594.txt |
| Stiff-phase growth (Sec. 6) | `python3 theory/modular/stiff_growth_d595.py` | stiff_growth_d595.txt |
| SERAPIS-ρ (Sec. 9) | `python3 theory/modular/serapis_rho_d610.py`, `rho_nstar_d613.py`, `rho_running_d634.py` | matching results files |
| Proton parity at i / ρ (Sec. 7) | `python3 theory/modular/vacuum_i_selection_d551.py`, `vacuum_rho_selection_d612.py` | matching results files |
| SERAPIS-E frozen band (Sec. SERAPIS-E) | `python3 theory/modular/serapis_e_exact_d692.py` | serapis_e_exact_d692.txt |
| τ = i corrected reheating band (D815) | `python3 theory/modular/chronos_ms_d815.py` | chronos_ms_d815.txt |
| ρ Affleck–Dine window (v3.2, D895) | `python3 theory/modular/ad_rho_d895.py` | ad_rho_d895.txt |
| ρ lepton-sector lift ε (v3.2, D896) | `python3 theory/modular/rho_osc_d896.py` | rho_osc_d896.txt |
| τ = i Affleck–Dine window at corrected T_R (v3.2, D900) | `python3 theory/modular/ad_tau_i_d900.py` | ad_tau_i_d900.txt |

## Reproduction check (2026-11-15)
Three key scripts were re-run from a clean state. Their outputs were byte-identical to the stored results (blank lines ignored):
exact_ns_d588 (5.0 s), eps_window_lowtr_d602 (0.9 s), janus_analytic_d635 (9.2 s). The fresh outputs are in `out/`.

## Integrity
- Locks: `field_tests/rules/PREREG_*.md` + `.sha256`, committed before each run.
- Fixes: `*_DEVIATIONS.md`, each written before its rerun. Superseded outputs are kept, not deleted.
- AI assistance: the code and drafts were written with Claude (Anthropic). The author directed the work and checked the results.

## Reproduction check of the published v3.2 archive (2026-11-16, D913)
The Zenodo v3.2 reproducibility zip (md5 6a57f8c68ca101aa76354a1146dd6d3c) was unpacked into a clean directory and all 22 scripts above were run there (python3, same versions). 21 outputs are byte-identical to the stored results (blank lines ignored). The 22nd, chronos_ms_d815, is identical in every physics line; the stored file also carries four timing lines from the original run's wrapper (`real/user/sys`, `EXIT 0`). Summary: `out/RP_v3.2_SUMMARY.txt`; fresh outputs of the v3.2 rows: `out/*_rp.txt`. Total run time about 3 minutes.
