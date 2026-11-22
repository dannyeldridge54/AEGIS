# The Unified Field Bloom (UFB): the UFE derivation toolkit (v1, 22 Nov 2026)
**Names (Danny 00:55):**
- **The Bloom** is the UFE derivation toolkit: tools/bloom + tools/loom core.
- **The Forge** is the compressor: tools/compress, loomz. The Forge is **paused**. Its jobs are frozen (SIGSTOP) and can be resumed later.
- Every lesson the Forge earned is now an engine rule in the Bloom.

## What the Bloom is
- **One target.** ln L_global − ½·k_fit·ln N, a BIC-style penalty. It is computed over every dataset term (`bloom_data.json`).
- **The structure.** Agents S / T / U / Thread / Evidence, each with at most 9 knobs. The Centre balances them (loomcore).
- **Lenses.** Every dataset term (node) is looked at through 7 lenses (below).
- **Run:** `python3 tools/bloom/bloom.py` (add `--json` for machine-readable output).

## Forge lesson → Bloom rule
| Forge lesson (D-note) | Bloom rule | where |
|---|---|---|
| Bypass traces: strong parts wired straight to the output (D2025) | every dataset feeds the target directly; no separate pass/fail bars | lens 1, `target()` |
| Shadow multiplexer: settings run side by side, the lowest cost wins (D2011) | each alternate dataset is scored side by side (e.g. CMB-SPA vs CMB-SPA + DESI) | lens 2 |
| Don't hide a conflict inside one ring (UFE v4 §7) | measure the tension between datasets before combining them | lens 3 |
| Scale ladder: the event state flipped between 200 kB and 3 MB | a value counts only if it is stable over its last two rungs | lens 4 |
| Random controls of the same shape (D2007 Phoenician, D2024 traditions) | a derived value must beat random admissible choices; gives a look-elsewhere p | lens 5, `random_control()` |
| Size of the last correction (new: GAMBIT practice, arXiv 2512.14109) | theory error = the last ladder step, used as a sensitivity lens only | lens 6 |
| Held-out decides | goodness of fit by parametric bootstrap (toys) | lens 7 |
| Negative space: the closing stack (D2012) | the owed list and the strict-evidence count are printed every run | `negative_space()` |
| Hash confirmation; no shared slots (D2016/D2017) | each dataset is owned by exactly one agent | `hygiene()` |
| Admission rule: coarse beats fine (D2007/D2008) | a knob must buy more lnL than ½ ln N, or it is NULL | `verdict()` |
| Planted controls (D2018–D2020) | injection-recovery runs on every invocation | `injection_test()` |
| Compass | direction and headroom of every term | `compass()` |
| Octave → fifth, Centre bandit, ladder to null | Agent / Centre from loomcore | T1 demo |
| Symbol systems are labels unless they beat random (D2024) | esoteric names are labels; never evidence | ESOTERIC_LENS.md |

## First run (D2026)
- **Target.** lnL = −9.43; k_fit = 8; N = 18; lnL − BIC = **−21.0**.
- **α_s is the whole deficit.** z = −4.22, lnL = −8.91. PDG 2025 is unchanged at 0.1180 ± 0.0009 (triangulation source 1 of 3).
- **Ladder lens: α_s is not converged.** The last Δ₃ step (−0.15 → −0.094) is 1.27× the shift still needed.
  - Taking that step as the theory error gives z = −0.77.
  - Read: this is a **gap**, not a pass. The next rung (explicit brane thresholds, T1) decides.
- **T1 demo.** A free Δ₃ knob reaches −0.047 and α_s = 0.1183 (ΔlnL = +8.87). That is labelled **FIT**, never claimed. It shows the engine refuses to count a tuned seam.
- **Other lenses:**
  - n_s shadow: −0.81σ with + DESI, +0.73σ alone; the two datasets are 1.09σ apart.
  - Goodness of fit over the gaussian terms: p = 0.0009, driven by α_s.
  - Injection recovered 0.371 vs 0.37 planted.
  - Hygiene OK.
- **Known limit.** The rank-1 coupling of Δ₃ → m₃/₂ → wino (D1937a) is not in the engine yet. A Δ₃ move must also move the wino term. Next: add the Jacobian from D1937a.
