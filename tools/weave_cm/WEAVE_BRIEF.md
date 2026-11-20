# CubeMind brief — how the Weave is derived, and how to keep going (20 Nov 2026)

CubeMind directs this track. It proposes, checks with its own tools, grades itself, and hands survivors to Claude + an independent referee. It never publishes, never edits theory files, never changes systems.

## 1. What has been done (the record)
- Everything is in `DERIVATION_LOG.md` (merged: the ladder log plus every D-note from the main log, house format `## D####: …`), latest D1748.
- Published (Zenodo): SERAPIS v3.4 status 10.5281/zenodo.24396665; The Quark Thread 24399408; Weave Control + Evidence Atlas 24399447; 23 earlier records updated with status addenda (list in PAPERS_2026-11-20.md); Reverse Thread status 2: 24399734.
- The model in one page: `WEAVE_FACTS.txt` (read by the proposer every cycle).

## 2. The method (non-negotiable)
1. **Postulate** one thing that goes beyond the data, with a number that could come out false.
2. **Lock** before computing: the rule, the inputs, the pass/fail threshold (Claude writes `PREREG_*.md` + `.sha256` in the repo for anything that becomes a D-note).
3. **Compute** with a validated tool (`TOOL: weave_* {json}`), never by guessing a number.
4. **Grade**: own self-check (numeric judge), then the QA eval, then Claude + referee. A FALSE self-check auto-rejects.
5. **Label** every number: P prediction · F fitted · A assumed/hosted · S standard physics · E estimate. Post-hoc choices are never evidence.
6. **Record**: a survivor becomes a D-note; a mistake becomes a correction note (`CORRECTION to D####`), never a silent edit.

## 3. Where to push next (today's directions)
- **Quarks:** the down sector wants a bigger slip than rung 1 (m_s/m_b comes out low in both models). Postulate what could supply it (another minimum family, a weight change) and predict its rung/CKM numbers with `weave_ckm` at new O(1) couplings.
- **Empty rungs 11+:** hidden families. Postulate a dark-sector family on a named rung (names: rung 10 Themis … 25 Morpheus, WEAVE_RUNG_NAMES.md) and predict its mass ratios from `weave_rung`.
- **Proton:** propagate a quark-rung change into m_p via `weave_proton` (sigma terms; most of m_p is QCD binding — not predicted by the Weave).
- **Molecules:** propagate any change of m_e, alpha or m_p into atomic/molecular scales with `weave_atomic` (Rydberg, Bohr radius, vibration ∝ μ^−1/2). These are standard physics (S) — the Weave content is only in what moves the inputs.
- **Leptons:** Koide boundary — how far a slip can go (`weave_koide_slip`).
- **Thread identity:** a sequestered or axion-like thread (open requirement, D1748) — propose a test, SEARCH: for literature where no tool exists.

## 4. Tools (registry names, all fast, CPU)
weave_rung {"m": 8} · weave_rung_of {"masses": [m1,m2,m3]} · weave_koide {"masses": [...]} · weave_koide_slip {"eps": 1e-4} · weave_tauq {"mass_GeV": 1e11, "phi0": 1} · weave_ckm {"model": "w864", "rung_d": 1, "rung_u": 9, "down": {"r1":..,"r2":..,"g_abs":..,"g_arg":..,"f_abs":..,"f_arg":..}, "up": {...}} · weave_proton {"dmhat_over_mhat": 0.01, "dms_over_ms": 0} · weave_atomic {"m_e_MeV": 0.511, "alpha": 0.0072973, "m_p_MeV": 938.272}
