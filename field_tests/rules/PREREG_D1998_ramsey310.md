# PREREG D1998: pulse search for R(3,10) = 41 (Danny 20:29–20:31: "point the engine at a test and crank it"). Locked before the search runs.
- **Known:** 40 ≤ R(3,10) ≤ 41. Exoo found the 39-vertex lower-bound graph; Angeltveit (arXiv 2401.00392) proved ≤ 41.
- **Target:** a graph G on 40 vertices with **no triangle** and **independence number α(G) ≤ 9**. Such a G proves R(3,10) ≥ 41, so R(3,10) = 41.
- **Engine** (tools/ramsey/r310.c): simulated-annealing pulses. Moves keep G triangle-free at all times. The score is the number of independent 10-sets. Each pulse is an annealing epoch with reheating, and several independent workers run on different seeds.
  - Cloud: 2 workers.
  - Danny's PC (CubeMind workspace): the same binary source, different seeds.
- **Success requires an independent verification** before any claim:
  1. A separate verifier (tools/ramsey/verify.py, pure Python) checks triangle-freeness and that no independent 10-set exists, by exhaustive search.
  2. A second check with a different algorithm: a networkx maximum-independent-set via the complement clique number.
  3. The graph6 string is committed.
  Only then is it a result. A paper or claim follows only after a referee pass and a literature check: is the graph already known? Was R(3,10) settled meanwhile?
- **Expected (honest prior):** failure is likely. Exoo and others ran large searches without success, and R(3,10) = 40 is possible, in which case no such graph exists. The run reports the best score (the fewest independent 10-sets) reached.
- **Budget:** up to 2 h wall in the cloud, and as long as the PC session runs.
