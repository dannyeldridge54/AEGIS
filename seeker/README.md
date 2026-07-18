# Seeker — Autonomous Discovery Engine

> Solves UFE optimization. Hunts anomalies. Surfaces discoveries.  
> Scripts, records, and learns from every evaluation. Runs AEGIS core + daemon.

```typescript
import { optimize } from 'seeker';

const best = await optimize(
  (p) => myModel.loss(p.lr, p.dropout, p.layers),
  [
    { name: 'lr', min: 0.0001, max: 0.1 },
    { name: 'dropout', min: 0, max: 0.8 },
    { name: 'layers', min: 1, max: 12 },
  ],
  { seed: 42 }  // Deterministic. Reproducible. Every time.
);
```

---

## What's New Over AEGIS

| Feature | Seeker | AEGIS |
|---------|--------|-------|
| Seeded PRNG (Xoshiro256**) | ✅ Deterministic | ❌ Math.random() |
| UFE Tracking | ✅ Every eval classified | ❌ Just totalEvals |
| Anomaly Detection | ✅ z-score + plateau + shift | ❌ Basic discovery only |
| Convergence Curves | ✅ Full AUCC preserved | ❌ Trimmed away |
| Statistical Comparisons | ✅ Mann-Whitney, Wilcoxon, CI | ❌ None |
| Model Head-to-Head Racing | ✅ N trials × benchmarks | ❌ Single run |
| ELO Leaderboard | ✅ Built-in | ❌ None |
| Real Gradient Descent | ✅ Finite-difference | ❌ Just mutation |
| Quadratic Surrogate (Bayesian) | ✅ Least-squares fit | ❌ Fallback to mutate |
| Annealing Temperature | ✅ Eval-count based | ❌ history.length (breaks on trim) |

---

## UFE Model Comparison

Race models against each other with statistical rigor:

```typescript
import { compareModels } from 'seeker';

const report = await compareModels({
  models: [
    { id: 'aggressive', name: 'High Explore', agentConfig: { explorationRate: 0.7 } },
    { id: 'balanced', name: 'Balanced', agentConfig: { explorationRate: 0.3 } },
    { id: 'greedy', name: 'Low Explore', agentConfig: { explorationRate: 0.1 } },
  ],
  benchmarks: 'all',     // 7 standard functions
  budget: 3000,           // Fixed eval budget per trial
  trials: 10,             // 10 repeated runs per model×benchmark
  rankBy: 'ufe_ratio',   // Rank by useful function evaluation efficiency
  baseSeed: 42,           // Reproducible
});

// report.leaderboard → ELO-ranked models with 95% CI
// report.pairwise → Mann-Whitney + Wilcoxon significance tests
// report.trials → Raw UFE data for every trial
```

---

## UFE Metrics

Every run tracks:

- **UFE Ratio** — what fraction of evaluations were actually useful
- **Convergence Curve** — full (eval_index, best_so_far) history, never trimmed
- **AUCC** — Area Under Convergence Curve (normalized)
- **Time-to-Target** — evals to reach 10%, 50%, 90% of known optimum
- **Anomalies** — z-score outliers, plateaus, landscape shifts

```typescript
const state = await agent.run(knownOptimum);
console.log(state.ufe.ufeRatio);         // 0.34 = 34% of evals were useful
console.log(state.ufe.aucc);             // Lower = faster convergence
console.log(state.ufe.timeToTarget);     // { pct10: 42, pct50: 180, pct90: null }
console.log(state.ufe.convergenceCurve); // [[1, 50.2], [2, 48.1], ...]
```

---

## Deterministic Runs

Every run is reproducible with a seed:

```typescript
// Same seed → same sequence → same results
const a = await optimize(fn, params, { seed: 42 });
const b = await optimize(fn, params, { seed: 42 });
// a.score === b.score  ← guaranteed
```

---

## Anomaly & Discovery Detection

Seeker watches for:

- **Anomalous scores** — >3σ from rolling mean
- **Plateaus** — variance collapse detection
- **Landscape shifts** — distribution mean drift (Cohen's d > 1.5)
- **Major improvements** — >5% relative jump

```typescript
agent.on((event) => {
  if (event.type === 'discovery') {
    console.log(event.discovery.type);        // 'anomaly' | 'plateau' | 'landscape_shift' | 'new_best'
    console.log(event.discovery.description);  // Human-readable
    console.log(event.discovery.confidence);   // 0-1
  }
});
```

---

## Statistical Engine

Built-in hypothesis testing:

```typescript
import { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating } from 'seeker';

const ci = bootstrapCI(scores);                    // 95% confidence interval
const mw = mannWhitneyU(scoresA, scoresB);         // Non-parametric two-sample
const ws = wilcoxonSignedRank(pairedA, pairedB);    // Paired signed-rank
const d = cohensD(scoresA, scoresB);                // Effect size

const elo = new ELORating();
elo.recordMatch('modelA', 'modelB', 1);             // A wins
elo.getLeaderboard();                                // Ranked by ELO
```

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    YOUR TASK                          │
│  evaluate(params) → score                            │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│                  Seeker Agent Core                     │
│                                                       │
│  ┌──────────┐  ┌───────────┐  ┌───────────────────┐  │
│  │ Seeded   │  │ Meta-     │  │ UFE Tracker       │  │
│  │ RNG      │→ │ Learner   │→ │ + Anomaly Detect  │  │
│  │ Xoshiro  │  │ (UCB1)    │  │ + Convergence     │  │
│  └──────────┘  └───────────┘  └───────────────────┘  │
│                                                       │
│  ┌──────────┐  ┌───────────┐  ┌───────────────────┐  │
│  │ Strategy │  │ Phase     │  │ Discovery Engine  │  │
│  │ Engine   │  │ Detector  │  │ + Memory System   │  │
│  │ (10 types)│  │           │  │                   │  │
│  └──────────┘  └───────────┘  └───────────────────┘  │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│               Comparison Engine                       │
│  Model Registry → Head-to-Head Racing → Statistics   │
│  → ELO Leaderboard → Pairwise Significance Tests    │
└──────────────────────────────────────────────────────┘
```

---

## Installation

```bash
cd seeker && npm install && npm run build
```

---

## Run Tests

```bash
npm test
```

---

## Run Benchmarks

```bash
npm run benchmark
```

---

**Built by Danny Lee Eldridge** — Evolved from AEGIS.  
danny@aegis-agent.dev
