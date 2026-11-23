# Referee ledger: every tool, every ping-pong round

A round = an independent referee (person or separate agent that did not build the tool) attacks the locked plan, the code and
the claims; the builder fixes only through a DEVIATIONS note written before any rerun; repeat until a round returns NULL.
`python tools/gifts/pingpong_suite.py` re-runs every locked test any time (also in CI, job `gifts`).

| Tool | For | Lock | Rounds | Verdict | Deviations |
|---|---|---|---|---|---|
| Spindle | Y. Liu (OSU) | D2183-D2185 | R71, R72 | NULL after fixes | PREREG_D2183_*_DEVIATIONS, D2185 DEV-1 |
| Zurvan | H. Baer (OU) | D2187 | R75, R75b | NULL | DEV-1..13 |
| Aion | K. S. Babu (OSU) | D2188 | R76, R76b | NULL | DEV-1..9 (DEV-8 Lantern kept by author) |
| Chronos | Nuclear rung (OU/OSU) | D2189 + A1-A3 | R77 (3 major, fixed); R78 running | pending | DEV-1..9 |

## Next in the rotation (older toolkits, one per loop tick)
Hyperion (astro / BBN / neutron stars) -> CERN+1 (LHC toolkit) -> Lattice Lab -> Janus (astro, lt) -> SERAPIS calc -> chem -> golden.
Each gets: lock a short referee charge, one independent referee round, DEVIATIONS for any fix, rerun its CI tests, record here.
