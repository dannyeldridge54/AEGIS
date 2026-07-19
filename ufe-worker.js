'use strict';
/**
 * UFE Worker Thread — runs a single optimization task in an isolated thread
 * 
 * Receives: { engineName, taskId, profileConfig, seedData, runSeed, taskDef }
 * Returns:  { taskId, bestParams, bestScore, evals, error? }
 */

const { parentPort, workerData } = require('worker_threads');

// Load engines
const aegis = require('./dist/index.js');
const seeker = require('./seeker/dist/index.js');

// Load shared tasks
const ufeTasks = require('./ufe-tasks');

// Map task IDs to task objects (inline tasks from ufe-tasks + engine tasks)
function getTaskById(taskId) {
  // Inline tasks from ufe-tasks.js
  const inlineTasks = {
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
  };
  if (inlineTasks[taskId]) return inlineTasks[taskId];

  // Engine tasks (from aegis/seeker compiled code)
  const engineTasks = {
    'einstein-cartan': aegis.einsteinCartanTask,
    'ft-gravity': aegis.fTGravityTask,
    'ufe-torsion': aegis.ufeTorsionTask,
    'torsion-wave': aegis.torsionWaveTask,
    'ufe-cross-domain': aegis.crossDomainTask,
  };
  return engineTasks[taskId] || null;
}

// Listen for task messages
parentPort.on('message', async (msg) => {
  const { engineName, taskId, profileConfig, seedData, runSeed } = msg;

  try {
    const task = getTaskById(taskId);
    if (!task) {
      parentPort.postMessage({ taskId, error: `Unknown task: ${taskId}` });
      return;
    }

    const Engine = engineName === 'AEGIS' ? aegis.AegisAgent : seeker.SeekerAgent;
    const agent = new Engine(task, {
      ...profileConfig,
      seed: runSeed,
      verbosity: 'silent',
    });

    // Cross-pollinate if seed data provided
    if (seedData) {
      agent.seed(seedData.params, seedData.score);
    }

    const result = await agent.run(task.optimum);
    const bp = result && result.best ? result.best.params : null;
    const bs = result && result.best ? result.best.score : null;

    parentPort.postMessage({
      taskId,
      bestParams: bp,
      bestScore: isFinite(bs) ? bs : null,
      evals: (result && result.totalEvals) || 0,
    });
  } catch (err) {
    parentPort.postMessage({ taskId, error: err.message });
  }
});
