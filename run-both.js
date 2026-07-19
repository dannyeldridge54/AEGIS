/**
 * AEGIS + Seeker — 24/7 Dual Pincer Runner
 *
 * AEGIS starts from the EXPLORATION end of the spectrum:
 *   wide ranges → high dimensionality → curiosity-driven → random
 *   ...and progressively tightens toward exploitation.
 *
 * Seeker starts from the EXPLOITATION end:
 *   narrow focus → low dimensionality → gradient/bayesian → surgical
 *   ...and progressively opens toward exploration.
 *
 * They meet in the middle. Every configuration gets covered.
 * Each full cycle reverses direction — AEGIS/Seeker swap ends.
 *
 * AEGIS Monitor: http://localhost:5555
 * Seeker Monitor: http://localhost:5556
 */

const aegis = require('./dist/index.js');
const seeker = require('./seeker/dist/index.js');
const { Worker } = require('worker_threads');
const os = require('os');

// Import shared tasks module (used by both main thread and workers)
const ufeTasks = require('./ufe-tasks');
const gpu = require('./gpu-accel');
const {
  torsionHubble, torsionHubbleEvolving, comovingDistance, comovingDistanceEvolving,
  growthFactor, CC_DATA, RS_PLANCK, C_LIGHT,
  cosmicChronTask, desiBAOTask, sneTask, h0TensionTask,
  rsdGrowthTask, energyConditionTask, s8TensionTask,
  wDETask, combinedFitTask, modelSelectionTask,
} = ufeTasks;

// Worker pool size — use physical cores minus 2 (leave headroom)
const WORKER_COUNT = Math.max(2, Math.min(os.cpus().length - 2, 12));
console.log(`🧵 Worker pool: ${WORKER_COUNT} threads (${os.cpus().length} logical CPUs)`);

// ═══════════════════════════════════════════════════════════════════════════════
// THE SPECTRUM — ordered from pure exploration (index 0) to pure exploitation
// ═══════════════════════════════════════════════════════════════════════════════

// ── Speed Controls (adjustable via env vars OR runtime API on :5557) ─────────
// Usage: EVAL_SCALE=2 node run-both.js      (double all eval budgets)
//        EVAL_SCALE=0.5 node run-both.js    (halve all — faster cycles)
//        DELAY_MS=0 node run-both.js        (zero delay between tasks)
let EVAL_SCALE = parseFloat(process.env.EVAL_SCALE || '1');
let DELAY_MS = parseInt(process.env.DELAY_MS || '50');
const CONTROL_PORT = parseInt(process.env.CONTROL_PORT || '5557');
console.log(`⚙️  Speed: EVAL_SCALE=${EVAL_SCALE}x  DELAY_MS=${DELAY_MS}ms  Control: http://localhost:${CONTROL_PORT}`);

// Base eval budgets (before EVAL_SCALE multiplier)
const BASE_EVALS = [800, 1200, 1000, 1000, 1000, 1000, 2000, 1200, 1000, 1500, 2000];

const spectrum = [
  { tag: 'chaos-scan',       baseIdx: 0,  config: { explorationRate: 0.95, strategies: ['random', 'curiosity'] } },
  { tag: 'wide-swarm',       baseIdx: 1,  config: { explorationRate: 0.85, strategies: ['swarm', 'curiosity', 'random'] } },
  { tag: 'evo-explore',      baseIdx: 2,  config: { explorationRate: 0.75, strategies: ['evolutionary', 'swarm', 'curiosity', 'random'] } },
  { tag: 'diverse-mix',      baseIdx: 3,  config: { explorationRate: 0.65, strategies: ['evolutionary', 'swarm', 'random', 'annealing'] } },
  { tag: 'annealing-hot',    baseIdx: 4,  config: { explorationRate: 0.60, strategies: ['annealing', 'swarm', 'curiosity'] } },
  { tag: 'balanced',         baseIdx: 5,  config: { explorationRate: 0.50 } },
  { tag: 'full-suite-deep',  baseIdx: 6,  config: { explorationRate: 0.50 } },
  { tag: 'bayesian-refine',  baseIdx: 7,  config: { explorationRate: 0.35, strategies: ['bayesian', 'gradient', 'annealing', 'exploit'] } },
  { tag: 'gradient-anneal',  baseIdx: 8,  config: { explorationRate: 0.25, strategies: ['gradient', 'annealing', 'exploit'] } },
  { tag: 'surgical-exploit', baseIdx: 9,  config: { explorationRate: 0.10, strategies: ['gradient', 'bayesian', 'exploit'] } },
  { tag: 'pure-refine',      baseIdx: 10, config: { explorationRate: 0.05, strategies: ['gradient', 'exploit'] } },
];

// Dynamic config getter — applies current EVAL_SCALE and adaptive task multiplier
function getProfileConfig(profile, taskId) {
  const taskMult = taskId ? getTaskMultiplier(taskId) : 1.0;
  return { ...profile.config, maxEvals: Math.round(BASE_EVALS[profile.baseIdx] * EVAL_SCALE * taskMult) };
}

const SPECTRUM_LEN = spectrum.length;

// ═══════════════════════════════════════════════════════════════════════════════
// PHYSICS TASKS — imported from ufe-tasks.js (shared with worker threads)
// ═══════════════════════════════════════════════════════════════════════════════
// 10 observational tasks + 5 torsion field theory = 15 unique physics domains
// Each appears at multiple spectrum tiers for full exploration/exploitation
// ═══════════════════════════════════════════════════════════════════════════════

const tasksByDifficulty = [
  // ── Tier 1: Small parameter spaces (2-3 params) ───────────────────────────
  energyConditionTask,                                // 2 params — viability
  aegis.einsteinCartanTask,                           // EC torsion — 8 params
  s8TensionTask,                                      // 3 params — S₈ tension
  aegis.fTGravityTask,                                // f(T) — 5 params

  // ── Tier 2: Medium (3-5 params) ───────────────────────────────────────────
  cosmicChronTask,                                    // CC H(z) — 3 params
  aegis.ufeTorsionTask,                               // UFE Mexican hat — 8 params
  rsdGrowthTask,                                      // fσ₈ growth — 4 params
  aegis.torsionWaveTask,                              // Wave — 7 params
  desiBAOTask,                                        // DESI BAO — 4 params
  aegis.crossDomainTask,                              // Cross-domain — 10 params

  // ── Tier 3: Hard (4-6 params, joint fits) ─────────────────────────────────
  sneTask,                                            // Pantheon+ SNe — 4 params
  aegis.einsteinCartanTask,                           // EC again — exploitation profile
  h0TensionTask,                                      // H₀ tension — 4 params
  aegis.fTGravityTask,                                // f(T) again
  modelSelectionTask,                                 // ΔBIC — 4 params
  aegis.ufeTorsionTask,                               // UFE again

  // ── Tier 4: Extreme (5-6 params, combined fits) ───────────────────────────
  wDETask,                                            // w₀wₐCDM + torsion — 6 params
  aegis.crossDomainTask,                              // Cross-domain again
  combinedFitTask,                                    // FULL multi-survey — 5 params
  aegis.torsionWaveTask,                              // Wave again
  combinedFitTask,                                    // Combined again — max budget
  aegis.crossDomainTask,                              // Cross-domain — max budget

  // ── Tier 5: Critical repeat — highest budget profiles ─────────────────────
  h0TensionTask,                                      // H₀ tension — max exploitation
  aegis.ufeTorsionTask,                               // UFE — max exploitation
  modelSelectionTask,                                 // Model selection — final
  combinedFitTask,                                    // Combined — final pass
];

const TASK_COUNT = tasksByDifficulty.length;

// ═══════════════════════════════════════════════════════════════════════════════
// PINCER SCHEDULER
//
// AEGIS sweeps exploration → exploitation on easy → hard tasks
// Seeker sweeps exploitation → exploration on hard → easy tasks
// They meet in the middle. Each cycle they swap direction.
// ═══════════════════════════════════════════════════════════════════════════════

function buildPincerQueue(startFromExploration) {
  const queue = [];

  if (startFromExploration) {
    // Pair easy tasks with exploration, hard tasks with exploitation
    for (let t = 0; t < TASK_COUNT; t++) {
      // Map task index [0..TASK_COUNT-1] onto spectrum [0..SPECTRUM_LEN-1]
      const spectrumIdx = Math.round(t * (SPECTRUM_LEN - 1) / Math.max(TASK_COUNT - 1, 1));
      const task = tasksByDifficulty[t];
      const profile = spectrum[spectrumIdx];
      queue.push({ task, profile });
    }
  } else {
    // Pair easy tasks with exploitation, hard tasks with exploration
    for (let t = 0; t < TASK_COUNT; t++) {
      const spectrumIdx = Math.round((TASK_COUNT - 1 - t) * (SPECTRUM_LEN - 1) / Math.max(TASK_COUNT - 1, 1));
      const task = tasksByDifficulty[t];
      const profile = spectrum[spectrumIdx];
      queue.push({ task, profile });
    }
  }

  return queue;
}

// ═══════════════════════════════════════════════════════════════════════════════
// WORKER POOL — parallel task execution across threads
// ═══════════════════════════════════════════════════════════════════════════════

const WORKER_PATH = require('path').join(__dirname, 'ufe-worker.js');
const workerPool = [];
const workerQueue = []; // pending tasks waiting for a free worker

function createWorkerPool() {
  for (let i = 0; i < WORKER_COUNT; i++) {
    spawnWorker(i);
  }
}

function spawnWorker(idx) {
  const w = new Worker(WORKER_PATH);
  w._idx = idx;
  w._busy = false;
  w._resolve = null;

  w.on('message', (result) => {
    const resolve = w._resolve;
    w._busy = false;
    w._resolve = null;
    if (resolve) resolve(result);
    // Check if there's queued work
    drainQueue();
  });

  w.on('error', (err) => {
    console.error(`⚠️ Worker ${idx} error:`, err.message);
    const resolve = w._resolve;
    w._busy = false;
    w._resolve = null;
    if (resolve) resolve({ error: err.message });
    // Respawn crashed worker
    workerPool[idx] = null;
    spawnWorker(idx);
    drainQueue();
  });

  workerPool[idx] = w;
}

function drainQueue() {
  while (workerQueue.length > 0) {
    const free = workerPool.find(w => w && !w._busy);
    if (!free) break;
    const { msg, resolve } = workerQueue.shift();
    free._busy = true;
    free._resolve = resolve;
    free.postMessage(msg);
  }
}

function runOnWorker(msg) {
  return new Promise((resolve) => {
    // Strip non-serializable fields (functions, task objects)
    const { _runId, _task, ...workerMsg } = msg;
    const free = workerPool.find(w => w && !w._busy);
    if (free) {
      free._busy = true;
      free._resolve = resolve;
      free.postMessage(workerMsg);
    } else {
      workerQueue.push({ msg: workerMsg, resolve });
    }
  });
}

// Run a batch of tasks in parallel via worker pool
async function runBatch(items) {
  return Promise.all(items.map(item => runOnWorker(item)));
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAUNCH
// ═══════════════════════════════════════════════════════════════════════════════

console.log(`
╔═══════════════════════════════════════════════════════════════════════╗
║       _    _____ ____ ___ ____                                       ║
║      / \\  | ____/ ___|_ _/ ___|                                      ║
║     / _ \\ |  _|| |  _ | |\\___ \\   +  Seeker                          ║
║    / ___ \\| |__| |_| || | ___) |     Discovery Engine                ║
║   /_/   \\_\\_____\\____|___|____/                                      ║
║                                                                       ║
║   24/7 PINCER STRATEGY — Converging from Opposite Ends               ║
║                                                                       ║
║   AEGIS  ◀━━ EXPLORATION ━━━━━━━━━━━━━━ EXPLOITATION ━━▶ Seeker      ║
║              wide / random / curiosity    gradient / surgical         ║
║                        ╲                ╱                              ║
║                          ╲  CONVERGE  ╱                               ║
║                            ╲  HERE  ╱                                 ║
║                              ╲    ╱                                   ║
║                                ╲╱                                     ║
║                     (swap ends each cycle)                            ║
║                                                                       ║
║   ${String(TASK_COUNT).padStart(2)} tasks × ${String(SPECTRUM_LEN).padStart(2)} profiles — smart pairing           ║
║   Each cycle: alternate direction for full coverage                   ║
║                                                                       ║
║   AEGIS  Monitor: http://localhost:5555                               ║
║   Seeker Monitor: http://localhost:5556                               ║
╚═══════════════════════════════════════════════════════════════════════╝
`);

const aegisMonitor = aegis.createMonitor({ port: 5555 });
const seekerMonitor = seeker.createMonitor({ port: 5556 });

// Complete a run on the monitor after worker finishes (workers can't fire events)
function completeWorkerRun(monitor, runId, bestScore, bestParams, evals) {
  const handler = monitor.createHandler(runId);
  // Simulate evaluation events so the counter updates
  for (let i = 0; i < (evals || 0); i += 10) {
    handler({ type: 'evaluation', result: { params: bestParams || {}, score: bestScore || Infinity, timestamp: Date.now() } });
  }
  if (bestParams && isFinite(bestScore)) {
    handler({ type: 'new_best', result: { params: bestParams, score: bestScore }, improvement: 0 });
  }
  handler({ type: 'stopped', reason: 'completed', state: { phase: 'done', ufe: null, strategies: [] } });
}

// Spatial anomaly + equation writer integration
const { computeSpatialAnomalies, HZ_OBSERVATIONS, createEquationWriter } = aegis;
const aegisWriter = createEquationWriter ? createEquationWriter('AEGIS') : null;
const seekerWriter = createEquationWriter ? createEquationWriter('Seeker') : null;

function logSpatialAnomalies(engine, runId, bestParams, monitor) {
  try {
    if (!bestParams || !computeSpatialAnomalies) return;
    // Only compute for f(T) and cross-domain runs that have f(T) params
    const hasAlpha = bestParams.alpha !== undefined || bestParams.fT_alpha !== undefined;
    const hasN = bestParams.n !== undefined || bestParams.fT_n !== undefined;
    if (!hasAlpha || !hasN) return;

    const fTParams = {
      alpha: bestParams.alpha || bestParams.fT_alpha || 0,
      beta: bestParams.beta || 0,
      n: bestParams.n || bestParams.fT_n || 1,
      lambda: bestParams.lambda || bestParams.lambda_quartic || 100,
      modelType: bestParams.modelType || 0,
    };

    const anomalies = computeSpatialAnomalies(fTParams);
    const significant = anomalies.filter(a => a.significance === 'high' || a.significance === 'moderate');

    if (significant.length > 0) {
      const high = significant.filter(a => a.significance === 'high');
      const mod = significant.filter(a => a.significance === 'moderate');
      console.log(`\n🌌 [${engine}] ${runId} — ${high.length} HIGH + ${mod.length} MODERATE spatial anomalies:`);
      for (const a of significant) {
        const icon = a.significance === 'high' ? '🔴' : '🟡';
          console.log(`   ${icon} z=${(a.z||0).toFixed(3)} | ${a.survey} | RA ${a.ra} Dec ${a.dec}`);
          console.log(`      ${a.anomalyType}: Δ=${(a.deviation_sigma||0).toFixed(1)}σ | ${a.fieldDescription}`);
          console.log(`      d=${(a.comovingDist_Mpc||0).toFixed(0)} Mpc | lookback ${(a.lookbackTime_Gyr||0).toFixed(1)} Gyr | ref: ${a.reference}`);
      }

      // Register as alert
      monitor.registerAlert({
        id: `spatial-${runId}`,
        title: `${significant.length} sky anomalies from ${runId}`,
        severity: 'critical',
        category: 'anomaly',
        detail: significant.map(a => `z=${(a.z||0).toFixed(3)} ${a.survey} ${a.anomalyType} ${(a.deviation_sigma||0).toFixed(1)}σ`).join('; '),
        data: { anomalyCount: significant.length, topAnomaly: significant[0] },
      });
    }
  } catch (e) {
    // Silent — don't crash the runner
  }
}

function synthesizeEquation(writer, taskId, params, score) {
  if (!writer) return null;
  try {
    // Use writeDiscovery — the proper API that dispatches to the right method
    // It expects an EvalResult-like object with .params
    const fakeResult = { params: { ...params }, score };
    const eq = writer.writeDiscovery('AEGIS/Seeker', taskId, fakeResult, score);
    if (eq) {
      return { plaintext: eq.plaintext || '', latex: eq.latex || '', eq };
    }
    return null;
  } catch (e) { return null; }
}

function logEquation(engine, runId, taskId, bestParams, bestScore, writer) {
  try {
    if (!writer || !bestParams) return;
    if (!taskId.match(/ufe-torsion|cross-domain|ft-gravity|einstein-cartan|torsion-wave/)) return;
    if (bestScore > 500) return;

    const eq = synthesizeEquation(writer, taskId, bestParams, bestScore);
    if (eq) {
      console.log(`\n📐 [${engine}] Equation from ${runId} (score ${bestScore.toFixed(2)}):`);
      console.log(`   ${eq.plaintext || eq.latex || 'N/A'}`);
    }
  } catch (e) {
    // Silent
  }
}

aegisMonitor.startDashboard();
seekerMonitor.startDashboard();

let aegisCycle = 0, seekerCycle = 0;
let aegisTotal = 0, seekerTotal = 0;

// ═══════════════════════════════════════════════════════════════════════════════
// CROSS-POLLINATION — engines share best discoveries
// When one engine finds a good solution, the other uses it as a seed point
// ═══════════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════════
// STATE PERSISTENCE — survive restarts without losing discoveries
// ═══════════════════════════════════════════════════════════════════════════════
const STATE_FILE = require('path').join(__dirname, 'ufe-state.json');

function saveState() {
  try {
    const state = {
      aegisBests, seekerBests, worstScores, pollinationCounts,
      bestKnown, bestEquation,
      aegisCycle, seekerCycle, aegisTotal, seekerTotal,
      savedAt: new Date().toISOString(),
    };
    require('fs').writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) { console.error('⚠️ State save failed:', e.message); }
}

function loadState() {
  try {
    if (!require('fs').existsSync(STATE_FILE)) return false;
    const state = JSON.parse(require('fs').readFileSync(STATE_FILE, 'utf8'));
    Object.assign(aegisBests, state.aegisBests || {});
    Object.assign(seekerBests, state.seekerBests || {});
    Object.assign(worstScores, state.worstScores || {});
    Object.assign(pollinationCounts, state.pollinationCounts || {});
    Object.assign(bestKnown, state.bestKnown || {});
    if (state.bestEquation) bestEquation = state.bestEquation;
    if (state.aegisCycle) aegisCycle = state.aegisCycle;
    if (state.seekerCycle) seekerCycle = state.seekerCycle;
    if (state.aegisTotal) aegisTotal = state.aegisTotal;
    if (state.seekerTotal) seekerTotal = state.seekerTotal;
    const taskCount = Object.keys(state.aegisBests || {}).length;
    console.log(`📂 Loaded state from ${state.savedAt} — ${taskCount} tasks, ${state.aegisTotal + state.seekerTotal} total runs`);
    return true;
  } catch (e) { console.error('⚠️ State load failed:', e.message); return false; }
}

const bestKnown = {}; // { taskId: { params, score, source } }

function recordBest(taskId, params, score, source) {
  if (!isFinite(score) || !params) return;
  const prev = bestKnown[taskId];
  // Strictly less than — don't log "beats" for equal scores
  if (!prev || score < prev.score) {
    const improved = prev ? prev.score - score : 0;
    bestKnown[taskId] = { params: { ...params }, score, source };
    if (prev && prev.source !== source && improved > 1e-6) {
      console.log(`\n🔄 [CROSS-POLLINATION] ${source} beat ${prev.source} on ${taskId}: ${score.toFixed(4)} < ${prev.score.toFixed(4)} (Δ${improved.toFixed(4)})`);
      countPollination(taskId);
    }
    // Save breakthroughs immediately
    if (improved > 0.01 || !prev) saveState();
  }
}

function getSeedParams(taskId, source) {
  const known = bestKnown[taskId];
  // Only seed from the OTHER engine's discovery
  if (known && known.source !== source) {
    // Add jitter to break plateaus — 2% random perturbation
    const jittered = { ...known.params };
    for (const key of Object.keys(jittered)) {
      if (typeof jittered[key] === 'number' && isFinite(jittered[key])) {
        const scale = Math.abs(jittered[key]) || 1;
        jittered[key] += (Math.random() - 0.5) * 0.04 * scale;
      }
    }
    return { params: jittered, score: known.score };
  }
  return null;
}

async function runAegisLoop() {
  while (true) {
    aegisCycle++;
    const fromExploration = aegisCycle % 2 === 1;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[AEGIS] ━━ Cycle ${aegisCycle} ━━ ${direction} ━━ ${queue.length} runs (${WORKER_COUNT} threads)`);

    for (let i = 0; i < queue.length; i += WORKER_COUNT) {
      const batch = queue.slice(i, i + WORKER_COUNT);
      const workerMsgs = batch.map(({ task, profile }) => {
        aegisTotal++;
        const seedData = getSeedParams(task.id, 'AEGIS');
        if (seedData) {
          console.log(`   🧬 [AEGIS] Seeding ${task.name} with Seeker's best (${seedData.score.toFixed(2)})`);
        }
        const runId = `aegis-${task.id}-${profile.tag}-c${aegisCycle}`;
        aegisMonitor.registerRun(runId, `AEGIS: ${task.name} [${profile.tag}]`);
        return {
          engineName: 'AEGIS',
          taskId: task.id,
          profileConfig: getProfileConfig(profile, task.id),
          seedData: seedData || null,
          runSeed: aegisTotal * 1000 + Date.now() % 10000,
          _runId: runId,
          _task: task,
        };
      });

      const results = await runBatch(workerMsgs);

      for (let j = 0; j < results.length; j++) {
        const r = results[j];
        const msg = workerMsgs[j];
        completeWorkerRun(aegisMonitor, msg._runId, r.bestScore, r.bestParams, r.evals || 0);
        if (r.error) {
          console.error(`[AEGIS] Error: ${msg.taskId}: ${r.error}`);
          continue;
        }
        if (r.bestParams && isFinite(r.bestScore)) {
          recordBest(r.taskId, r.bestParams, r.bestScore, 'AEGIS');
          updateScoreboard(r.taskId, r.bestScore, 'AEGIS');
          updateBestEquation('AEGIS', r.taskId, r.bestParams, r.bestScore, aegisWriter);
        }
        if (r.bestParams && r.taskId.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('AEGIS', msg._runId, r.bestParams, aegisMonitor);
          logEquation('AEGIS', msg._runId, r.taskId, r.bestParams, r.bestScore, aegisWriter);
        }
      }
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    console.log(`[AEGIS] Cycle ${aegisCycle} done — ${aegisTotal} lifetime runs`);
  }
}

async function runSeekerLoop() {
  while (true) {
    seekerCycle++;
    const fromExploration = seekerCycle % 2 === 0;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[Seeker] ━━ Cycle ${seekerCycle} ━━ ${direction} ━━ ${queue.length} runs (${WORKER_COUNT} threads)`);

    for (let i = 0; i < queue.length; i += WORKER_COUNT) {
      const batch = queue.slice(i, i + WORKER_COUNT);
      const workerMsgs = batch.map(({ task, profile }) => {
        seekerTotal++;
        const seedData = getSeedParams(task.id, 'Seeker');
        if (seedData) {
          console.log(`   🧬 [Seeker] Seeding ${task.name} with AEGIS's best (${seedData.score.toFixed(2)})`);
        }
        const runId = `seeker-${task.id}-${profile.tag}-c${seekerCycle}`;
        seekerMonitor.registerRun(runId, `Seeker: ${task.name} [${profile.tag}]`);
        return {
          engineName: 'Seeker',
          taskId: task.id,
          profileConfig: getProfileConfig(profile, task.id),
          seedData: seedData || null,
          runSeed: seekerTotal * 2000 + Date.now() % 10000,
          _runId: runId,
          _task: task,
        };
      });

      const results = await runBatch(workerMsgs);

      for (let j = 0; j < results.length; j++) {
        const r = results[j];
        const msg = workerMsgs[j];
        completeWorkerRun(seekerMonitor, msg._runId, r.bestScore, r.bestParams, r.evals || 0);
        if (r.error) {
          console.error(`[Seeker] Error: ${msg.taskId}: ${r.error}`);
          continue;
        }
        if (r.bestParams && isFinite(r.bestScore)) {
          recordBest(r.taskId, r.bestParams, r.bestScore, 'Seeker');
          updateScoreboard(r.taskId, r.bestScore, 'Seeker');
          updateBestEquation('Seeker', r.taskId, r.bestParams, r.bestScore, seekerWriter);
        }
        if (r.bestParams && r.taskId.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('Seeker', msg._runId, r.bestParams, seekerMonitor);
          logEquation('Seeker', msg._runId, r.taskId, r.bestParams, r.bestScore, seekerWriter);
        }
      }
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    console.log(`[Seeker] Cycle ${seekerCycle} done — ${seekerTotal} lifetime runs`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SCOREBOARD + EQUATION TRACKER — pushes to both monitors for dashboard display
// ═══════════════════════════════════════════════════════════════════════════════

// Track per-engine best scores, worst scores (for progress baseline), and cross-pollination counts
const aegisBests = {};  // { taskId: score }
const seekerBests = {}; // { taskId: score }
const worstScores = {}; // { taskId: score } — highest score ever seen, used as progress baseline
const pollinationCounts = {}; // { taskId: count }

// Target scores for progress calculation (χ² targets — lower is better)
const TASK_TARGETS = {
  'energy-conditions': 0,
  'einstein-cartan': 0.001,
  'torsion-wave': 0.01,
  'rsd-growth': 2,
  's8-tension': 8,
  'desi-bao-fit': 10,
  'dark-energy-eos': 10,
  'cc-hubble-fit': 12,
  'ft-gravity': 12,
  'model-selection-bic': 20,
  'sne-pantheon-fit': 50,
  'ufe-cross-domain': 50,
  'combined-multisurvey': 100,
  'h0-tension': 10,
  'ufe-torsion': 100,
};

// Adaptive eval budget: converged tasks get 25% budget, improving get 150%
function getTaskMultiplier(taskId) {
  const target = TASK_TARGETS[taskId];
  if (target === undefined) return 1.0;
  const aScore = aegisBests[taskId];
  const sScore = seekerBests[taskId];
  const best = (aScore != null && sScore != null) ? Math.min(aScore, sScore)
    : aScore != null ? aScore : sScore;
  if (best == null) return 1.0; // no data yet — normal budget
  if (best <= target) return 0.25; // converged — minimal budget
  if (target > 0 && best <= target * 2) return 1.5; // improving — boost
  if (target > 0 && best <= target * 5) return 1.25; // grinding — slight boost
  return 1.0; // exploring — normal
}

// Nice display names
const TASK_NAMES = {
  'energy-conditions': 'Energy Conditions',
  'einstein-cartan': 'Einstein-Cartan Torsion',
  'torsion-wave': 'Torsion Wave Dispersion',
  'rsd-growth': 'RSD fσ₈ Growth',
  's8-tension': 'S₈ Tension',
  'desi-bao-fit': 'DESI DR1 BAO',
  'dark-energy-eos': 'Dark Energy EoS w₀wₐ',
  'cc-hubble-fit': 'Cosmic Chronometer H(z)',
  'ft-gravity': 'f(T) Teleparallel',
  'model-selection-bic': 'Model Selection ΔBIC',
  'sne-pantheon-fit': 'Pantheon+ SNe Ia',
  'ufe-cross-domain': 'UFE Cross-Domain Unified',
  'combined-multisurvey': 'Combined Multi-Survey',
  'h0-tension': 'H₀ Tension Resolver',
  'ufe-torsion': 'UFE Torsion Mexican Hat',
};

function updateScoreboard(taskId, score, engine) {
  if (!isFinite(score)) return;
  // Track worst score seen (progress baseline)
  if (!worstScores[taskId] || score > worstScores[taskId]) worstScores[taskId] = score;
  if (engine === 'AEGIS') {
    if (!aegisBests[taskId] || score < aegisBests[taskId]) aegisBests[taskId] = score;
  } else {
    if (!seekerBests[taskId] || score < seekerBests[taskId]) seekerBests[taskId] = score;
  }
}

function countPollination(taskId) {
  pollinationCounts[taskId] = (pollinationCounts[taskId] || 0) + 1;
}

// Best equation tracker
let bestEquation = null;

function updateBestEquation(engine, taskId, params, score, writer) {
  try {
    if (!writer || !params || !isFinite(score)) return;
    if (score > 500) return;
    if (!taskId.match(/ufe-torsion|cross-domain|ft-gravity|einstein-cartan|torsion-wave/)) return;
    if (bestEquation && score >= bestEquation.score) return;
    const eq = synthesizeEquation(writer, taskId, params, score);
    if (eq) {
      bestEquation = {
        plaintext: eq.plaintext || eq.latex || 'N/A',
        latex: eq.latex || '',
        params: { ...params },
        score,
        engine,
        taskId,
      };
      console.log(`\n🏆 [EQUATION UPDATED] ${engine} → ${taskId} (score ${score.toFixed(4)}):`);
      console.log(`   ${bestEquation.plaintext}`);
    }
  } catch (e) { /* silent */ }
}

function pushScoreboardToMonitors() {
  const allTaskIds = Object.keys(TASK_TARGETS);
  const rows = allTaskIds.map(taskId => {
    const aScore = aegisBests[taskId] ?? null;
    const sScore = seekerBests[taskId] ?? null;
    const bestScore = (aScore !== null && sScore !== null) ? Math.min(aScore, sScore)
      : aScore !== null ? aScore : sScore;
    const bestEngine = bestScore === aScore ? 'AEGIS' : 'Seeker';
    const target = TASK_TARGETS[taskId];
    // Progress: use actual worst score seen as baseline, not a guess
    const worstSeen = worstScores[taskId] || null;
    let progress = 0;
    if (bestScore !== null) {
      if (bestScore <= target) {
        progress = 100;
      } else if (worstSeen !== null && worstSeen > target) {
        // Real progress = how far we've come from worst to target
        // Use log scale for scores spanning many orders of magnitude
        const logBest = Math.log10(Math.max(bestScore, 1e-12));
        const logWorst = Math.log10(Math.max(worstSeen, 1e-12));
        const logTarget = Math.log10(Math.max(target, 1e-12));
        if (logWorst > logTarget) {
          progress = Math.max(0, Math.min(99, (1 - (logBest - logTarget) / (logWorst - logTarget)) * 100));
        } else {
          // Linear fallback when log scale doesn't make sense
          progress = Math.max(0, Math.min(99, (1 - (bestScore - target) / (worstSeen - target)) * 100));
        }
      }
    }
    // Status — based on ratio of best score to target
    let status = 'exploring';
    if (bestScore !== null) {
      if (bestScore <= target) status = 'converged';
      else if (target > 0 && bestScore <= target * 2) status = 'improving';
      else if (target > 0 && bestScore <= target * 10) status = 'grinding';
      else if (target === 0 && bestScore < 1) status = 'improving';
      else if (target === 0 && bestScore < 100) status = 'grinding';
      else status = 'exploring';
    }
    return {
      task: TASK_NAMES[taskId] || taskId,
      taskId,
      aegisScore: aScore,
      seekerScore: sScore,
      bestScore,
      bestEngine,
      target,
      progress,
      pollinations: pollinationCounts[taskId] || 0,
      status,
    };
  }).sort((a, b) => {
    // Sort: converged first, then by progress descending
    const statusOrder = { converged: 0, improving: 1, grinding: 2, exploring: 3 };
    const aOrd = statusOrder[a.status] ?? 4;
    const bOrd = statusOrder[b.status] ?? 4;
    if (aOrd !== bOrd) return aOrd - bOrd;
    return b.progress - a.progress;
  });

  aegisMonitor.setScoreboard(rows);
  seekerMonitor.setScoreboard(rows);
  if (bestEquation) {
    aegisMonitor.setEquation(bestEquation);
    seekerMonitor.setEquation(bestEquation);
  }
}

// Push scoreboard every 5 seconds
setInterval(pushScoreboardToMonitors, 5000);

// Status printer + state persistence (every 60s)
setInterval(() => {
  const aegisDir = aegisCycle % 2 === 1 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  const seekerDir = seekerCycle % 2 === 0 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  console.log(`\n${'━'.repeat(70)}`);
  console.log(`AEGIS  │ cycle ${aegisCycle} (${aegisDir}) │ ${aegisTotal} total runs`);
  console.log(`Seeker │ cycle ${seekerCycle} (${seekerDir}) │ ${seekerTotal} total runs`);
  aegisMonitor.printStatus();
  seekerMonitor.printStatus();
  saveState(); // persist discoveries to disk
}, 60000);

// ═══════════════════════════════════════════════════════════════════════════════
// RUNTIME CONTROL API — adjust speed from dashboard without restarting
// ═══════════════════════════════════════════════════════════════════════════════
const controlServer = require('http').createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }

  // GET /config — current settings
  if (req.url === '/config' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      evalScale: EVAL_SCALE,
      delayMs: DELAY_MS,
      aegisCycle,
      seekerCycle,
      aegisTotal,
      seekerTotal,
      baseEvals: BASE_EVALS,
      effectiveEvals: BASE_EVALS.map(b => Math.round(b * EVAL_SCALE)),
      spectrumTags: spectrum.map(s => s.tag),
      gpu: gpu.getGPUInfo(),
    }));
    return;
  }

  // POST /config — update settings live
  if (req.url === '/config' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const update = JSON.parse(body);
        if (update.evalScale !== undefined) {
          EVAL_SCALE = Math.max(0.1, Math.min(10, parseFloat(update.evalScale)));
          console.log(`⚙️  [CONTROL] EVAL_SCALE changed to ${EVAL_SCALE}x`);
        }
        if (update.delayMs !== undefined) {
          DELAY_MS = Math.max(0, Math.min(5000, parseInt(update.delayMs)));
          console.log(`⚙️  [CONTROL] DELAY_MS changed to ${DELAY_MS}ms`);
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, evalScale: EVAL_SCALE, delayMs: DELAY_MS }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  res.writeHead(404); res.end('Not found');
});
controlServer.listen(CONTROL_PORT, () => {
  console.log(`🎛️  Control API: http://localhost:${CONTROL_PORT}/config`);
});

// Load persisted state before starting
loadState();
pushScoreboardToMonitors(); // show restored scores immediately

// Spawn worker pool for parallel task execution
createWorkerPool();
console.log(`🧵 Worker pool ready: ${WORKER_COUNT} threads`);

// Optional GPU acceleration — auto-detects and falls back gracefully
gpu.initGPU().then(info => {
  if (info && info.gpu) {
    console.log(`⚡ GPU: ${info.device} (${info.vram_gb}GB) — ${info.distances_per_sec.toLocaleString()} dist/sec`);
  } else if (info) {
    console.log(`⚡ GPU: NumPy CPU fallback — ${info.distances_per_sec.toLocaleString()} dist/sec`);
  } else {
    console.log('⚡ GPU: disabled (Python/NumPy not available)');
  }
}).catch(() => {});

Promise.all([runAegisLoop(), runSeekerLoop()]).catch(err => {
  console.error('Fatal error:', err);
});

process.on('SIGINT', () => {
  console.log('\nSaving state before shutdown...');
  saveState();
  gpu.shutdownGPU();
  // Terminate workers
  for (const w of workerPool) { if (w) w.terminate(); }
  aegisMonitor.stopDashboard();
  seekerMonitor.stopDashboard();
  process.exit(0);
});
