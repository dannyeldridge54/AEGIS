# Wording standard (8 Nov 2026, at Danny's request: "get everything in technical terms")

Use in every write-up, doc and commit message. Verdict labels from locked rules (BEATS, SUPPORTED, …) are kept exactly
as the rules define them, but each first use carries its operational definition.

| Avoid | Use instead |
|---|---|
| "beats ΛCDM" | "Δχ²_min ≤ −4 relative to ΛCDM on ≥ 2 of 3 SN compilations (SF rule threshold), with k extra parameters; ΔAIC = …" |
| "as good as w0–wa" | "within Δχ² ≤ +2 of w0–wa on ≥ 2 of 3 (COMPETITIVE per the SF rule); equal parameter count (2)" |
| "proves", "confirms", "shows the theory is right" | "is consistent with", "is preferred at …", "passes the pre-registered criterion …" |
| "fixes the S8 problem" | "reduces the DES Y6 S8 penalty from … to … (Gaussian compression, NLA, 0.798 +0.014/−0.015)" |
| "derived" (unqualified) | "derived given [stated inputs/assumptions]"; otherwise "chosen" or "fitted" (equation map) |
| "the field does both jobs" | "a single axion–dilaton with fixed λ reproduces/does not reproduce both the early and late phases (UB-1/UB-2)" |
| "significant" (local) | "local Δχ² = … (k dof, p = …); global significance … after the trials correction (V7)" |
| "no one else has this" | "no published model combining … was found in a search of … (date, scope)" |
| "light angle" | "ultralight axion fraction f = β_eff/√(2/3) with mass m (pheno_axion fluid, n = 1)" |
| "the Spiral" (first use) | "the Spiral Twist: rolling dilaton dark energy (exponential slope κ) with a dilaton-dependent dark-matter mass, β_eff = √(2/3) f" |

Always state: data combination, engine and build, best-of-N restarts, whether the comparison is blind, and every
deviation number.
