# SERAPIS v3.2 draft: readiness check (16 Nov 2026, 13:00 CT; D907)
No upload or Zenodo action taken. v3.1 (10.5281/zenodo.24281771) is unchanged.

## Build
- Clean rebuild (fresh build dir; pdflatex, bibtex, pdflatex ×2): **18 pages**, 0 undefined references or citations, 0 overfull boxes, 30 underfull (cosmetic line spacing in two-column text).
- bibtex: 0 errors; 2 warnings (missing optional fields: `number` in arXiv_2102_07488, `journal` handled by @misc for arXiv_2606_17994).

## Cross-references (scripted)
- D-numbers cited in the draft: 204. All exist in the D-notes. 195 have their own heading; 9 are inline corrections or frozen values inside a neighbouring note (D585a, D633, D645a, D646a, D667, D675, D677, D679, D681), each also tied to its PREREG file.
- \cite keys: 68, all present in refs.bib.

## Locks
- All 18 deep-project locks of 16 Nov (D829–D900, plus DECISION_RULE_D841) have sha256 files that verify, and every result file was first committed after its lock.
- MANIFEST.md was missing the 13 locks after D841 (D845–D900). **Fixed (mechanical):** an afternoon addendum lists them with UTC lock times, result files and the order check. Deviations noted: D835 (D1), D863 (D1); D880 corrected by D880a/D895, D883 superseded by D896 (both kept as recorded).

## Change log
- CHANGELOG_v3.2.md covers every draft commit since v3.1. D847–D849 (draft creation and number checks) appear through the D-notes they applied. Page count updated 16 → 18 (**fixed**).

## Consistency
- prediction_sheet.md agrees with Table I (per-branch conditions): m_ν₁ windows (D895, D900), the ρ AD section, D792 marked superseded, Σm_ν data note (D902). Referee passes R2 and R3 closed with Responses (REFEREE_v3.2_R2.md, _R3.md).
- Frozen predictions unchanged throughout.

## Substantive items (not fixed here; for the record)
- None blocking. The draft states openly what remains open: P3 has no string origin; the two fitted small numbers (ε at τ = i, the ρ lift); the Weinberg suppression (instanton condition, marginal at τ = i).

## Decisions left for Danny
1. Publish v3.2 to Zenodo as a new version of the SERAPIS record, or keep holding it. (No action without your explicit word.)
2. If publishing: the title, author line and email are unchanged from v3.1 — confirm they are still what you want on the public record.
