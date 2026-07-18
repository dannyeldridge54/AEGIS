# AEGIS Optimizer — Industry Playbook
## How to Get Maximum Value in Your Market Sector

*Copyright © 2012-2026 Danny Lee Eldridge. All rights reserved.*

---

## Table of Contents

1. [Key Concepts](#key-concepts)
2. [Finance & Trading](#finance--trading)
3. [Pharmaceutical & Biotech](#pharmaceutical--biotech)
4. [Manufacturing & Supply Chain](#manufacturing--supply-chain)
5. [Energy & Utilities](#energy--utilities)
6. [Aerospace & Defense](#aerospace--defense)
7. [AI / Machine Learning](#ai--machine-learning)
8. [Telecommunications](#telecommunications)
9. [Real Estate & Construction](#real-estate--construction)
10. [Agriculture & Food](#agriculture--food)
11. [Healthcare Operations](#healthcare-operations)
12. [Best Practices](#best-practices)

---

## Key Concepts

### Glossary — Terms Across All Sectors

| Term | What It Means | Why It Matters |
|------|--------------|----------------|
| **Objective Function** | The thing you want to minimize (cost, error, waste, risk). You write this. | AEGIS needs exactly one function that takes parameters and returns a number. Lower = better. |
| **Parameters** | The knobs you can turn (price, dosage, allocation, temperature). Each has a min and max. | Define what AEGIS is allowed to adjust. More parameters = harder problem = use dual engine. |
| **Score** | The output of your objective function. AEGIS drives this toward zero. | Track this — when it stops dropping, you've converged. |
| **Dual Engine** | AEGIS (explorer) + Seeker (refiner) running simultaneously. | Use for problems with 5+ parameters or multiple local optima. 40-100% better than single. |
| **Cross-Pollination** | Engines share their best discoveries. When one finds something good, the other refines it. | This is the secret sauce. No other optimizer does this. |
| **UFE Ratio** | "Useful Function Evaluations" — what % of tries actually improved the score. | Higher = more efficient. AEGIS auto-tunes strategies to maximize this. |
| **Convergence** | When the score stops improving significantly. | Your answer is ready. Check `result.best.params`. |
| **Strategy** | How AEGIS searches: random, evolutionary, gradient, annealing, swarm, curiosity, exploit. | You don't pick these — AEGIS auto-balances based on what's working. |
| **Anomaly** | An unusual parameter combination that produces unexpectedly good or bad results. | These often reveal hidden structure in your problem. Check the dashboard. |

### The Universal Pattern

Every optimization problem follows the same template:

```javascript
const result = await optimize({
  objective: (params) => {
    // 1. Use params to compute your business metric
    // 2. Return a single number (lower = better)
    return cost + penalty + risk;  // combine multiple objectives
  },
  parameters: [
    { name: 'knob1', min: lower_bound, max: upper_bound },
    { name: 'knob2', min: lower_bound, max: upper_bound },
    // ... as many as you need
  ],
});
```

---

## Finance & Trading

### What to Optimize
- **Portfolio allocation** — minimize risk for target return (Markowitz)
- **Trading strategy params** — lookback windows, thresholds, position sizes
- **Risk model calibration** — VaR/CVaR parameters against historical data
- **Option pricing** — implied volatility surface fitting
- **Algorithmic trading** — entry/exit signals, stop-loss levels

### Example: Portfolio Optimization

```javascript
const { dualOptimize } = require('@aegis/optimizer');

// Historical returns data (load from your data source)
const returns = loadDailyReturns(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']);

const result = await dualOptimize({
  objective: (weights) => {
    const w = Object.values(weights);
    const totalWeight = w.reduce((s, v) => s + Math.abs(v), 0);

    // Normalize weights
    const norm = w.map(v => Math.abs(v) / totalWeight);

    // Portfolio return (negative because we maximize)
    const portReturn = norm.reduce((s, wi, i) =>
      s + wi * mean(returns[i]), 0);

    // Portfolio risk (variance)
    const portVariance = computePortfolioVariance(norm, returns);

    // Sharpe ratio (negative = we want to maximize)
    const sharpe = portReturn / Math.sqrt(portVariance);

    return -sharpe;  // minimize negative Sharpe = maximize Sharpe
  },
  parameters: [
    { name: 'AAPL', min: 0, max: 0.4 },
    { name: 'GOOGL', min: 0, max: 0.4 },
    { name: 'MSFT', min: 0, max: 0.4 },
    { name: 'AMZN', min: 0, max: 0.4 },
    { name: 'TSLA', min: 0, max: 0.2 },  // cap volatile stock
  ],
  maxEvals: 5000,
  cycles: 10,
});

console.log('Optimal Sharpe:', -result.best.score);
console.log('Weights:', result.best.params);
```

### Pro Tips for Finance
- **Use `dualOptimize`** — financial landscapes have many local optima
- **Cap parameter ranges** — prevents unrealistic allocations
- **Add penalty terms** — for leverage limits, sector concentration, etc.
- **Run daily** — market conditions change; re-optimize regularly
- **UFE > 50%** means your objective function is well-structured

---

## Pharmaceutical & Biotech

### What to Optimize
- **Drug dosing regimens** — efficacy vs. toxicity tradeoff
- **Molecular design** — binding affinity, solubility, ADMET properties
- **Clinical trial design** — sample size, arm ratios, adaptive thresholds
- **Process development** — fermentation conditions, yield optimization
- **Formulation** — excipient ratios, release profiles

### Example: Drug Dosing Optimization

```javascript
const result = await dualOptimize({
  objective: (p) => {
    // PK/PD model — drug concentration over time
    const Cmax = p.dose * p.bioavailability / p.volume;
    const halfLife = 0.693 / p.clearance;
    const steadyState = Cmax / (1 - Math.exp(-p.clearance * p.interval));

    // Efficacy: want concentration in therapeutic window
    const efficacy = steadyState > p.MEC ? 0 : (p.MEC - steadyState) * 10;

    // Toxicity: penalty for exceeding toxic threshold
    const toxicity = steadyState > p.MTC ? (steadyState - p.MTC) * 100 : 0;

    // Convenience: prefer once-daily dosing
    const convenience = Math.abs(p.interval - 24) * 0.5;

    return efficacy + toxicity + convenience;
  },
  parameters: [
    { name: 'dose', min: 10, max: 500 },          // mg
    { name: 'interval', min: 4, max: 48 },         // hours
    { name: 'bioavailability', min: 0.1, max: 1 }, // fraction
    { name: 'volume', min: 10, max: 100 },          // liters
    { name: 'clearance', min: 0.01, max: 0.5 },    // L/hr
    { name: 'MEC', min: 1, max: 20 },              // μg/mL (min effective)
    { name: 'MTC', min: 10, max: 100 },            // μg/mL (max tolerated)
  ],
  maxEvals: 10000,
  cycles: 15,
});
```

### Pro Tips for Pharma
- **Always include safety constraints** as heavy penalty terms
- **Use dual engine** — dose-response surfaces are highly nonlinear
- **Log-scale parameters** for concentrations and clearance rates
- **Validate with known drugs** — run AEGIS on a drug with known optimal dosing
- **Export results** for regulatory documentation

---

## Manufacturing & Supply Chain

### What to Optimize
- **Production scheduling** — minimize makespan, changeovers, idle time
- **Inventory levels** — balance holding costs vs. stockout risk
- **Quality control** — process parameters for minimal defect rate
- **Routing & logistics** — vehicle routes, warehouse placement
- **Workforce allocation** — shift patterns, skill matching

### Example: Production Line Optimization

```javascript
const result = await dualOptimize({
  objective: (p) => {
    const throughput = p.speed * p.uptime * (1 - p.defectRate);
    const energyCost = p.speed * p.temperature * 0.12;  // $/hr
    const laborCost = p.workers * 45;  // $/hr
    const wasteCost = throughput * p.defectRate * p.materialCost;
    const maintenanceCost = p.speed > 80 ? (p.speed - 80) * 5 : 0;

    // We want to maximize profit (minimize negative profit)
    const revenue = throughput * p.unitPrice;
    const totalCost = energyCost + laborCost + wasteCost + maintenanceCost;
    const profit = revenue - totalCost;

    return -profit;  // minimize negative profit = maximize profit
  },
  parameters: [
    { name: 'speed', min: 10, max: 100 },        // units/hr
    { name: 'temperature', min: 150, max: 400 },  // °C
    { name: 'workers', min: 2, max: 20 },
    { name: 'uptime', min: 0.7, max: 0.99 },
    { name: 'defectRate', min: 0.001, max: 0.1 },
    { name: 'materialCost', min: 5, max: 50 },
    { name: 'unitPrice', min: 20, max: 200 },
  ],
  maxEvals: 5000,
  cycles: 10,
});

console.log('Max daily profit:', -result.best.score * 24);
```

### Pro Tips for Manufacturing
- **Include maintenance penalties** for extreme operating conditions
- **Model changeover costs** between product variants
- **Run per-shift** — conditions change between shifts
- **Use anomaly detection** to find unexpected sweet spots

---

## Energy & Utilities

### What to Optimize
- **Grid dispatch** — minimize generation cost meeting demand
- **Renewable placement** — solar/wind farm layout for max output
- **Battery storage** — charge/discharge schedules
- **Building HVAC** — comfort vs. energy cost
- **Pipeline routing** — pressure, flow, maintenance scheduling

### Example: Solar + Battery Dispatch

```javascript
const result = await dualOptimize({
  objective: (p) => {
    let totalCost = 0;
    for (let hour = 0; hour < 24; hour++) {
      const solarOutput = p.panelCapacity * solarIrradiance[hour];
      const demand = loadProfile[hour];
      const gap = demand - solarOutput;

      if (gap > 0) {
        // Need power: discharge battery or buy from grid
        const batteryDraw = Math.min(gap, p.batteryCapacity * p.maxDischarge);
        const gridBuy = gap - batteryDraw;
        totalCost += gridBuy * gridPrice[hour];
      } else {
        // Excess solar: charge battery or sell to grid
        const excess = -gap;
        const charge = Math.min(excess, p.batteryCapacity * p.maxCharge);
        const sell = excess - charge;
        totalCost -= sell * feedInTariff;
      }
    }
    // Add capital costs (amortized daily)
    totalCost += p.panelCapacity * 0.15;      // panel cost/day
    totalCost += p.batteryCapacity * 0.25;    // battery cost/day
    return totalCost;
  },
  parameters: [
    { name: 'panelCapacity', min: 5, max: 100 },     // kW
    { name: 'batteryCapacity', min: 5, max: 200 },   // kWh
    { name: 'maxCharge', min: 0.1, max: 1.0 },       // C-rate
    { name: 'maxDischarge', min: 0.1, max: 1.0 },
  ],
  maxEvals: 3000,
  cycles: 8,
});
```

---

## Aerospace & Defense

### What to Optimize
- **Trajectory planning** — fuel-optimal orbits, reentry paths
- **Structural design** — weight vs. strength tradeoffs
- **Sensor placement** — coverage maximization
- **Mission planning** — resource allocation across objectives
- **Control system tuning** — PID/MPC gains

### Example: Satellite Orbit Optimization

```javascript
const result = await dualOptimize({
  objective: (p) => {
    // Hohmann transfer deltaV
    const r1 = 6371 + p.parkingAlt;  // km
    const r2 = 6371 + p.targetAlt;
    const mu = 398600.4;  // km³/s² (Earth)

    const v1 = Math.sqrt(mu / r1);
    const vt1 = Math.sqrt(mu * (2/r1 - 2/(r1+r2)));
    const dv1 = Math.abs(vt1 - v1);

    const v2 = Math.sqrt(mu / r2);
    const vt2 = Math.sqrt(mu * (2/r2 - 2/(r1+r2)));
    const dv2 = Math.abs(v2 - vt2);

    const totalDV = dv1 + dv2 + p.planeChange * 0.1;

    // Coverage: higher orbit = more coverage but more fuel
    const coverage = Math.min(1, (p.targetAlt / 36000));

    return totalDV - coverage * 2;  // balance fuel vs. coverage
  },
  parameters: [
    { name: 'parkingAlt', min: 200, max: 2000 },
    { name: 'targetAlt', min: 400, max: 36000 },
    { name: 'planeChange', min: 0, max: 28.5 },    // degrees
  ],
});
```

---

## AI / Machine Learning

### What to Optimize
- **Hyperparameter tuning** — learning rate, batch size, architecture choices
- **Neural architecture search** — layer sizes, activation functions
- **Feature selection** — which features maximize model performance
- **Training schedules** — warmup, decay, curriculum learning
- **Ensemble weights** — how to combine multiple models

### Example: Neural Network Hyperparameter Tuning

```javascript
const result = await dualOptimize({
  objective: (p) => {
    // Train your model with these hyperparameters
    const model = trainModel({
      learningRate: 10 ** p.logLR,       // log scale
      batchSize: Math.round(2 ** p.logBatch),
      hiddenSize: Math.round(p.hiddenSize),
      dropout: p.dropout,
      weightDecay: 10 ** p.logWD,
      epochs: Math.round(p.epochs),
    });

    // Return validation loss (lower = better)
    return model.validationLoss;
  },
  parameters: [
    { name: 'logLR', min: -5, max: -1 },        // 1e-5 to 0.1
    { name: 'logBatch', min: 3, max: 10 },       // 8 to 1024
    { name: 'hiddenSize', min: 32, max: 1024 },
    { name: 'dropout', min: 0, max: 0.5 },
    { name: 'logWD', min: -6, max: -2 },         // 1e-6 to 0.01
    { name: 'epochs', min: 5, max: 100 },
  ],
  maxEvals: 200,   // each eval trains a model — expensive!
  cycles: 5,
});
```

### Pro Tips for ML
- **Use log-scale** for learning rates and weight decay
- **Limit maxEvals** — each evaluation trains a model
- **Single engine is fine** for < 5 hyperparameters
- **Dual engine** shines when tuning architecture + training schedule together

---

## Telecommunications

### What to Optimize
- **Network planning** — tower placement, frequency allocation
- **QoS routing** — latency/bandwidth tradeoffs
- **Capacity planning** — when/where to add infrastructure
- **Pricing** — rate plan optimization for revenue + retention

---

## Real Estate & Construction

### What to Optimize
- **Building design** — energy efficiency vs. construction cost
- **Project scheduling** — resource leveling, critical path
- **Land use** — zoning allocation for maximum value
- **HVAC sizing** — comfort vs. capital + operating cost

---

## Agriculture & Food

### What to Optimize
- **Crop planning** — what to plant where for maximum yield/profit
- **Irrigation scheduling** — water efficiency
- **Fertilizer blending** — nutrient ratios vs. cost
- **Supply chain** — harvest timing, storage, distribution

---

## Healthcare Operations

### What to Optimize
- **Staff scheduling** — coverage vs. overtime costs
- **Patient flow** — ED throughput, bed allocation
- **Resource allocation** — equipment placement, inventory
- **Appointment scheduling** — wait time minimization

---

## Best Practices

### 1. Start Simple
Begin with 2-3 parameters. Verify the optimizer finds the expected answer. Then add complexity.

### 2. Choose Your Engine
| Situation | Engine | Why |
|-----------|--------|-----|
| < 5 parameters, smooth | Single (`optimize`) | Fast, sufficient |
| 5-10 parameters | Dual (`dualOptimize`) | Cross-pollination helps |
| 10+ parameters | Dual + high evals | Need both exploration and refinement |
| Multiple local optima | Dual | Two engines escape traps better |
| Expensive evaluations | Single, low evals | Don't waste compute |

### 3. Structure Your Objective
```javascript
// Good: smooth, well-scaled
objective: (p) => {
  const cost = computeCost(p);
  const penalty = violatesConstraint(p) ? 1000 : 0;
  return cost + penalty;
}

// Better: graduated penalties
objective: (p) => {
  const cost = computeCost(p);
  const overBudget = Math.max(0, cost - budget);
  return cost + overBudget * 10;  // soft penalty, not cliff
}
```

### 4. Use Graduated Penalties (Not Hard Walls)
Instead of returning `Infinity` for constraint violations, add a penalty proportional to how far you are from feasibility. This gives the optimizer a gradient to follow.

### 5. Scale Your Parameters
If one parameter ranges 0-1 and another ranges 0-1000000, AEGIS handles it — but you'll converge faster if ranges are similar magnitudes. Consider normalizing.

### 6. Monitor the Dashboard
The live dashboard shows:
- **Convergence curve** — is the score still dropping?
- **Strategy effectiveness** — which strategies are finding improvements?
- **UFE ratio** — if low (< 30%), your problem may need restructuring
- **Anomalies** — unexpected good results often reveal hidden opportunities

### 7. Export and Act
```javascript
// Save results
const fs = require('fs');
fs.writeFileSync('optimal-params.json', JSON.stringify(result.best, null, 2));

// Use in production
const { params } = result.best;
setProductionParameters(params);
```

---

## Support & Licensing

| Tier | Price | Evals/Day | Engine | Support |
|------|-------|-----------|--------|---------|
| Free | $0 | 100 | Single | Community |
| Starter | $99/mo | 10,000 | Single | Email |
| Pro | $499/mo | 100,000 | Dual + Cross-Pollination | Priority |
| Enterprise | Custom | Unlimited | On-premise | Dedicated + SLA |

**Contact:** danny@aegis-optimizer.com
**GitHub:** https://github.com/dannyeldridge54/AEGIS
