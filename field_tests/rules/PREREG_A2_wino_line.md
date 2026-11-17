# PREREG A2 — wino γγ line at 1 TeV vs H.E.S.S. 2018 (Djl A) — locked 2026-11-17
Sources:
- σv(χ⁰χ⁰ → γγ) = c Σ sΓs* with c = 2 for identical particles and c = 1 otherwise (Hisano+ hep-ph/0610249 Eq. 6/8; 1307.4082 Eq. A8). Only Γ^γγ_{+−,+−} ≠ 0 at tree level, with σ^γγ_{+−}v = πα²/M² (1307.4082 Eq. B5). So σv_γγ = 2|s_{+−}|² πα²/M².
- H.E.S.S. 2018 (arXiv:1805.05741): γγ-only 95% limit ⟨σv⟩ ≈ 4e-28 cm³/s at 1 TeV (Einasto, 7 ROIs). Values at 2 and 3 TeV are not quoted in the text, so 1 TeV only.
- γZ is NOT included: no normalisation sourced. Because H.E.S.S. bounds γγ only, comparing γγ alone is the like-for-like test.
Computation: M = 1000 GeV, v = 1e-3 (halo), on-shell α = 1/128.943 and Beneke inputs. s from sommerfeld_nlo at LO (nlo = False) and at NLO (√2, post hoc).
Reported: σv_γγ, and f_max = √(4e-28/σv_γγ) at H.E.S.S.'s own Einasto normalisation. Compared with SERAPIS-E's wino fraction at 1.0 TeV, f = 0.26 (D1080/D784).
Verdicts:
- PASS if f_max ≥ 0.26 at tree-level Sommerfeld.
- Also reported with the one-loop reduction ×1/3–1/4 (1307.4082 caveat; f_max ×√3–√4).
No halo-profile variations (H.E.S.S.'s own Einasto only).
Script theory/wiring/a2_wino_line.py (written after this lock).
