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

/**
 * Run a single optimization with AEGIS engine.
 * @param {Object} options
 * @param {Function} options.objective - Function (params) => number to minimize
 * @param {Array} options.parameters - Parameter definitions [{name, min, max}]
 * @param {number} [options.maxEvals=5000] - Maximum function evaluations
 * @param {number} [options.explorationRate=0.5] - 0=exploit, 1=explore
 * @param {boolean} [options.silent=true] - Suppress console output
 * @returns {Promise<{best: {params, score}, totalEvals, runtime, ufe}>}
 */
async function optimize(options) {
  const {
    objective,
    parameters,
    maxEvals = 5000,
    explorationRate = 0.5,
    silent = true,
    strategies,
    seed,
    onProgress,
  } = options;

  const task = {
    id: options.id || 'custom-task',
    name: options.name || 'Custom Optimization',
    evaluate: objective,
    parameters,
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

  const state = await agent.run(options.optimum);

  return {
    best: state.best ? { params: state.best.params, score: state.best.score } : null,
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
    maxEvals = 3000,
    cycles = 5,
    silent = true,
    onCrossPolinate,
    onProgress,
  } = options;

  const task = {
    id: options.id || 'dual-task',
    name: options.name || 'Dual Optimization',
    evaluate: objective,
    parameters,
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

  return {
    best: overallBest,
    aegisBest,
    seekerBest,
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
  AegisAgent: aegis.AegisAgent,
  createMonitor: aegis.createMonitor,
};
