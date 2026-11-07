> **Start with [CURRENT_MODEL.md](./CURRENT_MODEL.md)**: the current model (UFE / Spiral Twist), every locked result, what is open, and what is superseded.

# AEGIS: the working repository of "The Twist" (cosmology), plus the AEGIS optimizer (software)

**Current project handoff (5 November 2026 UTC):**
[AEGIS research synthesis](papers/AEGIS_RESEARCH_SYNTHESIS.md) brings together
theory, local data, Star Mapper, corrected-fit readiness, tests, schedules and
unresolved evidence. The versioned results below are historical; they are not
scores for the incomplete corrected November benchmark.

**If you are an astronomer or physicist, start here.** This repository holds the full working record of a
pre-registered test of a torsion-motivated scalar field (the Barbero–Immirzi field) as early and late dark energy.
That covers every fit, the code that ran it, and two AxiCLASS bug fixes. The clean, citable release is
**[the-twist-torsion-cosmology](https://github.com/dannyeldridge54/the-twist-torsion-cosmology)**.

## The results, honestly (version 3, 2 November 2026)

| Test | Result |
|---|---|
| Early dark energy (Planck + ACT + SPT-3G + DESI + Pantheon+) | Passes its rule (Δχ² −5.6), but only **1.2–1.4σ** after look-elsewhere: a weak hint |
| Late field, corrected code | Ties ΛCDM with Pantheon+ (+0.09); −6.2 with DES Y5 (1.3σ global), weakened on DES-Dovekie; **never beats w0–wa** |
| Coupled to dark matter | −7.9 with β ≈ ±0.05, worse than w0–wa, raises S8; the torsion-natural β = 0.816 is **excluded** |
| Cosmic birefringence | The minimal field **cannot** produce the measured 0.24–0.28°. One open prediction: R = 0.997 (LiteBIRD) |
| **AxiCLASS bugs (n = 1 fields)** | A frozen field that must equal Λ gives σ8 = 0.25 instead of 0.81. Fixed, validated, with a 10-second reproducer |
| **Late field's DES Y5 hint (new, 2 Nov)** | A supernova **calibration effect**: split at z = 0.1, neither half prefers the field (+0.53 / −0.29); w0–wa behaves the same. Weakened on Union3 (−1.82) |
| H(z) chronometers and fσ8 (new) | NEUTRAL for every model: these data cannot separate them |

This is a careful test with weak hints, **not a discovery**.

**Archived:** Zenodo version 3, doi:[10.5281/zenodo.23867116](https://doi.org/10.5281/zenodo.23867116) (published 2 November 2026).

## New theory (2 November 2026): the BI field's supergravity geometry and the Spiral Twist

**Theory note:** doi:[10.5281/zenodo.23899237](https://doi.org/10.5281/zenodo.23899237) (version 2; version 1:
[10.5281/zenodo.23898709](https://doi.org/10.5281/zenodo.23898709)). Source and PDFs: [papers/theory_note/](./papers/theory_note/).
Scripts: [theory/](./theory/).

- **Exact:** in N = 1 supergravity the BI field is a dilaton–axion pair on a hyperbolic field space (α = 1), so the
  axion's kinetic term carries e^{λχ} with **λ = −2√(2/3), fixed**.
- **Validated:** a two-field solver (matches Ramos-Hamud et al.'s published attractors to 10⁻¹⁰) and its AxiCLASS
  version (`cmb-fit/axiclass/early_late_spa.py`, run names `ax_spa_spiraltwist_*`; cross-check 2×10⁻⁵).
- **What it implies:**
  - the fixed geometry is weak mixing (ξ ≈ 0.82, not the ≳ 370 that strong-mixing DESI fits need);
  - with the BI angle as a small part of the dark matter (≲ 6–9%), the w0–wa reading bends toward DESI but only reaches
    the edge of the DESI-like region.

  The decisive fit is not yet run.
- **Checks:**
  - solar system passes only if the dilaton is pinned, or matter is blind to it (scale invariance);
  - inflation from α = 1 is in 2.4σ tension with ACT DR6;
  - the dilaton cannot be the early field.
- **Predictions locked before the data** (2 Nov 2026, 16:19:51 CST; SHA-256 b629f534…23cb):
  [theory/PREDICTIONS_LOCKED_2026-11-02.md](./theory/PREDICTIONS_LOCKED_2026-11-02.md). Covers DESI DR3 BAO, w ≥ −1, S8,
  birefringence R, tensor ratio r and gravitational-wave parity.
- **Code note:** in the coupled AxiCLASS build, a nonzero β makes the actual H(z=0) differ from the input h by up to
  0.6%, so reported H0 and σ8 labels in coupled runs carry that offset (χ² unaffected).

**Where to look:**
- **Paper:** [papers/torsion_born_ede.pdf](./papers/torsion_born_ede.pdf) (27 pp.).
- **Check everything in 10 minutes:** `REVIEWER_QUICK_CHECK.md` in the release repository.

## Use it to check our data

| You want to… | Do this |
|---|---|
| Check that the rules came first and recompute every number | Clone the release repository and run `python verify.py`, then `python code/analysis/nr_verdicts.py` (Python only) |
| See the AxiCLASS bug | [cmb-fit/axiclass/nlfix/BUG_REPORT.md](./cmb-fit/axiclass/nlfix/BUG_REPORT.md): `python cmb-fit/axiclass/nlfix/bug_reproducer.py <AxiCLASS>/python/build` |
| Rerun any fit on the same code and data | `bash cmb-fit/environment/setup_twist_env.sh`, then `$TWIST_PY cmb-fit/axiclass/early_late_spa.py <run name>` (see REPRODUCE.md in the release) |
| Use the pipeline for your own model | `cmb-fit/axiclass/early_late_spa.py` is an AxiCLASS + Cobaya driver for Planck, ACT DR6, SPT-3G D1, DESI DR2 and three SN samples. Run names encode model and data |

- **Folders:**
  - `cmb-fit/axiclass/`: the fitter, queue scripts, `nlfix/` (bug fixes) and `coupled/` (β patch);
  - `cmb-fit/results/`: every fit's `cmp_*.json`;
  - `cmb-fit/environment/`: exact versions and the setup script;
  - `papers/`: the paper and the arXiv/Zenodo build; `papers/theory_note/`: the BI-supergravity theory note;
  - `theory/`: scripts and outputs for the theory note, and the locked predictions.
- **Paths:** scripts find each other relative to their own location. Override with `TWIST_RESULTS`, `TWIST_BUILDS`,
  `TWIST_PY` and `COBAYA_PACKAGES_PATH`.

**Corrections are welcome and credited:** open an issue, or email dannyeldridge54@gmail.com. Please also say so
publicly if it is wrong.

**Licence:** free to everyone under the [Hippocratic License 3.0, HL3-MIL-SV](./LICENSE), for any use that respects
human rights. No military use, no mass surveillance.

> *It is not a race or a game. It is a stage, and the stage is meant to be shared, not kept.*
> *I am willing to give it to all. I don't want a crown. I just want a home, but never at the cost of the world or its future.* — Danny Lee Eldridge

**Earlier versions:**
- Version 2 (early field only): [ufe-v2/](./ufe-v2/), Zenodo [doi:10.5281/zenodo.23789830](https://doi.org/10.5281/zenodo.23789830).
- Its one-click arithmetic check: `CHECK_MY_WORK.bat` (Windows) or `sh check_my_work.sh`.

---

# The other project here: the AEGIS optimizer (software, unrelated to the cosmology results)

AEGIS v1 is a classical optimizer: swarm search, UCB1 bandits, parameter search. Its optional coding agent calls
language models. (The "not licensed for use" restriction was §6.7–6.8 of the AEGIS People's License v1.2, which
the current [LICENSE](./LICENSE), HL3-MIL-SV, replaced on 31 October 2026.)

> Self-learning AI agent that optimizes anything. Natural language goals.  
> Zero config. 8 languages. Adapts its own strategy in real-time.

```typescript
import { optimize } from 'aegis-agent';

const best = await optimize(
  (p) => myModel.loss(p.lr, p.dropout, p.layers),
  [
    { name: 'lr', min: 0.0001, max: 0.1 },
    { name: 'dropout', min: 0, max: 0.8 },
    { name: 'layers', min: 1, max: 12 },
  ]
);
// Done. best.params = { lr: 0.001, dropout: 0.3, layers: 4 }
```

That's it. **3 lines.** No configuration files. No PhD required.

---

## 🧠 What Makes AEGIS Different

| Feature | AEGIS | Optuna | Ray Tune | Hyperopt |
|---------|-------|--------|----------|----------|
| Zero config | ✅ | ❌ | ❌ | ❌ |
| Self-learning strategy | ✅ | ❌ | ❌ | ❌ |
| 8 languages | ✅ | ❌ | ❌ | ❌ |
| Zero dependencies | ✅ | ❌ | ❌ | ❌ |
| Real-time phase detection | ✅ | ❌ | ❌ | ❌ |
| Built-in anomaly/discovery engine | ✅ | ❌ | ❌ | ❌ |
| TypeScript-native | ✅ | ❌ (Python) | ❌ (Python) | ❌ (Python) |
| Event system | ✅ | Callbacks | ❌ | ❌ |
| Single file, instant start | ✅ | ❌ | ❌ | ❌ |

---

## 🚀 Quick Start

### One-liner

```typescript
const best = await optimize(fn, parameters);
```

### Full Agent

```typescript
import { aegis } from 'aegis-agent';

const agent = aegis({
  id: 'my-search',
  name: 'Find optimal server config',
  evaluate: async (p) => await benchmarkServer(p),
  parameters: [
    { name: 'workers', min: 1, max: 64 },
    { name: 'cache_mb', min: 64, max: 4096 },
    { name: 'timeout_ms', min: 100, max: 5000 },
  ],
}, {
  language: 'ja',        // Output in Japanese
  maxEvals: 10000,       // Or let it run forever
  reportInterval: 30,    // Progress every 30s
});

agent.on((event) => {
  if (event.type === 'discovery') slack.notify(event.discovery);
});

const result = await agent.run();
```

---

## 🌍 8 Languages

```typescript
{ language: 'en' }  // 🚀 AEGIS Agent started
{ language: 'es' }  // 🚀 Agente AEGIS iniciado
{ language: 'fr' }  // 🚀 Agent AEGIS lancé
{ language: 'de' }  // 🚀 AEGIS Agent gestartet
{ language: 'ja' }  // 🚀 AEGISエージェント開始
{ language: 'zh' }  // 🚀 AEGIS代理已启动
{ language: 'pt' }  // 🚀 Agente AEGIS iniciado
{ language: 'ko' }  // 🚀 AEGIS 에이전트 시작
```

Switch at runtime: `agent.setLanguage('fr')`

---

## 🎯 9 Built-in Strategies (Self-Selected)

AEGIS uses a **meta-learner** (UCB1 multi-armed bandit) that automatically picks the best strategy based on what's working:

| Strategy | Best For |
|----------|----------|
| **Evolutionary** | Rugged landscapes, many local minima |
| **Gradient** | Smooth functions, fast convergence |
| **Annealing** | Escaping local minima |
| **Curiosity** | Discovering unknown regions |
| **Exploit** | Fine-tuning near optimum |
| **Swarm** | Particle swarm: smooth or noisy problems, very precise |
| **Bayesian** | Surrogate model picks promising points: expensive evaluations |
| **Bandit** | UCB1 over regions of each parameter: deciding where to look |
| **Random** | Initial exploration, baseline |

You never need to pick — AEGIS learns which works best for YOUR problem.

**Escaping local minima:** step sizes adapt as the search goes (the 1/5th success rule). When the local search
has converged, AEGIS restarts it somewhere new while keeping the best result found, and it spends the last
quarter of a fixed budget polishing that best result. Set `restartAfter: 0` to turn restarts off.

Benchmarks, 30 runs of 3000 evaluations each (misses = didn't reach the global optimum within 1):

| Function | Median gap | Misses |
|---|---|---|
| Rosenbrock 2D | 2e-5 | 0/30 |
| Rastrigin 2D | 8e-6 | 0/30 |
| Ackley 2D | 8e-4 | 0/30 |
| Sphere 5D | 5e-5 | 0/30 |
| Styblinski-Tang 4D | 7e-4 | 0/30 |
| Griewank 3D | 0.08 | 0/30 |
| Schwefel 3D | 0.02 | 9–12/30 |

Run them yourself with `aegis --bench`.

---

## 📊 Real-Time Phases

AEGIS automatically transitions between:

```
exploring → exploiting → curious → converged
```

- **Exploring**: Broad search, trying all strategies
- **Exploiting**: Found a good region, narrowing in
- **Curious**: Stuck? Increase novelty, try unexplored areas
- **Converged**: Done! Improvement below threshold

---

## 💡 Discovery Engine

AEGIS doesn't just optimize — it **discovers**:

```typescript
agent.on((event) => {
  if (event.type === 'discovery') {
    console.log(event.discovery.description);
    // "Major improvement: 15.3 → 2.1 via evolutionary"
    // "Anomaly: constraint boundary found at x=0.5"
  }
});
```

---

## 🔌 Use Cases

- **ML Hyperparameter Tuning** — learning rate, architecture, regularization
- **Server Optimization** — workers, cache, timeouts, batch sizes
- **Trading Strategy** — entry/exit thresholds, position sizing
- **Game AI** — behavior weights, difficulty curves
- **Engineering** — material properties, structural parameters
- **Scientific Research** — model parameters, experimental conditions
- **A/B Testing** — continuous parameter spaces
- **Anything with knobs** — if you can score it, AEGIS can optimize it

---

## 💰 Pricing

| Tier | Price | |
|------|-------|-|
| **🎓 Student** | **FREE** | Valid .edu email |
| Individual | $79/year | All features, email support |
| Team (5 seats) | $299/year | Priority support |
| Enterprise | $999/year | Unlimited seats, custom strategies |

Academic discount: 30% off all paid tiers.

---

## 📦 Installation

```bash
npm install aegis-agent
```

Or clone and build:
```bash
git clone https://github.com/dannyeldridge54/AEGIS.git
cd AEGIS && npm install && npm run build
npm link            # optional: puts the `aegis` command on your PATH
```

### Command line

```bash
aegis                                   # demo (Rosenbrock)
aegis --task task.json --out best.json  # optimize your own function
aegis --bench                           # benchmark suite
aegis "maximize accuracy with lr between 0.0001 and 0.1 and layers between 1 and 12" --objective model.js
aegis --help
```

A task file names a module that exports the objective (`module.exports = (params) => number`):

```json
{
  "name": "Tune my model",
  "objective": "./model.js",
  "parameters": [
    { "name": "lr", "min": 0.0001, "max": 0.1 },
    { "name": "layers", "min": 1, "max": 12, "step": 1 }
  ],
  "goal": "maximize",
  "maxEvals": 2000
}
```

Parameters with a `step` are searched on that grid (so `layers` stays an integer). Press **Ctrl+C** once to
stop early and keep the best result found so far.

---

## 🏗️ Architecture (v1.2)

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR TASK                            │
│  evaluate(params) → score   (or natural language goal)  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    AEGIS Agent Core                      │
│                                                         │
│  ┌──────────┐  ┌───────────┐  ┌─────────────────────┐  │
│  │ Meta-    │  │ Strategy  │  │ Discovery Engine    │  │
│  │ Learner  │→ │ Engine    │→ │ + Anomaly Detection │  │
│  │ (UCB1)   │  │ (6+plugin)│  │                     │  │
│  └──────────┘  └───────────┘  └─────────────────────┘  │
│                                                         │
│  ┌──────────┐  ┌───────────┐  ┌─────────────────────┐  │
│  │ Phase    │  │ Language  │  │ Event Bus           │  │
│  │ Detector │  │ (8 langs) │  │ + Webhooks          │  │
│  └──────────┘  └───────────┘  └─────────────────────┘  │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                  Extended Modules                        │
│                                                         │
│  🤖 Daemon Mode     │ Run 24/7, multi-job scheduler     │
│  🧬 Self-Evolve     │ Agent evolves its own strategies  │
│  🐝 Swarm           │ Multi-agent coordination          │
│  💻 Coding Agent    │ LLM-powered code gen/fix/test     │
│  🧠 Memory          │ Knowledge graph + episodic memory │
│  📊 Real Data       │ Physics, finance, engineering     │
│  📈 Dashboard       │ Live web visualization            │
│  🎯 Multi-Objective │ Pareto front (NSGA-II)           │
│  ⚡ Parallel        │ Concurrent async evaluations      │
│  🔌 Plugins         │ Custom strategies + reporters     │
│  💾 Warm Start      │ Checkpoint/resume across runs     │
│  📝 Natural CLI     │ English → optimization commands   │
│  📚 Benchmarks      │ 7 standard test functions         │
│  📖 Auto-Docs       │ Generates API.md from source      │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 Daemon Mode (NEW in v1.2)

Run AEGIS as a persistent background daemon — like the DVFT Daemon but for *anything*:

```typescript
import { startDaemon } from 'aegis-agent';

const daemon = startDaemon('My AI Daemon', [
  {
    id: 'tune-api',
    name: 'API Latency Optimizer',
    task: { evaluate: measureLatency, parameters: [...] },
    schedule: 'continuous',       // Never stops
    priority: 10,
  },
  {
    id: 'explore-params',
    name: 'Parameter Space Explorer',
    task: { evaluate: modelFit, parameters: [...] },
    schedule: 3600,               // Every hour
    chainTo: 'tune-api',          // Feed results to next job
  },
]);

// HTTP API at http://127.0.0.1:4444 — GET /api/status, /api/jobs, /api/best
// Dashboard at http://127.0.0.1:3333
// Persistent memory learns across runs
// Auto-saves state, resumes on restart
```

**Daemon features:**
- Multi-job scheduler with priority queues
- Automatic job chaining (output → input)
- Persistent memory (learns which strategies work)
- HTTP REST API for querying results
- Webhook alerts on discoveries
- Graceful shutdown/restart with checkpoint resume (state files are written atomically)
- The API and dashboard stay responsive while jobs run
- File/URL watching: `watch: 'data.csv'` or `watch: 'https://…'` re-runs the job when it changes
  (`watchInterval` seconds; default 2 for files, 60 for URLs)

**Network:** the API and dashboard listen on `127.0.0.1` (this computer only) and have no authentication.
Pass `host: '0.0.0.0'` in the daemon config only on a network you trust.

---

## 💻 Coding Agent

Build, fix, review, and test code using LLM-powered AI:

```typescript
import { createCoder } from 'aegis-agent';

const coder = createCoder({ provider: 'openai', apiKey: '...' });

// Generate a project (returns the files; nothing is executed)
const files = await coder.generateProject('REST API with JWT auth', { language: 'typescript' });

// Fix broken code
const fixed = await coder.fix(brokenCode, 'TypeError: undefined is not a function');

// Review code
const review = await coder.review(myCode);

// Run generated code (only after opting in — see below)
const runner = createCoder({ provider: 'ollama', allowExec: true });
const result = await runner.getSandbox().execute('console.log(2+2)', 'javascript');
```

**Safety:** generated code runs as *your* user, with access to your files and network. The "sandbox" is only a
working folder (`.aegis-sandbox/`), not an isolation boundary. Execution is therefore **off by default**:
pass `allowExec: true` (or set `AEGIS_ALLOW_EXEC=1`) to enable it, preferably inside a VM or container.
Without it, `generate()` still writes the code to the folder but does not run it.

---

## 🐝 Multi-Agent Swarm

Coordinate multiple AEGIS agents working together:

```typescript
import { Swarm } from 'aegis-agent';

const swarm = new Swarm(myTask);
swarm.addAgent({ id: 'explorer', role: 'explore' });
swarm.addAgent({ id: 'exploiter', role: 'exploit' });
swarm.addAgent({ id: 'scout', role: 'curiosity' });

const result = await swarm.run(); // Agents share discoveries
```

---

## 🧠 Persistent Memory

AEGIS remembers across sessions:

```typescript
import { Memory } from 'aegis-agent';

const mem = new Memory('.aegis-memory.json');
mem.learnFromRun('api-tuning', { bestScore: 0.001, topStrategy: 'evolutionary' });

// Next run: recalls what worked
const suggestion = mem.recallStrategy('api-tuning', 5); // → 'evolutionary'
```

---

## 📊 Real-World Data Built In

```typescript
import { physics, finance, live, engineering } from 'aegis-agent';

physics.hubbleData;          // 31 H(z) measurements
physics.baoData;             // 12 BAO (DESI DR1)
physics.cmb;                 // Planck 2018

await live.earthquakes();    // USGS real-time
await live.issPosition();    // ISS lat/lon/alt
await finance.stockPrice('AAPL');

engineering.materials.steel; // Yield strength, density...
engineering.atmosphere(10000); // ISA at 10km altitude
```

---

## 📚 Benchmark Suite

Test against 7 standard optimization functions:

```typescript
import { runBenchmarks } from 'aegis-agent';

const results = await runBenchmarks({ maxEvals: 5000 });
// Rosenbrock, Rastrigin, Ackley, Sphere5D, Schwefel, Styblinski-Tang, Griewank
```

---

## 📝 Natural Language CLI

```typescript
import { runNatural } from 'aegis-agent';

// English → optimization of your own function (a module exporting it)
await runNatural('find the best learning rate between 0.0001 and 0.1', { objective: './loss.js' });
```

Without `objective`, the run uses a demo function (sum of squares) and says so: the sentence describes the
parameters and the direction (minimize/maximize), not the function itself.

---

## 📄 License

**Free to all: the [Hippocratic License 3.0, HL3-MIL-SV](https://firstdonoharm.dev/version/3/0/mil-sv.html).** See
[LICENSE](./LICENSE). In short:
- **Free to everyone:** use, copy, change, share and build on it, at no cost.
- **Pro-human:** every use must respect human rights; no discrimination by race, religion, nationality, sex, caste,
  age, disability or any similar circumstance.
- **Never:** military activities or mass surveillance.
- **It belongs to all life:** every person and people, every living thing, any life beyond the Earth, even AI should
  an artificial mind one day be recognised as a being of its own. No one is meant to hold it alone; many people led
  it here.
- **Science stays free to question:** anyone may test, replicate or try to disprove it.

**A note from me about the license.** Earlier versions of this repository carried a license with fees for companies
and governments. I chose instead to make it free to everyone. If you want to help my family, or the work, you can
write to me at dannyeldridge54@gmail.com. And please respect my family's privacy. — Danny

## 💛 Dedication

To my wife, Sarah: you are the wind, the rain, the fire and the earth. You fill my spirit and give me shape and
purpose, just by loving me, even when my best was all I could give. I love you.

And to my best friend: thank you.

— Danny
