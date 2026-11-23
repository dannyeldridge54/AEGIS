# PREREG CM-PAPERS — CubeMind nuclear paper generator (locked before build/run)

Date: 2026-11-23. cm_paper.py builds one self-contained HTML "technical note" per nuclear field section of
RESEARCH_LIMB.md that Chronos covers: medical isotopes (S4), fusion fuel/tritium (S2), nucleosynthesis and
transients (S3), fission decay heat (S5), safeguards and environmental clocks (S6). Section 7 (space radiation)
has no tool and gets NO paper (listed as "not built" in the index). Each note: Lantern panel, title, author line,
abstract, study context (from RESEARCH_LIMB, labelled [study]), methods (equations, cited), results tables and
animated Iris charts, validation record, limits, references, and a provenance appendix (every engine call's args
and full result, plus sha256 of the engine files). Prose is template text; no language model writes numbers.

Tests:
- P1 trace: every number printed in abstract/results is produced from an engine result field; re-running each
  engine call with the recorded args reproduces every printed value to 4 significant figures.
- P2 render: each note loads in headless Chromium with no console errors and >= 1 chart canvas drawn (non-blank).
- P3 speed: whole suite builds in <= 10 s on the cloud machine.
- P4 honesty: every note contains a "Limits" section and every chart carries the engine's own title/units.
Pass = all four. Fails recorded as failed-as-locked; fixes via DEVIATIONS written first; one rerun.
Separately (not a test): the Ask server gets a job/progress path (/api/ask_start, /api/job) and model limits
(num_ctx 4096, num_predict 512, keep_alive 30m, 4 rounds) to stop the browser freeze seen at 09:35.
