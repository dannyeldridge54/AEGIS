# AEGIS Optimizer SDK

**Autonomous Dual-Engine Optimization with Cross-Pollination**

Drop in any objective function. Get optimal parameters. Zero configuration.

*Created by Danny Lee Eldridge — Copyright © 2012-2026*

---

## Why AEGIS?

| Feature | AEGIS | scipy.optimize | Optuna | Hyperopt |
|---------|-------|---------------|--------|----------|
| Zero config | ✅ | ❌ | ❌ | ❌ |
| Dual engine | ✅ | ❌ | ❌ | ❌ |
| Cross-pollination | ✅ | ❌ | ❌ | ❌ |
| Live dashboard | ✅ | ❌ | ✅ | ❌ |
| UFE efficiency tracking | ✅ | ❌ | ❌ | ❌ |
| Anomaly detection | ✅ | ❌ | ❌ | ❌ |
| Auto strategy selection | ✅ | ❌ | Partial | ❌ |

## Quick Start

```javascript
const { optimize } = require('@aegis/optimizer');

const result = await optimize({
  objective: (params) => {
    // Your function to minimize — ANY domain
    return (params.x - 3) ** 2 + (params.y + 1) ** 2;
  },
  parameters: [
    { name: 'x', min: -10, max: 10 },
    { name: 'y', min: -10, max: 10 },
  ],
});

console.log(result.best);
// { params: { x: 3.0000, y: -1.0000 }, score: 0.0000 }
```

## Dual Engine (Cross-Pollination)

Two engines attack your problem from opposite ends — one explores wide, one exploits deep. They share discoveries, leapfrogging each other to converge faster than any single optimizer.

```javascript
const { dualOptimize } = require('@aegis/optimizer');

const result = await dualOptimize({
  objective: myExpensiveFunction,
  parameters: myParams,
  cycles: 10,
  onCrossPolinate: (event) => {
    console.log(`🧬 ${event.from} → ${event.to}: ${event.score}`);
  },
});

console.log(`Best: ${result.best.score}`);
console.log(`Cross-pollinations: ${result.pollinations}`);
```

## Live Dashboard

```javascript
const { optimizeWithMonitor } = require('@aegis/optimizer');

const result = await optimizeWithMonitor({
  objective: myFunction,
  parameters: myParams,
  port: 8080,       // Dashboard at http://localhost:8080
  maxEvals: 50000,
});

// Dashboard shows:
// - Real-time convergence curves
// - Strategy effectiveness breakdown
// - UFE efficiency tracking
// - Anomaly detection alerts
// - Best parameters with scores
```

## API Reference

### `optimize(options)`

Single-engine optimization.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `objective` | `Function` | required | `(params) => number` to minimize |
| `parameters` | `Array` | required | `[{name, min, max}]` |
| `maxEvals` | `number` | 5000 | Max function evaluations |
| `explorationRate` | `number` | 0.5 | 0 = pure exploit, 1 = pure explore |
| `strategies` | `string[]` | all | Strategy subset to use |
| `silent` | `boolean` | true | Suppress console output |
| `seed` | `number` | auto | RNG seed for reproducibility |
| `onProgress` | `Function` | null | Progress callback |

**Returns:** `{ best: { params, score }, totalEvals, runtime, ufe }`

### `dualOptimize(options)`

Dual-engine with cross-pollination.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cycles` | `number` | 5 | Full explore/exploit cycles |
| `onCrossPolinate` | `Function` | null | Called when engines share data |

**Returns:** `{ best, aegisBest, seekerBest, totalEvals, pollinations }`

### `optimizeWithMonitor(options)`

Single-engine with live web dashboard.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `port` | `number` | 5555 | Dashboard HTTP port |

**Returns:** `{ best, dashboardUrl, stop() }`

## Available Strategies

| Strategy | Best For |
|----------|----------|
| `random` | Initial exploration, high-dimensional spaces |
| `evolutionary` | Complex landscapes, multiple optima |
| `gradient` | Smooth functions, fine-tuning |
| `annealing` | Escaping local minima |
| `swarm` | Parallel search, rugged landscapes |
| `curiosity` | Novel region discovery |
| `exploit` | Final convergence, surgical precision |

## Industry Applications

- **💊 Pharma** — Drug dosing, molecule design, clinical trial optimization
- **💰 Finance** — Portfolio allocation, risk calibration, pricing models
- **🏭 Manufacturing** — Process parameters, yield optimization, quality control
- **🔋 Energy** — Battery chemistry, grid scheduling, materials screening
- **🛰️ Aerospace** — Trajectory planning, structural optimization
- **🧬 Biotech** — Protein folding parameters, gene expression optimization
- **📊 ML/AI** — Hyperparameter tuning, architecture search, loss function design

## Proven at Scale

AEGIS has been validated on real-world scientific optimization:
- **15 simultaneous physics tasks** running 24/7
- **73+ observational data points** from major astronomical surveys
- **Cross-pollination** delivering 40%+ improvement over single-engine
- **Zero NaN/Infinity** across millions of evaluations
- **Live monitoring** with real-time scoreboard and anomaly detection

## License

Commercial license required for production use. Contact: danny@aegis-optimizer.com

Academic/research use: Free with attribution.

---

*Built by Danny Lee Eldridge | AEGIS — Autonomous Evolving General Intelligence System*
