# V7: global significance of the late-time claims (look-elsewhere)

**Status: LOCKED** on Danny's word (8 Nov 2026, "Get everything going by yourself"), before the computation below was
run. Fingerprint and UTC time in `PREREG_V7_LOOK_ELSEWHERE.md.sha256`.

## Claims evaluated
1. **Spiral** (`ax_spa_spiraltwist_nlfix`) vs ΛCDM (`ax_spa_lcdm_halofit`), k = 2 extra free parameters.
2. **S8-L** (`spiralL`) vs ΛCDM, k = 3 extra free parameters.
Main data: Planck + ACT + SPT + DESI DR2 + Pantheon+ (the files without an SN suffix). The DES-Dovekie and Union3
values are reported beside them, with the same N.

## Counting rule (N = number of hypotheses tried)
Inventory: every `cmb-fit/results/cmp_ax_spa_*.json` and `cmp_spiralL*.json` at the lock time. One hypothesis = one
distinct set of theory settings for the late-time field. Collapsed into one (not counted again):
- the same settings run on another SN set or another dataset variant (`_dovekie`, `_union3`, `_desy5`, `_nobao`,
  `_cmbonly`, `_planckfull*`, `_s8y6`);
- reruns of the same settings (`_nlfix` code fix, `_r4`, `_more`, `_b4`, `.stalled*`).
Not counted (references): `ax_spa_lcdm*`, `ax_spa_w0wa*`. The early-field runs (`ax_spa_edelock*`) are counted, since
they were tried on the same data.

## Statistic
- Local: p_loc = P(χ²_k ≥ −Δχ²) (Wilks), converted to a two-sided Gaussian σ.
- Global: p_glob = 1 − (1 − p_loc)^N (Šidák). This is an **upper bound** on the correction because the variants are
  correlated; it is reported as "global (conservative)".
- Both are always quoted together; the local number is never quoted alone afterwards.

## Readings
Per claim: global σ ≥ 3 **SIGNIFICANT AFTER LOOK-ELSEWHERE**; 2 ≤ σ < 3 **SUGGESTIVE**; < 2 **NOT SIGNIFICANT AFTER
LOOK-ELSEWHERE**. Wilks caveat (boundaries, parameters undefined under ΛCDM) is stated with the result.
