/**
 * AEGIS SDK Demo — General-Purpose Optimization
 *
 * Shows AEGIS solving problems from different industries.
 * No cosmology — pure business optimization.
 */

const { optimize, dualOptimize } = require('../index');

async function main() {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  AEGIS Optimizer SDK — Industry Demo');
  console.log('═══════════════════════════════════════════════════════════\n');

  // ── Demo 1: Supply Chain — Minimize cost while meeting demand ──────────
  console.log('📦 Demo 1: Supply Chain Cost Optimization\n');

  const supplyChain = await optimize({
    name: 'Supply Chain Cost',
    objective: (p) => {
      const productionCost = 50 * p.units_A + 80 * p.units_B;
      const shippingCost = 12 * p.units_A * p.distance_A + 8 * p.units_B * p.distance_B;
      const storageCost = 5 * Math.max(0, p.units_A + p.units_B - p.warehouse_cap);
      // Must meet demand of 1000 units
      const demandPenalty = 1000 * Math.max(0, 1000 - (p.units_A + p.units_B));
      return productionCost + shippingCost + storageCost + demandPenalty;
    },
    parameters: [
      { name: 'units_A', min: 0, max: 1500 },
      { name: 'units_B', min: 0, max: 1500 },
      { name: 'distance_A', min: 1, max: 50 },
      { name: 'distance_B', min: 1, max: 50 },
      { name: 'warehouse_cap', min: 500, max: 2000 },
    ],
    maxEvals: 3000,
  });

  console.log(`  Best cost: $${supplyChain.best.score.toFixed(2)}`);
  console.log(`  Units A: ${supplyChain.best.params.units_A.toFixed(0)}, Units B: ${supplyChain.best.params.units_B.toFixed(0)}`);
  console.log(`  Evaluations: ${supplyChain.totalEvals}, Runtime: ${supplyChain.runtime.toFixed(1)}s\n`);

  // ── Demo 2: Portfolio — Maximize Sharpe ratio ──────────────────────────
  console.log('💰 Demo 2: Portfolio Optimization (Sharpe Ratio)\n');

  const portfolio = await optimize({
    name: 'Portfolio Sharpe Ratio',
    objective: (p) => {
      // Expected returns (annualized %)
      const returns = [0.12, 0.08, 0.15, 0.06];
      const weights = [p.w1, p.w2, p.w3, 1 - p.w1 - p.w2 - p.w3];

      // Weight constraint
      const w4 = weights[3];
      if (w4 < 0 || w4 > 1) return 1e6;

      const portfolioReturn = weights.reduce((s, w, i) => s + w * returns[i], 0);

      // Simplified covariance
      const vols = [0.20, 0.12, 0.25, 0.08];
      const portfolioVol = Math.sqrt(weights.reduce((s, w, i) => s + (w * vols[i]) ** 2, 0));

      const riskFree = 0.04;
      const sharpe = (portfolioReturn - riskFree) / Math.max(portfolioVol, 0.001);

      return -sharpe; // Minimize negative Sharpe = maximize Sharpe
    },
    parameters: [
      { name: 'w1', min: 0, max: 1, description: 'Weight: Tech stocks' },
      { name: 'w2', min: 0, max: 1, description: 'Weight: Bonds' },
      { name: 'w3', min: 0, max: 1, description: 'Weight: Growth stocks' },
    ],
    maxEvals: 3000,
  });

  console.log(`  Best Sharpe ratio: ${(-portfolio.best.score).toFixed(4)}`);
  const w4 = 1 - portfolio.best.params.w1 - portfolio.best.params.w2 - portfolio.best.params.w3;
  console.log(`  Allocation: Tech ${(portfolio.best.params.w1*100).toFixed(1)}% | Bonds ${(portfolio.best.params.w2*100).toFixed(1)}% | Growth ${(portfolio.best.params.w3*100).toFixed(1)}% | Safe ${(w4*100).toFixed(1)}%`);
  console.log(`  Evaluations: ${portfolio.totalEvals}\n`);

  // ── Demo 3: Drug Dosing — Dual Engine with cross-pollination ───────────
  console.log('💊 Demo 3: Drug Dosing Optimization (Dual Engine)\n');

  const dosing = await dualOptimize({
    name: 'Drug Dosing Schedule',
    objective: (p) => {
      // Pharmacokinetic model: maximize efficacy, minimize toxicity
      const peak = p.dose * p.bioavailability;
      const trough = peak * Math.exp(-p.clearance * p.interval);

      // Therapeutic window: 5-15 mg/L
      const overPeak = Math.max(0, peak - 15) ** 2;
      const underTrough = Math.max(0, 5 - trough) ** 2;

      // Minimize total drug exposure (cost + side effects)
      const totalDrug = p.dose * (24 / p.interval);

      return overPeak * 10 + underTrough * 10 + totalDrug * 0.1;
    },
    parameters: [
      { name: 'dose', min: 10, max: 200, description: 'Dose (mg)' },
      { name: 'interval', min: 4, max: 24, description: 'Dosing interval (hours)' },
      { name: 'bioavailability', min: 0.3, max: 1.0, description: 'Oral bioavailability' },
      { name: 'clearance', min: 0.01, max: 0.5, description: 'Drug clearance rate' },
    ],
    maxEvals: 2000,
    cycles: 3,
    onCrossPolinate: (event) => {
      console.log(`  🧬 Cross-pollination! Cycle ${event.cycle}: ${event.from} → ${event.to} (score: ${event.score.toFixed(2)})`);
    },
  });

  console.log(`\n  Best score: ${dosing.best.score.toFixed(4)}`);
  console.log(`  Dose: ${dosing.best.params.dose.toFixed(1)} mg every ${dosing.best.params.interval.toFixed(1)} hours`);
  console.log(`  Cross-pollinations: ${dosing.pollinations}`);
  console.log(`  Total evaluations: ${dosing.totalEvals}\n`);

  console.log('═══════════════════════════════════════════════════════════');
  console.log('  All demos complete. AEGIS handles any domain.');
  console.log('═══════════════════════════════════════════════════════════');
}

main().catch(console.error);
