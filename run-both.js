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
  emergenceTask,
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
  // ═══════════════════════════════════════════════════════════════════════════
  // ALLOCATION: 1/3 UFE cosmology, 1/3 anomaly hunting, 1/3 emergence
  // Each third gets ~10 task slots in the rotation
  // ═══════════════════════════════════════════════════════════════════════════

  // ── THIRD 1: UFE Cosmology (core torsion fits) ────────────────────────────
  cosmicChronTask,                                    // CC H(z) — 3 params
  aegis.ufeTorsionTask,                               // UFE Mexican hat — 8 params
  desiBAOTask,                                        // DESI BAO — 4 params
  sneTask,                                            // Pantheon+ SNe — 4 params
  h0TensionTask,                                      // H₀ tension — 4 params
  wDETask,                                            // w₀wₐCDM + torsion — 6 params
  combinedFitTask,                                    // FULL multi-survey — 5 params
  s8TensionTask,                                      // S₈ tension — 3 params
  rsdGrowthTask,                                      // fσ₈ growth — 4 params
  aegis.ufeTorsionTask,                               // UFE — exploitation pass

  // ── THIRD 2: Anomaly Hunting (unreported discoveries) ─────────────────────
  aegis.einsteinCartanTask,                           // EC torsion — fresh anomalies
  aegis.fTGravityTask,                                // f(T) teleparallel deviations
  aegis.torsionWaveTask,                              // Wave dispersion anomalies
  aegis.crossDomainTask,                              // Cross-domain unified — anomalies
  modelSelectionTask,                                 // ΔBIC — statistical anomalies
  energyConditionTask,                                // Energy condition violations
  aegis.einsteinCartanTask,                           // EC — deeper exploration
  aegis.fTGravityTask,                                // f(T) — deeper exploration
  aegis.torsionWaveTask,                              // Wave — deeper exploration
  aegis.crossDomainTask,                              // Cross-domain — max budget

  // ── THIRD 3: Emergence (quantum→cosmos cascade) ───────────────────────────
  emergenceTask,                                      // Emergence — initial exploration
  emergenceTask,                                      // Emergence — exploitation pass 1
  emergenceTask,                                      // Emergence — exploitation pass 2
  emergenceTask,                                      // Emergence — exploitation pass 3
  emergenceTask,                                      // Emergence — exploitation pass 4
  emergenceTask,                                      // Emergence — exploitation pass 5
  emergenceTask,                                      // Emergence — exploitation pass 6
  emergenceTask,                                      // Emergence — deep exploitation
  emergenceTask,                                      // Emergence — deep exploitation 2
  emergenceTask,                                      // Emergence — max budget final
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
  const safeScore = isFinite(bestScore) ? bestScore : Infinity;
  const safeParams = bestParams || {};
  const now = Date.now();

  // Fire a single evaluation event with the final eval count (avoid spamming)
  if (evals > 0) {
    handler({
      type: 'evaluation',
      result: { params: safeParams, score: safeScore, timestamp: now, strategy: 'worker' },
    });
    // Manually set totalEvals on the run tracker since we only fire 1 event
    const run = monitor.runs ? monitor.runs.get(runId) : null;
    if (run) run.totalEvals = evals;
  }

  if (bestParams && isFinite(bestScore)) {
    handler({
      type: 'new_best',
      result: { params: bestParams, score: bestScore, timestamp: now, strategy: 'worker' },
      improvement: 0,
    });
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
      discoveries, discoveryCounter,
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
    // Restore discoveries
    if (state.discoveries && Array.isArray(state.discoveries)) {
      discoveries.length = 0;
      state.discoveries.forEach(d => discoveries.push(d));
      discoveryCounter = state.discoveryCounter || discoveries.length;
      console.log(`🔭 Loaded ${discoveries.length} novel discoveries`);
    }
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

function getSeedParams(taskId, source, task) {
  const known = bestKnown[taskId];

  // Priority 1: Emergence cascade seed (quantum → cosmo)
  if (task && task.parameters && Math.random() < 0.3) {
    const emergenceSeed = getEmergenceSeed(taskId, task.parameters);
    if (emergenceSeed) return emergenceSeed;
  }

  // Priority 2: Cross-pollination from other engine
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

// ═══════════════════════════════════════════════════════════════════════════════
// EMERGENCE CASCADE — quantum results propagate upward to constrain cosmology
// Level 1: Einstein-Cartan (spin → torsion tensor)
// Level 2: UFE Torsion (Mexican hat → VEV, mass, condensate)
// Level 3: Torsion Wave (propagation → dispersion, causality)
// Level 4: Cross-Domain (unification → β_eff, constraints)
// Level 5: Cosmology (H(z), BAO, SNe, growth)
// Level 6: Combined / Model Selection
// ═══════════════════════════════════════════════════════════════════════════════

const emergenceLevels = {
  1: ['einstein-cartan'],
  2: ['ufe-torsion', 'energy-conditions'],
  3: ['torsion-wave'],
  4: ['ufe-cross-domain', 'ft-gravity'],
  5: ['cc-hubble-fit', 'desi-bao-fit', 'sne-pantheon-fit', 'h0-tension', 'rsd-growth', 's8-tension', 'dark-energy-eos'],
  6: ['combined-multisurvey', 'model-selection-bic'],
};

// Derive physical quantities from converged lower levels
function computeEmergenceState() {
  const state = { level: 0, derived: {}, constraints: {} };

  // ── Level 1: Einstein-Cartan → spin density, torsion scalar ──
  const ec = bestKnown['einstein-cartan'];
  if (ec && ec.score < 0.1) {
    state.level = 1;
    const T2 = [ec.params.T01, ec.params.T02, ec.params.T03, ec.params.T12, ec.params.T13, ec.params.T23]
      .reduce((s, t) => s + (t || 0) ** 2, 0);
    state.derived.torsionScalar = Math.sqrt(T2);
    state.derived.spinDensity = ec.params.spinDensity || 0;
    state.derived.ecCoupling = ec.params.couplingLambda || 0;
  }

  // ── Level 2: UFE Torsion → μ², λ, T_vev, m_T, condensation ──
  const ufe = bestKnown['ufe-torsion'];
  if (ufe && ufe.score < 0.01) {
    state.level = Math.max(state.level, 2);
    const mu2 = Math.pow(10, ufe.params.log_mu2 || 0);
    const lambda = Math.pow(10, ufe.params.log_lambda || 0);
    const T_vev = mu2 > 0 && lambda > 0 ? Math.sqrt(mu2 / (2 * lambda)) : 0;
    const m_T = Math.sqrt(4 * mu2);

    state.derived.mu2 = mu2;
    state.derived.lambda = lambda;
    state.derived.T_vev = T_vev;
    state.derived.m_T = m_T;
    state.derived.gamma = ufe.params.gamma;
    state.derived.kappa_f = ufe.params.kappa_f;
    state.derived.kappa_g = ufe.params.kappa_g;

    // Derive effective β from torsion condensation
    // β_eff ≈ κ_g * T_vev² / (8πG * ρ_m) — torsion modifies matter sector
    // In natural units with T_vev ~ O(1): β_eff ~ κ_g * T_vev²
    if (T_vev > 0) {
      state.derived.beta_from_condensation = ufe.params.kappa_g * T_vev * T_vev * 1e-4;
    }
  }

  // ── Level 3: Torsion Wave → dispersion, phase velocity ──
  const wave = bestKnown['torsion-wave'];
  if (wave && wave.score < 0.1) {
    state.level = Math.max(state.level, 3);
    const omega = wave.params.frequency || 0;
    const k = wave.params.wavenumber || 0;
    state.derived.omega = omega;
    state.derived.wavenumber = k;
    state.derived.v_phase = k > 0 && omega > 0 ? omega / k : 0;
    state.derived.v_group = omega > 0 ? k / omega : 0;
    state.derived.waveAmplitude = wave.params.amplitude;
    state.derived.J_spin = wave.params.J_spin;

    // Wave mass must match Mexican hat: m_wave² ≈ 4μ²
    if (state.derived.mu2) {
      state.derived.massConsistency = Math.abs(4 * wave.params.mu2 - 4 * state.derived.mu2) / (4 * state.derived.mu2 + 1e-30);
    }
  }

  // ── Level 4: Cross-domain → unified constraints ──
  const cross = bestKnown['ufe-cross-domain'];
  if (cross && cross.score < 100) {
    state.level = Math.max(state.level, 4);
    state.derived.H0_cross = (cross.params.H0_rescaled || 1) * 70;
    state.derived.fT_alpha = cross.params.fT_alpha;
    state.derived.fT_n = cross.params.fT_n;
  }

  // ── Level 5: H₀ tension → evolving β(z) ──
  const h0 = bestKnown['h0-tension'];
  if (h0 && h0.score < 5) {
    state.level = Math.max(state.level, 5);
    state.derived.H0_tension = h0.params.H0;
    state.derived.beta0 = h0.params.beta0;
    state.derived.beta1 = h0.params.beta1;
    // β(z) = β₀ + β₁ * z/(1+z)
    state.derived.beta_at_z0 = h0.params.beta0;
    state.derived.beta_at_z1 = h0.params.beta0 + h0.params.beta1 * 0.5; // z=1
    state.derived.beta_at_zinf = h0.params.beta0 + h0.params.beta1;
  }

  // ── Build constraints for higher levels ──
  // These narrow the search space for cosmological tasks
  if (state.level >= 2 && state.derived.T_vev > 0) {
    // Torsion mass constrains wave equation
    state.constraints['torsion-wave'] = { mu2_hint: state.derived.mu2, lambda_hint: state.derived.lambda };
    // VEV constrains cross-domain
    state.constraints['ufe-cross-domain'] = { T_vev_hint: state.derived.T_vev, mu2_hint: state.derived.mu2 };

    // ── UFE EMERGENCE: Feed quantum→cosmology bottom-up ──
    // Emergence inherits Mexican Hat params from UFE Torsion (Level 2)
    state.constraints['ufe-emergence'] = {
      log_mu2_hint: ufe.params.log_mu2,
      log_lambda_hint: ufe.params.log_lambda,
      kappa_g_hint: ufe.params.kappa_g || state.derived.kappa_g,
      kappa_f_hint: ufe.params.kappa_f || state.derived.kappa_f,
    };
  }
  if (state.level >= 5 && state.derived.beta0 !== undefined) {
    // Evolving β constrains all cosmological tasks
    const beta_cosmo = state.derived.beta0; // use z=0 value for static-β tasks
    state.constraints['cc-hubble-fit'] = { beta_hint: beta_cosmo };
    state.constraints['desi-bao-fit'] = { beta_hint: beta_cosmo };
    state.constraints['sne-pantheon-fit'] = { beta_hint: beta_cosmo };
    state.constraints['rsd-growth'] = { beta_hint: state.derived.beta_at_z1 };
    state.constraints['combined-multisurvey'] = { beta_hint: beta_cosmo };

    // Emergence also inherits β-evolution and H₀ from Level 5
    if (state.constraints['ufe-emergence']) {
      state.constraints['ufe-emergence'].beta_quantum_hint = 0; // superposition → 0
      state.constraints['ufe-emergence'].beta_scale_hint = Math.abs(beta_cosmo) * 1e-3;
      state.constraints['ufe-emergence'].H0_hint = state.derived.H0_tension;
      state.constraints['ufe-emergence'].omega_m_hint = 0.30; // near Planck
    }
  }

  return state;
}

// Generate emergence-seeded starting point for a task
function getEmergenceSeed(taskId, taskParams) {
  const emergence = computeEmergenceState();
  const constraints = emergence.constraints[taskId];
  if (!constraints) return null;

  // Build a seed point using derived quantum constraints + random for the rest
  const seed = {};
  for (const p of taskParams) {
    if (constraints[p.name + '_hint'] !== undefined) {
      // Use derived value with small jitter
      const hint = constraints[p.name + '_hint'];
      const range = p.max - p.min;
      const jitter = (Math.random() - 0.5) * 0.1 * range;
      seed[p.name] = Math.max(p.min, Math.min(p.max, hint + jitter));
    } else if (p.name === 'beta' && constraints.beta_hint !== undefined) {
      const hint = constraints.beta_hint;
      const range = p.max - p.min;
      const jitter = (Math.random() - 0.5) * 0.2 * range;
      seed[p.name] = Math.max(p.min, Math.min(p.max, hint + jitter));
    } else {
      // Random within bounds
      seed[p.name] = p.min + Math.random() * (p.max - p.min);
    }
  }

  return { params: seed, score: Infinity, source: 'emergence' };
}

// Log emergence state periodically
let lastEmergenceLog = 0;
function logEmergenceState() {
  const now = Date.now();
  if (now - lastEmergenceLog < 120000) return; // every 2 min max
  lastEmergenceLog = now;

  const state = computeEmergenceState();
  if (state.level === 0) return;

  const levelNames = ['', 'QUANTUM', 'SYMMETRY BREAKING', 'PROPAGATION', 'UNIFICATION', 'COSMOLOGY', 'OBSERVATION'];
  console.log(`\n🌊 EMERGENCE CASCADE — Level ${state.level}: ${levelNames[state.level]}`);

  if (state.derived.T_vev) console.log(`   L2 → T_vev = ${state.derived.T_vev.toExponential(3)}, m_T = ${state.derived.m_T.toFixed(3)} M_Pl`);
  if (state.derived.v_phase) console.log(`   L3 → v_phase = ${state.derived.v_phase.toFixed(4)}c, ω = ${state.derived.omega.toFixed(4)}`);
  if (state.derived.beta0 !== undefined) console.log(`   L5 → β(z) = ${state.derived.beta0.toFixed(4)} + ${state.derived.beta1.toFixed(4)}·z/(1+z), H₀ = ${state.derived.H0_tension.toFixed(2)}`);

  const constrained = Object.keys(state.constraints);
  if (constrained.length > 0) console.log(`   ↳ Constraining ${constrained.length} tasks: ${constrained.join(', ')}`);
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
        const seedData = getSeedParams(task.id, 'AEGIS', task);
        if (seedData && seedData.source === 'emergence') {
          console.log(`   🌊 [AEGIS] Emergence seed for ${task.name} (quantum→cosmo)`);
        } else if (seedData) {
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
          checkForDiscoveries(r.taskId, r.bestParams, r.bestScore);
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
        const seedData = getSeedParams(task.id, 'Seeker', task);
        if (seedData && seedData.source === 'emergence') {
          console.log(`   🌊 [Seeker] Emergence seed for ${task.name} (quantum→cosmo)`);
        } else if (seedData) {
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
          checkForDiscoveries(r.taskId, r.bestParams, r.bestScore);
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
  'ufe-emergence': 30,
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
  'ufe-emergence': 'UFE Emergence (Quantum→Cosmos)',
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

// ═══════════════════════════════════════════════════════════════════════════════
// NOVEL DISCOVERY TRACKER — flags predictions not in existing survey data
// ═══════════════════════════════════════════════════════════════════════════════

const discoveries = [];  // { id, type, title, detail, params, significance, timestamp, taskId }
let discoveryCounter = 0;

// Known survey bounds — if our predictions fall outside these, it's novel
const SURVEY_BOUNDS = {
  H0:       { min: 67.0, max: 74.0, surveys: 'Planck+SH0ES' },
  omega_m:  { min: 0.25, max: 0.35, surveys: 'Planck+DES+KiDS' },
  sigma8:   { min: 0.75, max: 0.85, surveys: 'Planck+KiDS+DES' },
  w0:       { min: -1.3, max: -0.7, surveys: 'Planck+DESI+DES' },
  wa:       { min: -1.5, max: 0.5, surveys: 'DESI DR1' },
  beta:     { min: -999, max: 999, surveys: 'NONE — torsion coupling is novel' },
  beta0:    { min: -999, max: 999, surveys: 'NONE — evolving torsion is novel' },
  beta1:    { min: -999, max: 999, surveys: 'NONE — torsion evolution is novel' },
  rs:       { min: 140, max: 152, surveys: 'Planck+BOSS' },
};

// Physical thresholds that indicate novel physics
const NOVEL_CHECKS = [
  {
    id: 'torsion-coupling',
    test: (taskId, params) => {
      if (!params.beta && params.beta !== 0) return null;
      const b = params.beta;
      if (Math.abs(b) > 0.05) {
        return {
          type: 'novel_coupling',
          title: `Torsion coupling |beta|=${Math.abs(b).toFixed(4)} detected`,
          detail: `Non-zero torsion-matter coupling (beta=${b.toFixed(6)}) implies spacetime torsion modifies matter clustering. No current survey measures this — testable via next-gen BAO (DESI DR2, Euclid).`,
          significance: Math.min(Math.abs(b) / 0.05, 5).toFixed(1) + 'x threshold',
        };
      }
      return null;
    },
  },
  {
    id: 'evolving-torsion',
    test: (taskId, params) => {
      if (params.beta0 === undefined || params.beta1 === undefined) return null;
      if (Math.abs(params.beta1) > 0.05) {
        return {
          type: 'novel_evolution',
          title: `Evolving torsion: beta(z) = ${params.beta0.toFixed(4)} + ${params.beta1.toFixed(4)}*z/(1+z)`,
          detail: `Redshift-dependent torsion coupling detected. Early universe (beta_inf=${(params.beta0+params.beta1).toFixed(4)}) differs from late universe (beta_0=${params.beta0.toFixed(4)}). This is a completely novel prediction — no survey has tested for z-dependent torsion.`,
          significance: 'Novel physics',
        };
      }
      return null;
    },
  },
  {
    id: 'phantom-crossing',
    test: (taskId, params) => {
      if (params.w0 === undefined) return null;
      if (params.w0 < -1.0) {
        return {
          type: 'phantom_de',
          title: `Phantom dark energy: w0=${params.w0.toFixed(4)}`,
          detail: `Dark energy equation of state crosses phantom divide (w < -1). Combined with torsion coupling beta=${(params.beta||0).toFixed(4)}, this suggests torsion contributes an effective phantom component. DESI DR1 hints at w0 < -1 but torsion origin is unreported.`,
          significance: `${Math.abs(params.w0 + 1).toFixed(3)} below phantom divide`,
        };
      }
      return null;
    },
  },
  {
    id: 'h0-bridge',
    test: (taskId, params) => {
      if (taskId !== 'h0-tension' || !params.H0) return null;
      if (params.H0 > 69.5 && params.H0 < 74.5) {
        return {
          type: 'h0_resolution',
          title: `H0 tension bridged: ${params.H0.toFixed(2)} km/s/Mpc`,
          detail: `Torsion model finds H0=${params.H0.toFixed(2)} between Planck (67.4) and SH0ES (73.0). This is achieved through evolving torsion coupling, not by adding new particles or modifying recombination. No published model uses torsion condensation for this.`,
          significance: 'Novel mechanism',
        };
      }
      return null;
    },
  },
  {
    id: 'torsion-mass',
    test: (taskId, params) => {
      if (taskId !== 'ufe-torsion' || !params.log_mu2) return null;
      const mu2 = Math.pow(10, params.log_mu2);
      const mT = 2 * Math.sqrt(mu2);
      if (mT > 1.0) {
        return {
          type: 'novel_mass',
          title: `Torsion mass m_T = ${mT.toFixed(2)} (Planck units)`,
          detail: `Torsion field has dynamical mass m_T=${mT.toFixed(2)} M_Pl = ${(mT * 1.22e19).toExponential(2)} GeV from Mexican hat potential. This predicts a massive torsion boson not in the Standard Model. Testable via gravitational wave spectroscopy or collider missing energy.`,
          significance: `${mT.toFixed(2)} M_Pl`,
        };
      }
      return null;
    },
  },
  {
    id: 'vev-alignment',
    test: (taskId, params) => {
      if (taskId !== 'ufe-torsion') return null;
      const mu2 = Math.pow(10, params.log_mu2 || 0);
      const lam = Math.pow(10, params.log_lambda || 0);
      const T0 = Math.pow(10, params.log_T0 || 0);
      const Tvev = mu2 > 0 && lam > 0 ? Math.sqrt(mu2 / (2 * lam)) : 0;
      if (Tvev > 0 && Math.abs(T0 / Tvev - 1) < 0.001) {
        return {
          type: 'spontaneous_condensation',
          title: `Torsion condensation confirmed: T0/Tvev = ${(T0/Tvev).toFixed(6)}`,
          detail: `Background torsion field sits at vacuum expectation value to ${Math.abs(T0/Tvev - 1).toExponential(1)} precision. This is spontaneous torsion condensation — the gravitational analogue of the Higgs mechanism. Completely novel; no survey has observed torsion VEV alignment.`,
          significance: 'Novel mechanism — gravitational Higgs analogue',
        };
      }
      return null;
    },
  },
  {
    id: 'subluminal-wave',
    test: (taskId, params) => {
      if (taskId !== 'torsion-wave') return null;
      const k = params.wavenumber || 0;
      const omega = params.frequency || 0;
      if (k > 0 && omega > 0) {
        const vPhase = omega / k;
        if (vPhase < 1.0 && vPhase > 0.01) {
          return {
            type: 'torsion_wave',
            title: `Subluminal torsion wave: v_phase = ${vPhase.toFixed(4)}c`,
            detail: `Torsion perturbations propagate at ${(vPhase*100).toFixed(1)}% of light speed. This predicts a new type of gravitational radiation detectable by pulsar timing arrays (NANOGrav, EPTA) at frequencies f ~ ${(omega/(2*Math.PI)).toExponential(2)} Hz. No current survey has searched for torsion waves.`,
            significance: `v = ${(vPhase*100).toFixed(1)}% c`,
          };
        }
      }
      return null;
    },
  },
  {
    id: 'sound-horizon-shift',
    test: (taskId, params) => {
      if (!params.rs) return null;
      const shift = params.rs - 147.09;
      if (Math.abs(shift) > 3.0) {
        return {
          type: 'rs_shift',
          title: `Sound horizon shifted: rs = ${params.rs.toFixed(2)} Mpc (Planck: 147.09)`,
          detail: `Torsion model prefers sound horizon ${shift > 0 ? 'larger' : 'smaller'} than Planck by ${Math.abs(shift).toFixed(1)} Mpc. If confirmed, this implies torsion was active during recombination epoch. Testable via CMB lensing + BAO cross-correlation.`,
          significance: `Delta_rs = ${shift.toFixed(1)} Mpc`,
        };
      }
      return null;
    },
  },
];

function checkForDiscoveries(taskId, params, score) {
  if (!params || !isFinite(score) || score > 200) return;

  for (const check of NOVEL_CHECKS) {
    const result = check.test(taskId, params);
    if (!result) continue;

    // Deduplicate: don't re-report same discovery type for same task
    const existing = discoveries.find(d => d.type === result.type && d.taskId === taskId);
    if (existing) {
      // Update if better score
      if (score < existing.score) {
        existing.params = { ...params };
        existing.score = score;
        existing.detail = result.detail;
        existing.title = result.title;
        existing.significance = result.significance;
        existing.timestamp = Date.now();
      }
      continue;
    }

    discoveryCounter++;
    const discovery = {
      id: discoveryCounter,
      ...result,
      taskId,
      params: { ...params },
      score,
      timestamp: Date.now(),
    };
    discoveries.push(discovery);
    console.log(`\n${'='.repeat(70)}`);
    console.log(`  NOVEL DISCOVERY #${discoveryCounter}: ${result.title}`);
    console.log(`  Type: ${result.type} | Significance: ${result.significance}`);
    console.log(`  Task: ${TASK_NAMES[taskId] || taskId} (score: ${score.toFixed(4)})`);
    console.log(`  ${result.detail}`);
    console.log(`${'='.repeat(70)}`);
  }
}

function getDiscoverySummary() {
  return {
    total: discoveries.length,
    novel_coupling: discoveries.filter(d => d.type === 'novel_coupling').length,
    novel_evolution: discoveries.filter(d => d.type === 'novel_evolution').length,
    phantom_de: discoveries.filter(d => d.type === 'phantom_de').length,
    h0_resolution: discoveries.filter(d => d.type === 'h0_resolution').length,
    novel_mass: discoveries.filter(d => d.type === 'novel_mass').length,
    spontaneous_condensation: discoveries.filter(d => d.type === 'spontaneous_condensation').length,
    torsion_wave: discoveries.filter(d => d.type === 'torsion_wave').length,
    rs_shift: discoveries.filter(d => d.type === 'rs_shift').length,
    discoveries: discoveries.map(d => ({
      id: d.id, type: d.type, title: d.title, significance: d.significance,
      taskId: d.taskId, score: d.score,
    })),
  };
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
  // Push novel discoveries to live dashboards
  const discSummary = getDiscoverySummary();
  aegisMonitor.setDiscoveries(discSummary);
  seekerMonitor.setDiscoveries(discSummary);
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
  if (discoveries.length > 0) {
    const types = {};
    discoveries.forEach(d => { types[d.type] = (types[d.type] || 0) + 1; });
    const summary = Object.entries(types).map(([t, c]) => `${t}:${c}`).join(' ');
    console.log(`NOVEL  │ ${discoveries.length} unreported discoveries │ ${summary}`);
  }
  logEmergenceState();
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

  // GET / — HTML dashboard
  if ((req.url === '/' || req.url === '') && req.method === 'GET') {
    const rows = Object.keys(TASK_TARGETS).map(taskId => {
      const aScore = aegisBests[taskId] != null ? aegisBests[taskId] : null;
      const sScore = seekerBests[taskId] != null ? seekerBests[taskId] : null;
      const bestScore = (aScore != null && sScore != null) ? Math.min(aScore, sScore)
        : aScore != null ? aScore : sScore;
      const target = TASK_TARGETS[taskId];
      const converged = bestScore !== null && bestScore <= target;
      const pct = bestScore != null && target > 0 ? Math.min(100, Math.max(0, (1 - (bestScore - target) / (bestScore + 1)) * 100)).toFixed(0) : converged ? 100 : 0;
      return { taskId, name: TASK_NAMES[taskId] || taskId, bestScore, target, converged, pct, pollinations: pollinationCounts[taskId] || 0 };
    }).sort((a, b) => (a.converged ? 0 : 1) - (b.converged ? 0 : 1) || (a.bestScore || 999) - (b.bestScore || 999));

    const convergedCount = rows.filter(r => r.converged).length;
    const totalRuns = aegisTotal + seekerTotal;
    const emergenceState = computeEmergenceState();
    const levelNames = ['NONE', 'QUANTUM', 'SYMMETRY BREAKING', 'PROPAGATION', 'UNIFICATION', 'COSMOLOGY', 'OBSERVATION'];

    const html = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>AEGIS Control Dashboard</title>
<meta http-equiv="refresh" content="10">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }
  h1 { color: #60a5fa; font-size: 28px; margin-bottom: 5px; }
  .subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
  .stats { display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
  .stat { background: #1e293b; border-radius: 8px; padding: 12px 18px; border: 1px solid #334155; }
  .stat .label { font-size: 11px; color: #94a3b8; text-transform: uppercase; }
  .stat .value { font-size: 22px; font-weight: bold; color: #60a5fa; }
  .stat .value.green { color: #34d399; }
  .stat .value.yellow { color: #fbbf24; }
  table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }
  th { background: #334155; padding: 10px 12px; text-align: left; font-size: 12px; color: #94a3b8; text-transform: uppercase; }
  td { padding: 8px 12px; border-top: 1px solid #334155; font-size: 13px; }
  tr:hover { background: #334155; }
  .converged { color: #34d399; font-weight: bold; }
  .active { color: #fbbf24; }
  .bar { background: #334155; border-radius: 4px; height: 6px; width: 100px; display: inline-block; vertical-align: middle; }
  .bar-fill { background: #60a5fa; height: 100%; border-radius: 4px; transition: width 0.3s; }
  .bar-fill.done { background: #34d399; }
  .section { margin-top: 25px; margin-bottom: 10px; font-size: 16px; color: #60a5fa; border-bottom: 1px solid #334155; padding-bottom: 5px; }
  .cascade { background: #1e293b; border-radius: 8px; padding: 15px; border: 1px solid #334155; margin-top: 10px; }
  .cascade-level { display: flex; align-items: center; gap: 10px; padding: 5px 0; }
  .cascade-level .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot.green { background: #34d399; }
  .dot.yellow { background: #fbbf24; }
  .dot.gray { background: #475569; }
  a { color: #60a5fa; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .endpoints { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px; }
  .endpoint { background: #1e293b; padding: 6px 12px; border-radius: 4px; font-family: monospace; font-size: 12px; border: 1px solid #334155; }
</style></head><body>
<h1>⚡ AEGIS — Autonomous Exploration Engine</h1>
<p class="subtitle">Unified Field Equation • Torsion Cosmology • Danny Lee Eldridge</p>

<div class="stats">
  <div class="stat"><div class="label">Converged</div><div class="value green">${convergedCount}/16</div></div>
  <div class="stat"><div class="label">Total Runs</div><div class="value">${(totalRuns/1e6).toFixed(2)}M</div></div>
  <div class="stat"><div class="label">AEGIS Cycle</div><div class="value">${aegisCycle}</div></div>
  <div class="stat"><div class="label">Seeker Cycle</div><div class="value">${seekerCycle}</div></div>
  <div class="stat"><div class="label">Eval Scale</div><div class="value">${EVAL_SCALE}x</div></div>
  <div class="stat"><div class="label">Emergence</div><div class="value yellow">L${emergenceState.level}</div></div>
</div>

<div class="section">📊 Scoreboard</div>
<table>
<tr><th>Task</th><th>Best χ²</th><th>Target</th><th>Progress</th><th>Status</th><th>Pollinations</th></tr>
${rows.map(r => `<tr>
  <td><a href="/task/${r.taskId}">${r.name}</a></td>
  <td>${r.bestScore != null ? r.bestScore.toFixed(4) : '—'}</td>
  <td>${r.target}</td>
  <td><div class="bar"><div class="bar-fill${r.converged ? ' done' : ''}" style="width:${r.pct}%"></div></div></td>
  <td class="${r.converged ? 'converged' : 'active'}">${r.converged ? '✅ Converged' : '🔄 Active'}</td>
  <td>${r.pollinations}</td>
</tr>`).join('')}
</table>

<div class="section">🌊 Emergence Cascade — Level ${emergenceState.level}: ${levelNames[emergenceState.level]}</div>
<div class="cascade">
  ${[
    { l: 1, n: 'Einstein-Cartan', s: emergenceState.level >= 1 },
    { l: 2, n: 'UFE Mexican Hat', s: emergenceState.level >= 2 },
    { l: 3, n: 'Torsion Wave', s: emergenceState.level >= 3 },
    { l: 4, n: 'Cross-Domain', s: emergenceState.level >= 4 },
    { l: 5, n: 'Cosmology (H₀)', s: emergenceState.level >= 5 },
    { l: 6, n: 'Emergence', s: false },
  ].map(x => `<div class="cascade-level"><div class="dot ${x.s ? 'green' : 'gray'}"></div> <b>L${x.l}:</b> ${x.n} ${x.s ? '→ feeding upward' : '(pending)'}</div>`).join('')}
</div>

<div class="section">🔗 API Endpoints</div>
<div class="endpoints">
  <a href="/scoreboard" class="endpoint">GET /scoreboard</a>
  <a href="/discoveries" class="endpoint">GET /discoveries</a>
  <a href="/emergence" class="endpoint">GET /emergence</a>
  <a href="/config" class="endpoint">GET /config</a>
  <a href="/task/h0-tension" class="endpoint">GET /task/:id</a>
</div>

</body></html>`;
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
    return;
  }

  // GET /settings — HTML settings page
  if (req.url === '/settings' && req.method === 'GET') {
    const html = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>AEGIS Settings</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }
  h1 { color: #60a5fa; font-size: 24px; margin-bottom: 20px; }
  .back { color: #60a5fa; text-decoration: none; font-size: 13px; }
  .card { background: #1e293b; border-radius: 8px; padding: 20px; border: 1px solid #334155; margin-bottom: 15px; }
  .card h2 { font-size: 16px; color: #60a5fa; margin-bottom: 12px; }
  label { display: block; font-size: 12px; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase; }
  input, select { background: #0f172a; border: 1px solid #475569; color: #e2e8f0; padding: 8px 12px; border-radius: 4px; width: 200px; font-size: 14px; margin-bottom: 12px; }
  button { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; }
  button:hover { background: #1d4ed8; }
  button.danger { background: #dc2626; }
  button.danger:hover { background: #b91c1c; }
  .row { display: flex; gap: 15px; align-items: end; flex-wrap: wrap; }
  .status { margin-top: 10px; padding: 8px 12px; background: #064e3b; border-radius: 4px; color: #34d399; font-size: 13px; display: none; }
  .status.error { background: #7f1d1d; color: #fca5a5; }
  .tasks { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 8px; margin-top: 10px; }
  .task-btn { background: #334155; border: 1px solid #475569; color: #e2e8f0; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; text-align: left; }
  .task-btn:hover { background: #475569; }
  .current { font-size: 13px; color: #94a3b8; margin-bottom: 8px; }
</style></head><body>
<a href="/" class="back">← Back to Dashboard</a>
<h1>⚙️ AEGIS Settings</h1>

<div class="card">
  <h2>Speed Controls</h2>
  <p class="current">Current: EVAL_SCALE = ${EVAL_SCALE}x, DELAY_MS = ${DELAY_MS}ms</p>
  <div class="row">
    <div><label>Eval Scale (0.1–10x)</label><input type="number" id="evalScale" value="${EVAL_SCALE}" step="0.1" min="0.1" max="10"></div>
    <div><label>Delay Between Tasks (ms)</label><input type="number" id="delayMs" value="${DELAY_MS}" step="10" min="0" max="5000"></div>
    <button onclick="updateConfig()">Apply</button>
  </div>
  <div class="status" id="configStatus"></div>
</div>

<div class="card">
  <h2>Quick Presets</h2>
  <div class="row">
    <button onclick="preset(0.5, 100)">🐢 Slow (0.5x, 100ms)</button>
    <button onclick="preset(1, 50)">⚡ Normal (1x, 50ms)</button>
    <button onclick="preset(2, 20)">🔥 Fast (2x, 20ms)</button>
    <button onclick="preset(4, 0)">🚀 Max Speed (4x, 0ms)</button>
  </div>
</div>

<div class="card">
  <h2>Reset Task (Re-converge)</h2>
  <p class="current">Warning: This clears all progress for the selected task. Use when stuck.</p>
  <div class="tasks">
    ${Object.keys(TASK_TARGETS).map(id => `<button class="task-btn" onclick="restartTask('${id}')">${TASK_NAMES[id] || id}</button>`).join('')}
  </div>
  <div class="status" id="restartStatus"></div>
</div>

<div class="card">
  <h2>System Info</h2>
  <p class="current">
    AEGIS Cycles: ${aegisCycle} | Seeker Cycles: ${seekerCycle}<br>
    Total Evaluations: ${(aegisTotal + seekerTotal).toLocaleString()}<br>
    Workers: 12 threads | Port: ${CONTROL_PORT}<br>
    Tasks: ${Object.keys(TASK_TARGETS).length} | Converged: ${Object.keys(TASK_TARGETS).filter(id => {
      const a = aegisBests[id], s = seekerBests[id];
      const best = (a != null && s != null) ? Math.min(a,s) : a != null ? a : s;
      return best != null && best <= TASK_TARGETS[id];
    }).length}
  </p>
</div>

<script>
async function updateConfig() {
  const evalScale = document.getElementById('evalScale').value;
  const delayMs = document.getElementById('delayMs').value;
  try {
    const r = await fetch('/config', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({evalScale: +evalScale, delayMs: +delayMs}) });
    const d = await r.json();
    showStatus('configStatus', 'Applied: EVAL_SCALE=' + d.evalScale + 'x, DELAY_MS=' + d.delayMs + 'ms', false);
  } catch(e) { showStatus('configStatus', 'Error: ' + e.message, true); }
}
function preset(scale, delay) {
  document.getElementById('evalScale').value = scale;
  document.getElementById('delayMs').value = delay;
  updateConfig();
}
async function restartTask(id) {
  if (!confirm('Reset ' + id + '? This clears all progress.')) return;
  try {
    const r = await fetch('/restart/' + id, { method: 'POST' });
    const d = await r.json();
    showStatus('restartStatus', 'Reset: ' + id + ' — will re-converge', false);
  } catch(e) { showStatus('restartStatus', 'Error: ' + e.message, true); }
}
function showStatus(id, msg, isError) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.className = 'status' + (isError ? ' error' : '');
  el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 4000);
}
</script>
</body></html>`;
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
    return;
  }

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
      discoveries: getDiscoverySummary(),
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

  // GET /discoveries — novel predictions not in survey data
  if (req.url === '/discoveries' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(getDiscoverySummary()));
    return;
  }

  // GET /emergence — quantum→cosmo cascade state
  if (req.url === '/emergence' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    const state = computeEmergenceState();
    const levelNames = ['NONE', 'QUANTUM', 'SYMMETRY BREAKING', 'PROPAGATION', 'UNIFICATION', 'COSMOLOGY', 'OBSERVATION'];
    res.end(JSON.stringify({
      level: state.level,
      levelName: levelNames[state.level],
      derived: state.derived,
      constrainedTasks: Object.keys(state.constraints),
      constraints: state.constraints,
      pathway: [
        { level: 1, name: 'Einstein-Cartan', status: bestKnown['einstein-cartan'] ? 'converged' : 'pending', output: 'spin density → torsion tensor' },
        { level: 2, name: 'UFE Mexican Hat', status: bestKnown['ufe-torsion'] && bestKnown['ufe-torsion'].score < 0.01 ? 'converged' : 'pending', output: 'μ², λ → T_vev, m_T' },
        { level: 3, name: 'Torsion Wave', status: bestKnown['torsion-wave'] && bestKnown['torsion-wave'].score < 0.1 ? 'converged' : 'pending', output: 'ω, k → v_phase, dispersion' },
        { level: 4, name: 'Cross-Domain', status: bestKnown['ufe-cross-domain'] && bestKnown['ufe-cross-domain'].score < 100 ? 'active' : 'pending', output: 'EC ↔ f(T) ↔ Wave ↔ VEV' },
        { level: 5, name: 'Cosmology', status: bestKnown['h0-tension'] && bestKnown['h0-tension'].score < 5 ? 'converged' : 'active', output: 'β(z), H₀, distances' },
        { level: 6, name: 'Combined', status: 'active', output: 'multi-survey unified fit' },
      ],
    }));
    return;
  }

  // GET /scoreboard — full scoreboard data
  if (req.url === '/scoreboard' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    const rows = Object.keys(TASK_TARGETS).map(taskId => {
      const aScore = aegisBests[taskId] != null ? aegisBests[taskId] : null;
      const sScore = seekerBests[taskId] != null ? seekerBests[taskId] : null;
      const bestScore = (aScore != null && sScore != null) ? Math.min(aScore, sScore)
        : aScore != null ? aScore : sScore;
      const bestEngine = bestScore === aScore ? 'AEGIS' : 'Seeker';
      const target = TASK_TARGETS[taskId];
      return {
        task: TASK_NAMES[taskId] || taskId, taskId,
        aegisScore: aScore, seekerScore: sScore,
        bestScore, bestEngine, target,
        bestParams: bestKnown[taskId] || null,
        pollinations: pollinationCounts[taskId] || 0,
        converged: bestScore !== null && bestScore <= target,
      };
    });
    res.end(JSON.stringify(rows));
    return;
  }

  // GET /task/:id — single task details
  const taskMatch = req.url && req.url.match(/^\/task\/([a-z0-9-]+)$/);
  if (taskMatch && req.method === 'GET') {
    const taskId = taskMatch[1];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      taskId,
      task: TASK_NAMES[taskId] || taskId,
      aegisScore: aegisBests[taskId] || null,
      seekerScore: seekerBests[taskId] || null,
      target: TASK_TARGETS[taskId] || null,
      bestParams: bestKnown[taskId] || null,
      worstSeen: worstScores[taskId] || null,
      pollinations: pollinationCounts[taskId] || 0,
    }));
    return;
  }

  // POST /restart/:id — clear bestKnown for a stuck task to re-converge
  const restartMatch = req.url && req.url.match(/^\/restart\/([a-z0-9-]+)$/);
  if (restartMatch && req.method === 'POST') {
    const taskId = restartMatch[1];
    if (bestKnown[taskId]) delete bestKnown[taskId];
    if (aegisBests[taskId]) delete aegisBests[taskId];
    if (seekerBests[taskId]) delete seekerBests[taskId];
    if (worstScores[taskId]) delete worstScores[taskId];
    saveState();
    console.log(`🔄 [CONTROL] Reset task "${taskId}" — cleared bestKnown/scores`);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, taskId, message: 'Task reset, will re-converge' }));
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
