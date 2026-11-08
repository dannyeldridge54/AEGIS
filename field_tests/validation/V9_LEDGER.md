# V9 — Pre-registration ledger (every rule, its hash, every verdict)

**Built 8 Nov** by `field_tests/ledger/build_ledger.py` → `field_tests/ledger/LEDGER.md` + `ledger.json`.
- 50 locked files; SHA-256 re-verified on disk: 47 exact, 3 identical except Windows CRLF line endings (two CubeMind
  SPT-3G rules and their companion script), **0 content changes**.
- 72 recorded verdicts (CLAIMS_INDEX to 2 Nov + CURRENT_MODEL since): by keyword class pass 18, fail 16, neutral 10,
  mixed 1, open 6, reported 21. Classes are for counting only; verdict text is authoritative.
**Next.** Rerun after each scored test (check-ins); add public timestamps (git push time, Zenodo DOI, Software
Heritage) per rule; present as an appendix table in the paper.
