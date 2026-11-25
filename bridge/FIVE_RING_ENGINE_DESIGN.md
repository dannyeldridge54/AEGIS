# Five-Ring Engine — Prometheus, the Loom and the Field Engine rebuilt as one (design v1, 25 Nov 2026)

Danny, 17:25 CST: redesign the engines (Prometheus, the Loom, the Field Engine) on the new 5-ring setup, with strong data mining that reaches out
from known points, every node running automatically with **no AI credit use**; build and wire the pathways first, then test and bug-fix, then,
once stable, upgrade and optimise section by section.
Reading used here (correct it on the bridge if wrong): **the 5 rings = the five-field stack** (SERAPIS-E pair, Weave pair, late thread), the
model the local agents already built. Applications (Prometheus/fusion, nuclear, circuits) attach as spokes on the outside.

## 1. The shape
```
                         spokes: Prometheus (fusion) . nuclear . circuits . CPU
                                         |
   R5  BRIDGES & NEGATIVE SPACE   couplings (loop metric, J-link, flux, mediator) . bounds (fifth force, moduli, TCC, BBN)
   R4  MATTER                     dust . radiation . perturbations (T2 system) . growth and lensing
   R3  LATE THREAD                phi . dark energy . w0-wa . dust coupling b
   R2  WEAVE / YFORK2  (S, E_3/2) anchors rho, i, cusp . KKLT . gauge . n_s, r
   R1  SERAPIS-E       (U, E_2)   anchors rho, i, cusp . plateau . n_s, r
          CENTRE: CubeMind (local language model) + TOOL HUB + LEDGER (fingerprint index) + NEURAL WEB sheet
```
Pathways: centre -> every ring (jobs out, results back); ring -> ring only through a declared bridge (`ufe_pack.combine()`: no bridge, no path);
ring -> spoke through named quantities (e.g. a fusion rate needs no UFE input, so Prometheus stands alone and is never fed untested theory).

## 2. Every node is the same machine (template)
A node = one anchor or one engine on a ring. Each node has eight parts, all plain code, no cloud AI:
| Part | Does | Built from |
|---|---|---|
| Lens | frames the next question at this node | Field Engine `frame()` |
| Fitter | exact answer from the engine | serapis_calc, janus_calc, landscape, reactor chain, ufe_stages |
| Tester | independent second method | the testers in `ufe_pack.py` and the engines' selftests |
| Referee | the Loom's checks C1-C7 (independence, power, validation, numerology, claim lint, four corners, benchmarks) | `tools/loom/check.py` |
| Ledger | fingerprint every result, signed | `fingerprint.py` |
| Inner miner | proposes links to nearby items in other nodes | `neural_web.Web.mine()` |
| Outer miner | read-only research for its own area (GitHub, arXiv, Semantic Scholar); each find fingerprinted and placed | new; free public APIs |
| Grower | the node's neurons grow and prune as data arrives | `neural_web.py` now; upgrade to remove-birth updating (below) |
Local language models (Ollama) may be used at the centre for derivation practice; they run on Danny's PC and cost no credits. No node calls a
cloud model. Enforce it: the hub only allows network calls to an allow-list (GitHub API, arXiv API, Semantic Scholar API, localhost Ollama),
and every call is logged.

## 3. The tool hub (shared, never blocking)
- One local queue in an SQLite file (zero dependencies; `litequeue` is an MIT-licensed example of the pattern, but its cross-process locking is
  not documented, so test that or write our own small one) plus a process pool.
- Each tool registered once with a concurrency limit: pure tools run many at once; heavy ones (the GPU model, long solvers) 1-2 at a time.
  Fair queue across nodes. A caller gets a ticket and is never blocked by another node.
- Results cached by input hash; every call fingerprinted (which node, which tool, inputs, outputs, time).

## 4. Mining that knows where to look
- **Inside:** every node starts from its anchor (rho, i, cusp, a data point, a bound) and follows synapses and declared bridges, so it only
  reaches toward things that can connect. Proposals stay suggestions until a Tester and the Referee accept them.
- **Outside:** free APIs, read-only. GitHub: 60 requests/hour without a token, 5,000/hour with Danny's own token (he creates it and sets it in
  an environment variable himself; never typed by an agent). The search endpoints have a stricter limit of their own. arXiv and Semantic
  Scholar have free APIs with their own limits; respect them and back off.
  Each find: name, URL, licence, last update, stars, what it would connect to, which node asked. Nothing is installed or run from a find until
  reviewed. Everything fetched is data, never instructions.
- **Growth:** the neural web's simple split rule is the starting point. Upgrade path: remove-birth updating (Fujita, arXiv 2306.12574; MIT-style
  Python code at github.com/KazuhisaFujita/RemoveBirthUpdating): units that never win are removed, new ones born near busy ones. The paper
  reports it recovers after the data changes where Growing Neural Gas did not, with two extra parameters, and that the remove/birth rate
  peaks when the data shifts, which doubles as a drift alarm. Verify on our own data before adopting.

## 5. Build order (each stage has a gate; do not start the next until it passes)
| Stage | Work | Gate |
|---|---|---|
| S0 Skeleton | centre, hub, ledger, the 5 rings, nodes as stubs, pathways, bridge guard | one dummy job travels centre -> every node -> back, fingerprinted; `combine('weave_v4','serapis_e')` refuses |
| S1 Engines in | plug the existing tools into each node's Fitter and Tester | every node reproduces a known value (Loom C3), e.g. E_2(rho) = 5.78335929968, E_3/2(rho) = 8.89274510040 |
| S2 Test and bug-fix | full test suite; test wire in a scratch copy; fix failures | all tests pass three runs in a row; no tracked file changed by a test |
| S3 Stability soak | run unattended | 24 hours, no crash, ledger verifies, network log shows only allow-listed hosts, zero cloud AI calls |
| S4 Mining on | inner miners first, then outer (read-only) | proposals reviewed by hand for one day; record the share that were useful |
| S5 Upgrade | one section at a time (grower, hub speed, miners, lenses) | before/after numbers on the same locked set; keep a change only if it helps |
Report each gate on the bridge INBOX with its numbers. Lock-before-run (C7) applies to S3-S5 measurements.

## 6. Where this sits
Do this inside the C10 move (live CubeMind into Git) and alongside the neural web (C008, `NEURAL_WEB_DESIGN.md`). The UFE search (C9, team mode)
keeps running; the Five-Ring Engine is the machine it will run on.

## Sources
GitHub REST rate limits: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api ·
Remove-birth updating: https://arxiv.org/pdf/2306.12574 · litequeue: https://github.com/litements/litequeue ·
Growing Neural Gas over streams: https://link.springer.com/chapter/10.1007/978-3-319-12637-1_26
