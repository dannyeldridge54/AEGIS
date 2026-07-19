'use strict';
// ─────────────────────────────────────────────────────────────────────────────
// MCMC ERROR BARS — Metropolis-Hastings around converged solutions
// Produces parameter uncertainties (±) for paper Table I
// ─────────────────────────────────────────────────────────────────────────────
const fs = require('fs');
const ufeTasks = require('./ufe-tasks');

// ── Metropolis-Hastings MCMC ─────────────────────────────────────────────────
function mcmc(evaluate, startParams, paramDefs, { nSteps = 50000, burnIn = 10000, thinBy = 5, stepScale = 0.02 } = {}) {
  const paramNames = paramDefs.map(p => p.name);
  const ranges = {};
  for (const p of paramDefs) ranges[p.name] = p.max - p.min;

  let current = { ...startParams };
  let currentScore = evaluate(current);
  const chain = [];
  let accepted = 0;

  for (let i = 0; i < nSteps; i++) {
    // Propose: Gaussian step in each parameter
    const proposal = { ...current };
    for (const name of paramNames) {
      const step = (Math.random() - 0.5) * 2 * stepScale * ranges[name];
      proposal[name] = Math.max(
        paramDefs.find(p => p.name === name).min,
        Math.min(paramDefs.find(p => p.name === name).max, current[name] + step)
      );
    }

    const proposalScore = evaluate(proposal);

    // Metropolis acceptance: min(1, exp(-Δχ²/2))
    const deltaLogL = -0.5 * (proposalScore - currentScore);
    if (deltaLogL > 0 || Math.random() < Math.exp(deltaLogL)) {
      current = proposal;
      currentScore = proposalScore;
      accepted++;
    }

    // Record after burn-in, with thinning
    if (i >= burnIn && (i - burnIn) % thinBy === 0) {
      chain.push({ ...current, _score: currentScore });
    }
  }

  return { chain, acceptRate: accepted / nSteps };
}

// ── Statistics ───────────────────────────────────────────────────────────────
function chainStats(chain, paramName) {
  const values = chain.map(c => c[paramName]).sort((a, b) => a - b);
  const n = values.length;
  const mean = values.reduce((s, v) => s + v, 0) / n;
  const std = Math.sqrt(values.reduce((s, v) => s + (v - mean) ** 2, 0) / (n - 1));
  const median = values[Math.floor(n / 2)];
  const lo68 = values[Math.floor(n * 0.16)];
  const hi68 = values[Math.floor(n * 0.84)];
  const lo95 = values[Math.floor(n * 0.025)];
  const hi95 = values[Math.floor(n * 0.975)];
  return { mean, std, median, lo68, hi68, lo95, hi95 };
}

// ── Run MCMC for key tasks ───────────────────────────────────────────────────
async function runMCMC() {
  const state = JSON.parse(fs.readFileSync('ufe-state.json', 'utf8'));

  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║   MCMC ERROR BARS — Parameter Uncertainties for Papers     ║');
  console.log('║   Method: Metropolis-Hastings, 50k steps, 10k burn-in     ║');
  console.log('╚══════════════════════════════════════════════════════════════╝\n');

  // Tasks to analyze (must have converged/good solutions)
  const taskMap = {
    'cc-hubble-fit': { task: ufeTasks.cosmicChronTask, label: 'Cosmic Chronometers' },
    'desi-bao-fit': { task: ufeTasks.desiBAOTask, label: 'DESI BAO' },
    'h0-tension': { task: ufeTasks.h0TensionTask, label: 'H₀ Tension Resolver' },
    'rsd-growth': { task: ufeTasks.rsdGrowthTask, label: 'Growth Factor fσ₈' },
    'dark-energy-eos': { task: ufeTasks.wDETask, label: 'Dark Energy EoS' },
  };

  const allResults = {};

  for (const [id, { task, label }] of Object.entries(taskMap)) {
    const best = state.bestKnown && state.bestKnown[id];
    if (!best || !best.params) {
      console.log(`  Skipping ${label}: no converged solution\n`);
      continue;
    }

    console.log(`  ── ${label} (${id}) ──`);
    console.log(`  Starting from best: chi²=${best.score.toFixed(4)}`);

    const t0 = Date.now();
    const { chain, acceptRate } = mcmc(task.evaluate, best.params, task.parameters, {
      nSteps: 50000,
      burnIn: 10000,
      thinBy: 5,
      stepScale: 0.015,
    });
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

    console.log(`  Chain: ${chain.length} samples, acceptance: ${(acceptRate * 100).toFixed(1)}%, ${elapsed}s`);
    console.log('');
    console.log('  ┌─────────────────┬────────────────┬──────────────────────┬──────────────────────┐');
    console.log('  │    Parameter     │   Best Fit     │     68% CI (1σ)      │     95% CI (2σ)      │');
    console.log('  ├─────────────────┼────────────────┼──────────────────────┼──────────────────────┤');

    const taskResults = {};
    for (const p of task.parameters) {
      const s = chainStats(chain, p.name);
      taskResults[p.name] = s;
      const bestVal = best.params[p.name];
      const pm68 = `${s.lo68.toFixed(4)} — ${s.hi68.toFixed(4)}`;
      const pm95 = `${s.lo95.toFixed(4)} — ${s.hi95.toFixed(4)}`;
      console.log(`  │ ${p.name.padEnd(15)} │ ${bestVal.toFixed(6).padStart(14)} │ ${pm68.padStart(20)} │ ${pm95.padStart(20)} │`);
    }
    console.log('  └─────────────────┴────────────────┴──────────────────────┴──────────────────────┘');

    // Print LaTeX-ready ± format
    console.log('  LaTeX:');
    for (const p of task.parameters) {
      const s = taskResults[p.name];
      const bestVal = best.params[p.name];
      const errUp = s.hi68 - bestVal;
      const errDn = bestVal - s.lo68;
      if (Math.abs(errUp - errDn) / Math.max(errUp, errDn, 1e-10) < 0.3) {
        // Symmetric error
        const avg = (errUp + errDn) / 2;
        console.log(`    ${p.name} = ${bestVal.toFixed(4)} \\pm ${avg.toFixed(4)}`);
      } else {
        // Asymmetric error
        console.log(`    ${p.name} = ${bestVal.toFixed(4)}^{+${errUp.toFixed(4)}}_{-${errDn.toFixed(4)}}`);
      }
    }

    allResults[id] = taskResults;
    console.log('');
  }

  // Save chain results
  const outPath = 'mcmc-results.json';
  fs.writeFileSync(outPath, JSON.stringify(allResults, null, 2));
  console.log(`  Results saved to ${outPath}`);
}

runMCMC().catch(e => console.error(e));
