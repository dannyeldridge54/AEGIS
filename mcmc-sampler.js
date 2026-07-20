'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// MCMC UNCERTAINTY QUANTIFIER
// Metropolis-Hastings sampling around CMA-ES best-fits for proper posteriors,
// Δχ² vs ΛCDM, confidence intervals, and significance calculations.
// ═══════════════════════════════════════════════════════════════════════════════

const fs = require('fs');
const path = require('path');
const ufeTasks = require('./ufe-tasks');

// ── Task registry ────────────────────────────────────────────────────────────
const TASKS = {
  'cc-hubble-fit': ufeTasks.cosmicChronTask,
  'desi-bao-fit': ufeTasks.desiBAOTask,
  'sne-pantheon-fit': ufeTasks.sneTask,
  'h0-tension': ufeTasks.h0TensionTask,
  'rsd-growth': ufeTasks.rsdGrowthTask,
  'energy-conditions': ufeTasks.energyConditionTask,
  's8-tension': ufeTasks.s8TensionTask,
  'dark-energy-eos': ufeTasks.wDETask,
  'combined-multisurvey': ufeTasks.combinedFitTask,
  'model-selection-bic': ufeTasks.modelSelectionTask,
  'ufe-emergence': ufeTasks.emergenceTask,
};

// ── ΛCDM baseline (β=0) for each task ───────────────────────────────────────
function evaluateLCDM(taskId) {
  const task = TASKS[taskId];
  if (!task) return Infinity;
  // Set β=0 (or equivalent) with Planck best-fit for other params
  const lcdmParams = {};
  for (const p of task.parameters) {
    if (p.name === 'beta' || p.name === 'beta0' || p.name === 'beta1' || p.name === 'beta_quantum' || p.name === 'beta_scale') {
      lcdmParams[p.name] = 0;
    } else if (p.name === 'H0') {
      lcdmParams[p.name] = 67.4; // Planck
    } else if (p.name === 'omega_m') {
      lcdmParams[p.name] = 0.315;
    } else if (p.name === 'sigma8') {
      lcdmParams[p.name] = 0.811;
    } else if (p.name === 'rs') {
      lcdmParams[p.name] = 147.09;
    } else if (p.name === 'w0') {
      lcdmParams[p.name] = -1.0;
    } else if (p.name === 'wa') {
      lcdmParams[p.name] = 0.0;
    } else if (p.name === 'gamma') {
      lcdmParams[p.name] = 0.55; // GR growth index
    } else {
      // Use midpoint of allowed range
      lcdmParams[p.name] = (p.min + p.max) / 2;
    }
  }
  return task.evaluate(lcdmParams);
}

// ── Metropolis-Hastings MCMC ─────────────────────────────────────────────────
function runMCMC(taskId, startParams, options = {}) {
  const task = TASKS[taskId];
  if (!task) throw new Error(`Unknown task: ${taskId}`);

  const nSamples = options.nSamples || 50000;
  const burnIn = options.burnIn || 10000;
  const thinning = options.thinning || 5;
  const proposalScale = options.proposalScale || 0.02;

  const paramNames = task.parameters.map(p => p.name);
  const nParams = paramNames.length;

  // Initialize at best-fit
  let current = { ...startParams };
  let currentScore = task.evaluate(current);

  // Proposal widths: fraction of parameter range
  const propWidths = {};
  for (const p of task.parameters) {
    propWidths[p.name] = (p.max - p.min) * proposalScale;
  }

  // Chain storage
  const chain = [];
  let accepted = 0;
  let total = 0;

  console.log(`  MCMC ${taskId}: ${nSamples} samples, burn-in ${burnIn}, thin ${thinning}`);
  console.log(`  Starting χ² = ${currentScore.toFixed(4)}, ${nParams} params`);

  for (let i = 0; i < nSamples + burnIn; i++) {
    // Propose new point (Gaussian random walk)
    const proposal = {};
    for (const p of task.parameters) {
      const noise = (Math.random() + Math.random() + Math.random() +
                     Math.random() + Math.random() + Math.random() - 3) / 3 * propWidths[p.name];
      proposal[p.name] = Math.max(p.min, Math.min(p.max, current[p.name] + noise));
    }

    const proposalScore = task.evaluate(proposal);
    total++;

    // Metropolis acceptance: exp(-Δχ²/2) since score = χ²
    const deltaChiSq = proposalScore - currentScore;
    const acceptProb = Math.exp(-deltaChiSq / 2);

    if (Math.random() < acceptProb) {
      current = proposal;
      currentScore = proposalScore;
      accepted++;
    }

    // Store after burn-in, with thinning
    if (i >= burnIn && (i - burnIn) % thinning === 0) {
      chain.push({ params: { ...current }, score: currentScore });
    }

    // Adaptive proposal scaling every 1000 steps during burn-in
    if (i < burnIn && i > 0 && i % 1000 === 0) {
      const rate = accepted / total;
      if (rate < 0.2) {
        for (const p of task.parameters) propWidths[p.name] *= 0.7;
      } else if (rate > 0.5) {
        for (const p of task.parameters) propWidths[p.name] *= 1.3;
      }
    }
  }

  const acceptRate = accepted / total;
  console.log(`  Acceptance rate: ${(acceptRate * 100).toFixed(1)}%, chain length: ${chain.length}`);

  return { chain, acceptRate, nParams, taskId };
}

// ── Posterior statistics ─────────────────────────────────────────────────────
function computeStats(mcmcResult) {
  const { chain, nParams, taskId } = mcmcResult;
  const task = TASKS[taskId];
  const paramNames = task.parameters.map(p => p.name);

  const stats = {};
  for (const name of paramNames) {
    const values = chain.map(s => s.params[name]).sort((a, b) => a - b);
    const n = values.length;
    const mean = values.reduce((s, v) => s + v, 0) / n;
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / (n - 1);
    const std = Math.sqrt(variance);
    const median = values[Math.floor(n / 2)];
    const lo68 = values[Math.floor(n * 0.16)];
    const hi68 = values[Math.floor(n * 0.84)];
    const lo95 = values[Math.floor(n * 0.025)];
    const hi95 = values[Math.floor(n * 0.975)];

    stats[name] = { mean, std, median, lo68, hi68, lo95, hi95 };
  }

  // χ² statistics
  const scores = chain.map(s => s.score);
  const bestScore = Math.min(...scores);
  const meanScore = scores.reduce((s, v) => s + v, 0) / scores.length;

  // ΛCDM comparison
  const lcdmScore = evaluateLCDM(taskId);
  const deltaChiSq = lcdmScore - bestScore; // positive = UFE better
  const nDataPoints = getDataPointCount(taskId);
  const dof = nDataPoints - nParams;
  const chiSqPerDof = bestScore / Math.max(1, dof);

  // Significance of β ≠ 0 (if β param exists)
  let betaSigma = null;
  const betaParam = paramNames.find(n => n === 'beta' || n === 'beta0');
  if (betaParam && stats[betaParam]) {
    betaSigma = Math.abs(stats[betaParam].mean) / stats[betaParam].std;
  }

  // Δχ² → σ significance (Wilks' theorem, 1 extra param)
  const deltaParams = 1; // β is the extra param vs ΛCDM
  const pValue = deltaChiSq > 0 ? chiSquaredPValue(deltaChiSq, deltaParams) : 1.0;
  const sigmaFromDeltaChi = deltaChiSq > 0 ? pValueToSigma(pValue) : 0;

  return {
    taskId, paramStats: stats, bestScore, meanScore, lcdmScore,
    deltaChiSq, nDataPoints, dof, chiSqPerDof, betaSigma, sigmaFromDeltaChi, pValue
  };
}

// ── Data point counts per task ───────────────────────────────────────────────
function getDataPointCount(taskId) {
  const counts = {
    'cc-hubble-fit': 33,       // 33 CC H(z) measurements
    'desi-bao-fit': 12,        // DESI DR1 BAO data points
    'sne-pantheon-fit': 1701,  // Pantheon+ binned to ~40 effective
    'h0-tension': 33,          // CC data points
    'rsd-growth': 18,          // fσ₈ measurements
    'energy-conditions': 33,   // CC-based
    's8-tension': 18,          // S₈ measurements
    'dark-energy-eos': 33,     // CC + derived
    'combined-multisurvey': 63, // CC + BAO + RSD
    'model-selection-bic': 33,  // CC data
    'ufe-emergence': 63,       // CC + BAO + RSD + SNe
  };
  return counts[taskId] || 33;
}

// ── Chi-squared p-value (Wilson-Hilferty approximation) ──────────────────────
function chiSquaredPValue(x, k) {
  if (x <= 0 || k <= 0) return 1.0;
  // Normal approximation for chi-squared CDF
  const z = Math.pow(x / k, 1/3) - (1 - 2 / (9 * k));
  const denom = Math.sqrt(2 / (9 * k));
  const zNorm = z / denom;
  return 1 - normalCDF(zNorm);
}

function normalCDF(x) {
  const t = 1 / (1 + 0.2316419 * Math.abs(x));
  const d = 0.3989422804014327; // 1/sqrt(2π)
  const p = d * Math.exp(-x * x / 2) *
    (t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))));
  return x > 0 ? 1 - p : p;
}

function pValueToSigma(p) {
  if (p >= 1) return 0;
  if (p <= 0) return 10;
  // Inverse normal CDF approximation (Beasley-Springer-Moro)
  const t = Math.sqrt(-2 * Math.log(p / 2));
  return t - (2.515517 + t * (0.802853 + t * 0.010328)) /
    (1 + t * (1.432788 + t * (0.189269 + t * 0.001308)));
}

// ── Gelman-Rubin convergence diagnostic ──────────────────────────────────────
function gelmanRubin(chains, paramName) {
  const m = chains.length; // number of chains
  const n = chains[0].length; // chain length

  const chainMeans = chains.map(c => {
    const vals = c.map(s => s.params[paramName]);
    return vals.reduce((a, b) => a + b, 0) / vals.length;
  });

  const grandMean = chainMeans.reduce((a, b) => a + b, 0) / m;

  // Between-chain variance
  const B = (n / (m - 1)) * chainMeans.reduce((s, mu) => s + (mu - grandMean) ** 2, 0);

  // Within-chain variance
  const W = chains.reduce((s, c, i) => {
    const vals = c.map(x => x.params[paramName]);
    const mu = chainMeans[i];
    return s + vals.reduce((ss, v) => ss + (v - mu) ** 2, 0) / (n - 1);
  }, 0) / m;

  const varEst = ((n - 1) / n) * W + (1 / n) * B;
  const Rhat = Math.sqrt(varEst / W);
  return Rhat;
}

// ── Main: Run MCMC for all tasks with best-fit starting points ───────────────
async function runFullAnalysis() {
  console.log('╔═══════════════════════════════════════════════════════════════╗');
  console.log('║  MCMC UNCERTAINTY QUANTIFICATION — AEGIS/UFE                 ║');
  console.log('╚═══════════════════════════════════════════════════════════════╝\n');

  // Load best-fit state
  let state;
  try {
    state = JSON.parse(fs.readFileSync(path.join(__dirname, 'ufe-state.json'), 'utf8'));
  } catch (e) {
    console.error('Cannot load ufe-state.json — run optimizer first');
    process.exit(1);
  }

  const results = {};
  const tasksToRun = [
    'cc-hubble-fit', 'desi-bao-fit', 'h0-tension', 'rsd-growth',
    's8-tension', 'dark-energy-eos', 'combined-multisurvey', 'ufe-emergence'
  ];

  for (const taskId of tasksToRun) {
    const bestEntry = state.bestKnown?.[taskId];
    if (!bestEntry || !bestEntry.params) {
      console.log(`⚠️  Skipping ${taskId} — no best-fit params available`);
      continue;
    }

    console.log(`\n━━━ ${taskId.toUpperCase()} ━━━`);

    // Run 2 chains for Gelman-Rubin
    const chains = [];
    for (let c = 0; c < 2; c++) {
      // Slightly perturb start for second chain
      const start = { ...bestEntry.params };
      if (c > 0) {
        const task = TASKS[taskId];
        for (const p of task.parameters) {
          start[p.name] += (Math.random() - 0.5) * (p.max - p.min) * 0.05;
          start[p.name] = Math.max(p.min, Math.min(p.max, start[p.name]));
        }
      }
      const mcmc = runMCMC(taskId, start, {
        nSamples: 30000,
        burnIn: 5000,
        thinning: 3,
        proposalScale: 0.015,
      });
      chains.push(mcmc.chain);
    }

    // Compute stats from combined chains
    const combined = { chain: [...chains[0], ...chains[1]], nParams: TASKS[taskId].parameters.length, taskId };
    const stats = computeStats(combined);
    results[taskId] = stats;

    // Gelman-Rubin for key params
    const task = TASKS[taskId];
    const betaParam = task.parameters.find(p => p.name === 'beta' || p.name === 'beta0' || p.name === 'H0');
    if (betaParam && chains[0].length > 100) {
      const Rhat = gelmanRubin(chains, betaParam.name);
      results[taskId].Rhat = Rhat;
      console.log(`  Gelman-Rubin R̂(${betaParam.name}) = ${Rhat.toFixed(4)} ${Rhat < 1.1 ? '✓' : '⚠️ NOT CONVERGED'}`);
    }

    // Report
    console.log(`  Best χ² = ${stats.bestScore.toFixed(4)}, ΛCDM χ² = ${stats.lcdmScore.toFixed(4)}`);
    console.log(`  Δχ² = ${stats.deltaChiSq.toFixed(2)} (UFE ${stats.deltaChiSq > 0 ? 'better' : 'worse'})`);
    console.log(`  χ²/dof = ${stats.chiSqPerDof.toFixed(3)} (dof = ${stats.dof})`);
    console.log(`  Significance: ${stats.sigmaFromDeltaChi.toFixed(2)}σ (p = ${stats.pValue.toExponential(2)})`);
    if (stats.betaSigma) console.log(`  |β|/σ_β = ${stats.betaSigma.toFixed(2)}σ`);

    // Parameter summary
    for (const [name, s] of Object.entries(stats.paramStats)) {
      if (name.includes('beta') || name === 'H0' || name === 'omega_m') {
        console.log(`    ${name} = ${s.mean.toFixed(4)} ± ${s.std.toFixed(4)} [${s.lo95.toFixed(4)}, ${s.hi95.toFixed(4)}]`);
      }
    }
  }

  // ── Save results ─────────────────────────────────────────────────────────────
  const outputPath = path.join(__dirname, 'mcmc-results.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\n✅ MCMC results saved to ${outputPath}`);

  // ── Summary table ────────────────────────────────────────────────────────────
  console.log('\n╔═══════════════════════════════════════════════════════════════════════════╗');
  console.log('║  SUMMARY: Δχ² vs ΛCDM and Significance                                  ║');
  console.log('╠═══════════════════════════════════════════════════════════════════════════╣');
  console.log('║  Task                  │ χ²_UFE  │ χ²_ΛCDM │  Δχ²  │  σ   │ χ²/dof     ║');
  console.log('╠═══════════════════════════════════════════════════════════════════════════╣');
  for (const [tid, r] of Object.entries(results)) {
    const name = tid.padEnd(22);
    const ufe = r.bestScore.toFixed(2).padStart(7);
    const lcdm = r.lcdmScore.toFixed(2).padStart(7);
    const delta = r.deltaChiSq.toFixed(2).padStart(6);
    const sig = r.sigmaFromDeltaChi.toFixed(1).padStart(4);
    const cdof = r.chiSqPerDof.toFixed(3).padStart(6);
    console.log(`║  ${name} │ ${ufe} │ ${lcdm}  │ ${delta} │ ${sig}σ │ ${cdof}      ║`);
  }
  console.log('╚═══════════════════════════════════════════════════════════════════════════╝');

  return results;
}

// ── Run if called directly ───────────────────────────────────────────────────
if (require.main === module) {
  runFullAnalysis().catch(e => { console.error(e); process.exit(1); });
}

module.exports = { runMCMC, computeStats, evaluateLCDM, runFullAnalysis, TASKS };
