# AEGIS — Autonomous Evolving General Intelligence System

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

Commercial license — see [LICENSE](./LICENSE) for details.  
Free for students with valid .edu email.

---

**Built by Danny Lee Eldridge** — Independent researcher since 2012.  
danny@aegis-agent.dev
