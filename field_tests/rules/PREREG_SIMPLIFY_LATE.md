# Late-field simplification bracket: can the Spiral's slope κ be fixed at a theory value? (SIMPLIFY-L)

**Status: LOCKED** on Danny's word (8 Nov 2026, "Set those tests up to run after the ones we're currently doing").
Fingerprint and UTC time in `PREREG_SIMPLIFY_LATE.md.sha256`. No fixed-κ fit had been run.

## Question
The Spiral fits find κ = 0.86 / 0.97 / 1.17 (Pantheon+ / DES-Dovekie / Union3), free. Does fixing κ at a value the
theory singles out keep the fit, with one setting fewer?

## Candidates (fixed now, no others)
- **K1: κ = 0.8165** (= √(2/3), the same constant that links β_eff to the angle share, β_eff = 0.816 f).
- **K2: κ = 1** (the plain exponential).
Each runs on Pantheon+, DES-Dovekie and Union3: `ax_spa_spiraltwist_kappa0.8165{,_dovekie,_union3}_nlfix` and
`ax_spa_spiraltwist_kappa1{...}_nlfix`; everything else exactly as the stored Spiral fits (same build, data, priors,
β free, best of the same restarts).

Not in this bracket, said plainly: fixing β (the theory ties β to the angle share f, which is not yet derived; see
the V3 coupling note) and joining the early and late fields (needs the early field as a fluid in the same build plus
its own engine gate; a separate rule).

## Scoring (as PREREG_BRACKET.md)
score = χ² − 2 (one fewer free parameter, AIC credit). Summed over the three SN sets. The free-κ Spiral (stored
`ax_spa_spiraltwist{,_dovekie,_union3}_nlfix`, χ² as stored) gets no credit.
- **WINNER** = the lower summed score of K1, K2, but only if it beats the free-κ sum by at least 2.
- Otherwise **κ STAYS FREE**.
Every score is reported, including the loser; two candidates were tried, and that is stated with any winner.

## Check (reported)
A fixed-κ fit cannot have a lower χ² than the free-κ fit on the same data; if one does by more than 0.05, the free-κ
fit is flagged as not fully converged and that is reported beside the verdict (nothing is re-run to change it).

## When
On the PC after bracket round 3 finishes (it waits for the three round-3 result files and for this lock).
