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

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Your Task                        │
│  evaluate(params) → score                        │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│              AEGIS Agent                         │
│                                                  │
│  ┌──────────┐  ┌───────────┐  ┌─────────────┐  │
│  │ Meta-    │  │ Strategy  │  │ Discovery   │  │
│  │ Learner  │→ │ Engine    │→ │ Engine      │  │
│  │ (UCB1)   │  │ (6 types) │  │ (anomalies) │  │
│  └──────────┘  └───────────┘  └─────────────┘  │
│                                                  │
│  ┌──────────┐  ┌───────────┐  ┌─────────────┐  │
│  │ Phase    │  │ Language  │  │ Event       │  │
│  │ Detector │  │ System    │  │ Bus         │  │
│  └──────────┘  └───────────┘  └─────────────┘  │
└──────────────────────────────────────────────────┘
```

---

## 📄 License

Commercial license — see [LICENSE](./LICENSE) for details.  
Free for students with valid .edu email.

---

**Built by Danny Lee Eldridge** — Independent researcher since 2012.  
danny@aegis-agent.dev
