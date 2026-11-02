# AxiCLASS: an n = 1 axion field breaks δ_m and halofit/HMcode, even when it is frozen

**Found by:** a null test (2026-11-01). **Status:** fixed in a separate build; validated; not yet reported upstream.

## The test anyone can run (about 10 s, needs only `classy`)

A frozen n = 1 field (F = 100 M_Pl, m = 0.015 H₀) never moves, so it **is** a cosmological constant. Its matter
power must equal ΛCDM's.

```
python bug_reproducer.py <AxiCLASS>/python/build
```

| | ΛCDM | Frozen field, installed AxiCLASS | Frozen field, fixed build |
|---|---|---|---|
| σ8 | 0.8084 | **0.2484** (ratio 0.31) | 0.8084 (ratio 1.00000) |
| P_lin(k = 0.1 h/Mpc) | 17193 | **1623** (ratio 0.094) | 17193 (ratio 1.00001) |
| P_nl(k = 1 h/Mpc), halofit | 1263 | **0.80** (ratio 0.0006) | 1257 (ratio 0.995) |

## The two causes

1. **input.c:** for `n_axion = 1` the code forces `include_scf_in_delta_m`. That puts the field, which behaves like
   dark energy, into the matter perturbation δ_m. It dilutes δ_m, collapsing σ8 and P(k).
2. **halofit / HMcode:** they take Ω_m from a total that counts the field's ρ − 3p as matter, which biases the
   non-linear correction for any scalar-field dark energy. CLASS shares this pattern.

**Patch:** `0001-nl-scf-fix.patch`. It changes only these two places; build scripts are `build_nlfix.sh` and
`build_coupled_nlfix.sh`.

## Validation

- **Full likelihood** (Planck + ACT DR6 + SPT-3G D1 + DESI DR2 + Pantheon+): frozen field minus true Λ goes from
  χ² +1.35 (installed) to **+0.13** (fixed). The tolerance pre-registered before the fix was 0.15.
- **Remaining:** a 0.5% non-linear residual at k = 1 h/Mpc on the fixed build. Its cause is not isolated (possibly
  halofit's dark-energy w(z) handling); it is reported, not hidden.
- **Unaffected:** early dark energy with n ≥ 2 (the field dilutes away before δ_m matters).
- **Impact:** every published or ongoing AxiCLASS analysis of axion-like (n = 1) dark energy that uses AxiCLASS's
  σ8/S8 or non-linear spectra.
