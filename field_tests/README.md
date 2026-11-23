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

---

> **Status 7 Nov:** TF-P, SF and TF are **complete** (run on the PC 2–3 Nov; scores in `../CURRENT_MODEL.md`). Running now: SF2 and FP. FP-L was withdrawn before running (`rules/WITHDRAWN_FP_LOCK.md`).

# Field tests: everything left to complete the field

Set up 7 Nov 2026 (AI-assisted). Every test here has its pass/fail rule **locked before its data**; this folder only
runs and scores them. Nothing in it changes a rule, a prior or a run setting.

| Test | Question | Runs | Where |
|---|---|---|---|
| **TF-P** | Does the derived Nieh–Yan F = 1.559 M_Pl fit? | 3 (Union3 blind) | PC, AxiCLASS |
| **SF** | Does the effective Spiral Twist beat ΛCDM or match w0–wa? (gate passed: 0.08 ≤ 1.0) | 3 | PC, AxiCLASS |
| **TF** | The two heuristic F values, √(3/2) and √6 | 6 | PC, AxiCLASS |
| **FP** | Fingerprint (Holst) vs plain cosine (Nieh–Yan): tests the coupling choice | 2 + build + regression gate | PC, AxiCLASS (Fingerprint build) |
| **S8WL** | Full weak-lensing likelihoods (DES Y3, KiDS-Legacy) instead of the S8 penalty | per survey | PC, CosmoSIS; **draft rule, lock first** |
| **N2** | Potential power: n = 3 vs 2 vs 4 (`edelockP_n2_deep`) | 1 | cloud, CAMB (Kronos) |
| **BR** | Knockout bracket, stage 1: 6 variants (then stages 2–3 as the rule says) | 6+ | cloud, CAMB (Kronos) |

`TESTS.json` lists every run name and rule file. `STATUS.md` (written by `score.py`) shows where each stands.

## On the PC

- **Start now and schedule nightly:** double-click `SCHEDULE_FIELD_TESTS.bat`. It builds and checks the Fingerprint code, then starts the 14 AxiCLASS runs (12 + 2 Fingerprint; about
  2–3 hours on 16 cores, 7 lanes) and adds a nightly 01:13 resume. Finished runs are skipped, so re-runs are safe.
- **Just run once:** `RUN_FIELD_TESTS.bat` (add `--push` to publish results to the `field-results` branch).
- **Order:** Union3 first (the blind sample), then DES Y5 and Pantheon+; TF-P before TF.
- **Scoring:** `python field_tests/score.py` at any time. It calls the locked scorers in `scorers/` (copies of the
  release scorers, changed only to read `$TWIST_RESULTS`; original hashes in `scorers/ORIGINAL_SHA256.txt`).

## FP: rebuilt 7 Nov

**Now runnable.** `torsion_shape/patch_sinh.py`, `build_sinh.sh`, `regress_sinh.py` (the rule's every-digit check, a gate) and
`fp_fit.py` (fits `fp_cosine` and `fp_sinh` identically; `fp_fit.py score` applies the rule). `run_pc.sh` builds and checks it
automatically before the lanes start. Deviations: `torsion_shape/FP_DEVIATIONS.md` (the rule's reference number came from a
withdrawn, unconverged run, so the plain cosine is refitted on the same engine).

Original note:

The `axion_sinh_x0` AxiCLASS option behind the Fingerprint (`PREREGISTRATION_SINH.md`) was not in any repository (rebuilt 7 Nov, see above). To
run FP: re-add the option to the potential (V, dV, ddV) using g(d) = s[sinh((d+φ₀)/s) − sinh(φ₀/s)]/cosh(φ₀/s),
s = √(3/2), x₀ = arsinh(1/γ₀) = 2.1445 fixed; confirm that with the option off it reproduces the current build to every
printed digit (the rule's own regression check); then fit Planck 2018 + DESI DR2 + Pantheon+ and compare with the
plain-cosine reference χ²_eff 2427.80 as the rule states. Log the rebuild as a deviation (code re-implemented, rule
unchanged).

## In the cloud (Kronos)

N2 and the bracket use the CAMB pipeline and run in the cloud chat; their results land in
`aegis-Kronos-syndyr/data/fits/refit5/` and are scored by `research/refit/tournament.py` and `bracket.py`.

## Safeguards (added 7 Nov, after the 6 Nov stall)

What went wrong: GitHub refused every cloud job (billing) with no alert; a queue waited for files that never came; the
F derivation and three locked rules lived only in the release repository; TF-P, SF and TF had run on the PC (2–3 Nov) but their results never left it. Now:

1. **No paid cloud queue.** All Kronos GitHub Actions workflows are disabled. Fits run on the PC (`run_pc.sh`) or in a
   cloud chat, never on Actions minutes. Re-enable a workflow only after checking billing.
2. **No waiting on other jobs.** `run_pc.sh` starts what is missing and skips what is done; a nightly resume picks up
   anything that stopped.
3. **Rules live here.** `rules/` holds byte-identical copies of the locked TF, TF-P and SF rules and the Nieh–Yan
   derivation; `ufe-v2/tests/test_field_rules_locked.py` fails if any copy stops matching its lock hash.
4. **Nothing stays only on the PC.** `sync_check.sh` runs at the start and end of every PC run and writes `SYNC.md`:
   uncommitted files and unpushed commits in every project repo it finds, flagged ⚠. It is pushed with the results.
5. **Someone checks every morning.** The daily scheduled score (08:58 CT) reports verdicts, ⚠ sync flags, GitHub jobs
   that failed to start, and results that have not moved for two days.
