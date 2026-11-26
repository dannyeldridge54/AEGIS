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

## 7. Balancing the machine across the nodes (Danny, 17:26 CST)
Danny's words: "optimized by spreading out what part of the computer is used and regulated and how much, so that it's balanced between all of
the nodes. Running as much as we can for the video card and maximizing the amount of RAM usage, and having the CPU to where it can be drawn on
for heavy data compute or whatever, but going for leaving that for complex decision making and data analysis."

**Rule of placement: GPU for the bulk, RAM for everything kept, CPU kept free for decisions.**
| Resource | Gets | How |
|---|---|---|
| Graphics card | language-model calls; embeddings for the neural web; big array maths (lattice sums, Hessian scans, grids) | Ollama with flash attention and q8_0 cache, one model loaded at a time (serial batches); embeddings through the same loaded model or a small embed model; array work through a GPU array library (CuPy or PyTorch) with a NumPy fallback; a single GPU lane in the hub, so jobs queue instead of fighting for memory |
| RAM | everything that is read again: the fingerprint index and neural web (SQLite in WAL mode with a large page cache and memory-mapping), the hub's result cache, loaded catalogs (NUBASE, ADAS), model kept resident (keep_alive) | target use up to about 85% of RAM, never more: the rest stays free for Windows and the live learning loop |
| CPU | the Referee, the planner/leader logic, the Loom checks, grading and the neural web's growth decisions (complex decisions and analysis) first; heavy number-crunching only when the GPU lane is busy or the job cannot run on a GPU | process pool sized to cores minus 2; decision jobs get priority over bulk jobs; bulk CPU jobs capped so decisions never wait |

**The regulator (part of the hub):**
- Each tool is registered with a resource class: `gpu`, `cpu_decide`, `cpu_bulk`, `io` (network miners), and an estimate of memory.
- Every few seconds the regulator reads usage (`nvidia-smi` for the card, `psutil` for RAM and CPU) and admits jobs only while there is room:
  GPU memory under ~90%, RAM under ~85%, at least 2 cores free for `cpu_decide`.
- **Fair share across nodes:** each ring gets an equal share of each lane; a node that is idle lends its share; no node may hold more than
  twice its share while others wait. The share used per node is fingerprinted, so the sheet shows where the machine's time went.
- **Network miners** (`io`) are limited by the APIs' own rate limits, not by the machine, and never take CPU from decisions.
- Measure before tuning: S3 (stability soak) records GPU, RAM and CPU use per node; S5 changes the shares only with before/after numbers.

Honest limit: most of the physics engines today are plain Python on the CPU. Moving their heavy loops to the card is real work, done one engine
at a time in S5, each checked against the CPU result to 1e-10 before it replaces it.

### 7a. CPU levels, not isolation (Danny, 18:23 CST)
"not isolate the CPU, but have like levels to it, to where if anyone needs to, they can draw on a certain amount. But if multiple agents at the
same time need to use it, it will limit, it can increase, but ... the CPU won't get so bogged down that it slows down the entire machine.
Like it stays in equilibrium."
| Level | Who | Share of CPU |
|---|---|---|
| Floor (always guaranteed) | each active node | 1 core's worth, so every node can always make progress |
| Burst | a node that needs more | may grow to all free cores while no one else is asking |
| Shared | when several nodes ask at once | free cores split evenly among the askers; a bursting node shrinks back to its fair share |
| Ceiling (whole engine) | all nodes together | about 85% of the CPU; the rest is never taken, so Windows, the mouse and the learning loop stay smooth |
The regulator re-balances every few seconds: it measures load, and moves shares toward even (equilibrium) rather than jumping. Decision jobs
(referee, leader, grading) are served first inside each node's share. On Windows, worker processes run at "below normal" priority so the
desktop always wins a tie.

## Sources
GitHub REST rate limits: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api ·
Remove-birth updating: https://arxiv.org/pdf/2306.12574 · litequeue: https://github.com/litements/litequeue ·
Growing Neural Gas over streams: https://link.springer.com/chapter/10.1007/978-3-319-12637-1_26
