/**
 * AEGIS Optimizer SDK
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Dual-engine autonomous optimization with cross-pollination.
 * Drop in any objective function. Get optimal parameters. Zero config.
 *
 * @example
 *   const { optimize } = require('@aegis/optimizer');
 *   const result = await optimize({
 *     objective: (params) => (params.x - 3)**2 + (params.y + 1)**2,
 *     parameters: [
 *       { name: 'x', min: -10, max: 10 },
 *       { name: 'y', min: -10, max: 10 },
 *     ],
 *   });
 *   console.log(result.best); // { params: { x: 3, y: -1 }, score: 0 }
 */

const aegis = require('../dist/index.js');

// ── Parameter Processing ─────────────────────────────────────────────────────
// Handles integer, categorical, and conditional parameters by wrapping the
// user's objective with parameter type enforcement.

function processParameters(parameters) {
  const processed = [];
  const integerParams = new Set();
  const categoricalParams = {};  // name -> { values, indexMap }
  const conditionalParams = {};  // name -> { dependsOn, condition }

  for (const param of parameters) {
    if (param.type === 'integer') {
      integerParams.add(param.name);
      processed.push({ name: param.name, min: param.min, max: param.max });
    } else if (param.type === 'categorical') {
      const values = param.values || param.choices;
      categoricalParams[param.name] = { values, indexMap: {} };
      values.forEach((v, i) => { categoricalParams[param.name].indexMap[i] = v; });
      processed.push({ name: param.name, min: 0, max: values.length - 0.001 });
    } else if (param.condition) {
      conditionalParams[param.name] = param.condition;
      processed.push({ name: param.name, min: param.min, max: param.max });
    } else {
      processed.push({ name: param.name, min: param.min, max: param.max });
    }
  }

  // Wrapper that converts optimizer's continuous params to typed params
  function transformParams(rawParams) {
    const transformed = { ...rawParams };
    for (const name of integerParams) {
      if (transformed[name] !== undefined) {
        transformed[name] = Math.round(transformed[name]);
      }
    }
    for (const [name, cat] of Object.entries(categoricalParams)) {
      if (transformed[name] !== undefined) {
        const idx = Math.floor(Math.min(transformed[name], cat.values.length - 1));
        transformed[name] = cat.values[Math.max(0, idx)];
      }
    }
    return transformed;
  }

  return { processed, transformParams, integerParams, categoricalParams, conditionalParams };
}

// ── Constraint Processing ────────────────────────────────────────────────────
// Wraps the objective with constraint penalties so users can write clean
// constraint functions instead of manual penalty hacking.

function wrapWithConstraints(objective, constraints, penaltyScale = 1000) {
  if (!constraints || constraints.length === 0) return objective;

  return (params) => {
    const score = objective(params);
    let penalty = 0;

    for (const constraint of constraints) {
      if (typeof constraint === 'function') {
        // Function constraint: returns 0 if satisfied, positive if violated
        const violation = constraint(params);
        if (violation > 0) penalty += violation * penaltyScale;
      } else if (constraint.type === 'inequality') {
        // { type: 'inequality', fn: (p) => p.x + p.y - 100, direction: '<=' }
        const val = constraint.fn(params);
        if (constraint.direction === '<=' && val > 0) penalty += val * penaltyScale;
        if (constraint.direction === '>=' && val < 0) penalty += (-val) * penaltyScale;
      } else if (constraint.type === 'equality') {
        // { type: 'equality', fn: (p) => p.x + p.y, target: 100, tolerance: 0.01 }
        const val = constraint.fn(params);
        const target = constraint.target || 0;
        const tol = constraint.tolerance || 0.001;
        const err = Math.abs(val - target);
        if (err > tol) penalty += (err - tol) * penaltyScale;
      } else if (constraint.type === 'range') {
        // { type: 'range', param: 'x', min: 0, max: 100 }
        const val = params[constraint.param];
        if (val < constraint.min) penalty += (constraint.min - val) * penaltyScale;
        if (val > constraint.max) penalty += (val - constraint.max) * penaltyScale;
      }
    }

    return score + penalty;
  };
}

// ── Result Export ────────────────────────────────────────────────────────────

function exportResult(result, format = 'json') {
  if (format === 'csv') {
    const lines = ['parameter,value'];
    if (result.best) {
      for (const [k, v] of Object.entries(result.best.params)) {
        lines.push(`${k},${v}`);
      }
      lines.push(`_score,${result.best.score}`);
      lines.push(`_totalEvals,${result.totalEvals || ''}`);
      if (result.ufe) lines.push(`_ufeRatio,${result.ufe.ufeRatio || ''}`);
    }
    return lines.join('\n');
  }

  if (format === 'summary') {
    const lines = [];
    lines.push('═══════════════════════════════════════════');
    lines.push('  AEGIS OPTIMIZER — RESULTS REPORT');
    lines.push('  Generated: ' + new Date().toISOString());
    lines.push('═══════════════════════════════════════════');
    if (result.best) {
      lines.push(`  Best Score: ${result.best.score}`);
      lines.push('  Parameters:');
      for (const [k, v] of Object.entries(result.best.params)) {
        lines.push(`    ${k}: ${typeof v === 'number' ? v.toPrecision(8) : v}`);
      }
    }
    if (result.totalEvals) lines.push(`  Total Evaluations: ${result.totalEvals}`);
    if (result.ufe) {
      lines.push(`  UFE Ratio: ${(result.ufe.ufeRatio * 100).toFixed(1)}%`);
      lines.push(`  Useful Evals: ${result.ufe.usefulEvals}/${result.ufe.totalEvals}`);
    }
    if (result.pollinations) lines.push(`  Cross-Pollinations: ${result.pollinations}`);
    if (result.cycles) lines.push(`  Dual Cycles: ${result.cycles}`);
    lines.push('═══════════════════════════════════════════');
    return lines.join('\n');
  }

  // Default JSON
  return JSON.stringify(result, null, 2);
}

/**
 * Run a single optimization with AEGIS engine.
 * @param {Object} options
 * @param {Function} options.objective - Function (params) => number to minimize
 * @param {Array} options.parameters - Parameter definitions [{name, min, max, type?, values?}]
 * @param {Array} [options.constraints] - Constraint functions or objects
 * @param {number} [options.maxEvals=5000] - Maximum function evaluations
 * @param {number} [options.explorationRate=0.5] - 0=exploit, 1=explore
 * @param {boolean} [options.silent=true] - Suppress console output
 * @param {Object} [options.warmStart] - Previous result to resume from {params, score}
 * @param {Function} [options.onProgress] - Called on improvements: (event) => void
 * @returns {Promise<{best: {params, score}, totalEvals, runtime, ufe}>}
 */
async function optimize(options) {
  const {
    objective,
    parameters,
    constraints,
    maxEvals = 5000,
    explorationRate = 0.5,
    silent = true,
    strategies,
    seed,
    onProgress,
    warmStart,
    penaltyScale,
  } = options;

  // Process parameter types (integer, categorical)
  const { processed, transformParams } = processParameters(parameters);

  // Wrap objective with type transforms + constraints
  let wrappedObjective = (rawParams) => objective(transformParams(rawParams));
  wrappedObjective = wrapWithConstraints(wrappedObjective, constraints, penaltyScale);

  const task = {
    id: options.id || 'custom-task',
    name: options.name || 'Custom Optimization',
    evaluate: wrappedObjective,
    parameters: processed,
  };

  const agent = new aegis.AegisAgent(task, {
    maxEvals,
    explorationRate,
    strategies: strategies || ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'],
    verbosity: silent ? 'silent' : 'normal',
    seed: seed || Date.now(),
  });

  if (onProgress) {
    agent.on((event) => {
      if (event.type === 'improvement' || event.type === 'report') {
        onProgress(event);
      }
    });
  }

  // Warm start: seed from previous run
  if (warmStart && warmStart.params && warmStart.score !== undefined) {
    agent.seed(warmStart.params, warmStart.score);
  }

  const state = await agent.run(options.optimum);

  // Transform params back to typed values
  const best = state.best ? {
    params: transformParams(state.best.params),
    score: state.best.score,
  } : null;

  return {
    best,
    totalEvals: state.totalEvals,
    runtime: state.runtime,
    ufe: state.ufe,
    phase: state.phase,
    discoveries: state.discoveries,
  };
}

/**
 * Run dual-engine optimization with cross-pollination.
 * Two engines attack the problem from opposite ends of the explore/exploit
 * spectrum, sharing discoveries to converge faster.
 *
 * @param {Object} options - Same as optimize() plus:
 * @param {number} [options.cycles=5] - Number of full cycles
 * @param {Function} [options.onCrossPolinate] - Called when engines share data
 * @returns {Promise<{best, aegisBest, seekerBest, totalEvals, pollinations}>}
 */
async function dualOptimize(options) {
  const seeker = require('../seeker/dist/index.js');

  const {
    objective,
    parameters,
    constraints,
    maxEvals = 3000,
    cycles = 5,
    silent = true,
    onCrossPolinate,
    onProgress,
    warmStart,
    penaltyScale,
  } = options;

  // Process parameter types
  const { processed, transformParams } = processParameters(parameters);

  // Wrap with constraints
  let wrappedObjective = (rawParams) => objective(transformParams(rawParams));
  wrappedObjective = wrapWithConstraints(wrappedObjective, constraints, penaltyScale);

  const task = {
    id: options.id || 'dual-task',
    name: options.name || 'Dual Optimization',
    evaluate: wrappedObjective,
    parameters: processed,
  };

  // Exploration/exploitation spectrum
  const profiles = [
    { tag: 'explore', config: { maxEvals, explorationRate: 0.85, strategies: ['random', 'curiosity', 'swarm'] } },
    { tag: 'balanced', config: { maxEvals, explorationRate: 0.50, strategies: ['evolutionary', 'annealing', 'gradient'] } },
    { tag: 'exploit', config: { maxEvals, explorationRate: 0.15, strategies: ['gradient', 'exploit', 'annealing'] } },
  ];

  let aegisBest = null;
  let seekerBest = null;
  let totalEvals = 0;
  let pollinations = 0;

  // Warm start both engines if provided
  if (warmStart && warmStart.params) {
    aegisBest = { params: { ...warmStart.params }, score: warmStart.score };
    seekerBest = { params: { ...warmStart.params }, score: warmStart.score };
  }

  for (let cycle = 0; cycle < cycles; cycle++) {
    for (const profile of profiles) {
      // AEGIS: explore first
      const aegisAgent = new aegis.AegisAgent(task, {
        ...profile.config,
        verbosity: silent ? 'silent' : 'normal',
        seed: (cycle * 100 + totalEvals) * 1000 + Date.now() % 10000,
      });
      // Seed from Seeker's best
      if (seekerBest) aegisAgent.seed(seekerBest.params, seekerBest.score);

      if (onProgress) aegisAgent.on(onProgress);
      const aegisResult = await aegisAgent.run();
      totalEvals += aegisResult.totalEvals;

      if (aegisResult.best && (!aegisBest || aegisResult.best.score < aegisBest.score)) {
        aegisBest = { params: { ...aegisResult.best.params }, score: aegisResult.best.score };
      }

      // Seeker: exploit first (reversed profiles)
      const reverseIdx = profiles.length - 1 - profiles.indexOf(profile);
      const seekerProfile = profiles[reverseIdx];
      const seekerAgent = new seeker.SeekerAgent(task, {
        ...seekerProfile.config,
        verbosity: silent ? 'silent' : 'normal',
        seed: (cycle * 200 + totalEvals) * 2000 + Date.now() % 10000,
      });
      // Seed from AEGIS's best
      if (aegisBest) seekerAgent.seed(aegisBest.params, aegisBest.score);

      if (onProgress) seekerAgent.on(onProgress);
      const seekerResult = await seekerAgent.run();
      totalEvals += seekerResult.totalEvals;

      const prevBest = seekerBest ? seekerBest.score : Infinity;
      if (seekerResult.best && (!seekerBest || seekerResult.best.score < seekerBest.score)) {
        seekerBest = { params: { ...seekerResult.best.params }, score: seekerResult.best.score };
        if (seekerBest.score < prevBest && aegisBest) {
          pollinations++;
          if (onCrossPolinate) onCrossPolinate({ cycle, from: 'AEGIS', to: 'Seeker', score: seekerBest.score });
        }
      }
    }
  }

  const overallBest = (!aegisBest && !seekerBest) ? null
    : (!seekerBest || (aegisBest && aegisBest.score <= seekerBest.score)) ? aegisBest
    : seekerBest;

  // Transform params back to typed values
  const transformedBest = overallBest ? { params: transformParams(overallBest.params), score: overallBest.score } : null;

  return {
    best: transformedBest,
    aegisBest: aegisBest ? { params: transformParams(aegisBest.params), score: aegisBest.score } : null,
    seekerBest: seekerBest ? { params: transformParams(seekerBest.params), score: seekerBest.score } : null,
    totalEvals,
    pollinations,
    cycles,
  };
}

/**
 * Create a live-monitored optimization with web dashboard.
 * @param {Object} options - Same as optimize() plus:
 * @param {number} [options.port=5555] - Dashboard port
 * @returns {Promise<result>} - Also starts http://localhost:{port}
 */
async function optimizeWithMonitor(options) {
  const monitor = aegis.createMonitor({ port: options.port || 5555 });
  monitor.startDashboard();

  const task = {
    id: options.id || 'monitored-task',
    name: options.name || 'Monitored Optimization',
    evaluate: options.objective,
    parameters: options.parameters,
  };

  const agent = new aegis.AegisAgent(task, {
    maxEvals: options.maxEvals || 10000,
    explorationRate: options.explorationRate || 0.5,
    strategies: options.strategies || ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'],
    verbosity: 'silent',
    seed: options.seed || Date.now(),
  });

  const runId = `run-${Date.now()}`;
  monitor.registerRun(runId, task.name);
  agent.on(monitor.createHandler(runId));

  const state = await agent.run(options.optimum);

  return {
    best: state.best ? { params: state.best.params, score: state.best.score } : null,
    totalEvals: state.totalEvals,
    runtime: state.runtime,
    ufe: state.ufe,
    dashboardUrl: `http://localhost:${options.port || 5555}`,
    stop: () => monitor.stopDashboard(),
  };
}

module.exports = {
  optimize,
  dualOptimize,
  optimizeWithMonitor,
  exportResult,
  AegisAgent: aegis.AegisAgent,
  createMonitor: aegis.createMonitor,
};
