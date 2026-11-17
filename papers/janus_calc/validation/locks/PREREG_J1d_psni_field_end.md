# PREREG J1d — PSNI with an explicit field-value end (follows D1022)
Locked 2026-11-17 after a diagnostic trajectory (recorded in the D-note) and before any J1d score.
Diagnostic finding (data, no score): from y₀ = 0.35 the exact background reaches the singular point y → 0 at N ≈ 62.06
with ε_H ≈ 0.074 < 1 — ε_H = 1 is never reached before the singularity, so "N* before ε_H = 1" is undefined for PSNI
(α = 1e-3, f = 5) in an exact treatment; ASPIC's end (ε_1V = 1 at x_end = π/2 − 2e-4) is a slow-roll definition.
Test: give Janus and the exact MS reference the SAME end as ASPIC — the field value y_end = f(π/2 − x_end) with ASPIC's
x_end (= 1.57065364198363, committed raw output) — via an end-at-field event (core.Model option end_y). Pivot N* e-folds
before reaching y_end. Score PSNI at N* = 50, 60 as in J7d (Janus vs ASPIC vs exact MS). No pass/fail; numbers added to
the running total with the stated end definition.
