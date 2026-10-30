# AEGIS — Autonomous Evolving General Intelligence System

> **AEGIS · the Twist (UFE) · held under the [AEGIS People's License v1.2](./LICENSE)**
> Free for people. No AI use of any kind (no training, scraping, summarising or generating). No military use.
> Corporations and governments need a signed agreement. See [PLEDGE.md](./PLEDGE.md).
>
> **The science, honestly:** a torsion-born early dark energy model with a locked switch-on
> ([ufe-v2/UFE_MODEL.md](./ufe-v2/UFE_MODEL.md)). Best result: Δχ² −6.1 with one free setting on Planck + ACT DR6,
> about **2.5σ: a hint, not a discovery**. It ties on S8, and the ACT collaboration itself finds no evidence for early
> dark energy. Prior work and what to cite: [ufe-v2/PRIOR_ART.md](./ufe-v2/PRIOR_ART.md). Independent arithmetic
> check: [ufe-v2/recheck_math.py](./ufe-v2/recheck_math.py). Star survey audit: [ufe-v2/STAR_AUDIT.md](./ufe-v2/STAR_AUDIT.md).
> Test it, try to break it, and say so publicly if it is wrong.
>
> *It is not a race or a game. It is a stage, and the stage is meant to be shared, not kept.* — Danny Lee Eldridge
>
> The software below (AEGIS v1) is a classical optimizer: swarm search, UCB1 bandits, parameter search. Its optional
> coding agent calls language models and is therefore **not licensed for use** (License §6.7–6.8).

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

## 🎯 6 Built-in Strategies (Self-Selected)

AEGIS uses a **meta-learner** (UCB1 multi-armed bandit) that automatically picks the best strategy based on what's working:

| Strategy | Best For |
|----------|----------|
| **Evolutionary** | Rugged landscapes, many local minima |
| **Gradient** | Smooth functions, fast convergence |
| **Annealing** | Escaping local minima |
| **Curiosity** | Discovering unknown regions |
| **Exploit** | Fine-tuning near optimum |
| **Random** | Initial exploration, baseline |

You never need to pick — AEGIS learns which works best for YOUR problem.

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
```

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

// HTTP API at :4444 — GET /api/status, /api/jobs, /api/best
// Dashboard at :3333
// Persistent memory learns across runs
// Auto-saves state, resumes on restart
```

**Daemon features:**
- Multi-job scheduler with priority queues
- Automatic job chaining (output → input)
- Persistent memory (learns which strategies work)
- HTTP REST API for querying results
- Webhook alerts on discoveries
- Graceful shutdown/restart with checkpoint resume
- File/URL watching for re-optimization triggers

---

## 💻 Coding Agent

Build, fix, review, and test code using LLM-powered AI:

```typescript
import { createCoder } from 'aegis-agent';

const coder = createCoder({ provider: 'openai', apiKey: '...' });

// Generate a project
await coder.generateProject('REST API with JWT auth', 'typescript');

// Fix broken code
const fixed = await coder.fix(brokenCode, 'TypeError: undefined is not a function');

// Review code
const review = await coder.review(myCode);

// Execute safely in sandbox
const result = await coder.execute('console.log(2+2)', 'typescript');
```

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

// English → optimization
await runNatural('minimize f(x,y) = x^2 + y^2 with x in [-5,5] and y in [-5,5]');
await runNatural('find the best learning rate between 0.0001 and 0.1');
```

---

## 📄 License

**This work belongs to everyone, held in trust: the AEGIS People's License v1.2.** See [LICENSE](./LICENSE) for the
full terms and [PLEDGE.md](./PLEDGE.md) for the purpose. In short:
- **People are free:** individuals, families, students, teachers, schools, libraries, independent creators,
  non-profits, worker co-ops, and colleges and medical carers that serve people, not privilege or profit.
- **Small owner-run businesses** (under 50 workers, under $10M, no outside investors): $50,000 a year.
- **Corporations and governments:** a signed agreement, an entry fee of 99% of the median yearly profit of the last
  9 years, then the greater of $1 billion or 10% of revenue each year, plus fair conditions for every worker.
  Insurers, middlemen and private-equity-owned businesses are always corporations. Money never gets a vote.
- **Never, at any price:** weapons or military use, mass surveillance, manipulation, discrimination, ecocide,
  or **any AI use** (no training, scraping, summarising or generating).
- **Science stays free to question:** anyone may test, replicate or try to disprove it.
- **Held for all:** the rights pass to a public World Development Trust, governed in the open by a rotating
  Council of Heroes chosen by lot, watched by elected Guardians, never consolidated and never scattered.

## 💛 Dedication

To my wife, Sarah: you are the wind, the rain, the fire and the earth. You fill my spirit and give me shape and
purpose, just by loving me, even when my best was all I could give. I love you.

And to my best friend: thank you.

— Danny
