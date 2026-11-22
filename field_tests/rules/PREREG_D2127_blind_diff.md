# PREREG D2127: checklist item 20, independent reproduction diff. Locked before running the builder-side diff.

- **Inputs:** the referee's blind implementation (tools/seed/referee_blind/blind.py). It parses the exceptional table from the LaTeX and was written from p.tex, independent in transcription and in code structure. It shares the documented readings: z₀, block-3, P2 and cyclic X/Y. Its raw output is tools/seed/referee_blind/blind_out.json.
- **Test:** an exact diff of all 8 cycle vectors (Table 27 plus 3 random branes r1–r3) and of all random-brane χ entries, between blind_out.json and our engine.
- **Verdict:** PASS if there are 0 differences.
