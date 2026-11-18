# PREREG NA5 — node audit phase 5: canonical-factor consistency across the SERAPIS-E reheating/lepto scripts
Locked before running. Question left open by NA3 (D1235): does the 2⊕1 flavour modulus coincide with SERAPIS-E's inflaton, so that the n = 1 factor y√2 applies?
## Test (deterministic code/text reading, script below run once)
1. Text: D721–D722 state whether φ → NN decays are of SERAPIS-E's inflaton through the flavour modulus at ρ. If yes, the inflaton IS the flavour modulus for these nodes.
2. Code: every theory/modular/*.py that (a) maps the SERAPIS-E potential with y = exp(√2 φ) (n = 1) AND (b) uses a coupling factor y·√(2/3) (n = 3). Each such file is INCONSISTENT (the same field cannot have two Kähler weights).
3. Every theory/modular/*.py using y·√(2/3) or m = 2.2e13 is listed with the D-note it feeds (taint list).
Verdict: NA3 caveat RESOLVED (√3 applies) if 1 says yes; files in 2 are INCONSISTENT. No reruns here; downstream reruns need their own locks. Results: field_tests/results/na5_canonical_audit.txt.
