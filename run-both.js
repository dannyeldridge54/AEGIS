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

// ═══════════════════════════════════════════════════════════════════════════════
// THE SPECTRUM — ordered from pure exploration (index 0) to pure exploitation
// ═══════════════════════════════════════════════════════════════════════════════

const spectrum = [
  // ── Tier 1: Maximum Exploration ───────────────────────────────────────────
  {
    tag: 'chaos-scan',
    config: { maxEvals: 1500, explorationRate: 0.95, strategies: ['random', 'curiosity'] },
    desc: 'Pure random + curiosity, nearly zero exploitation',
  },
  {
    tag: 'wide-swarm',
    config: { maxEvals: 3000, explorationRate: 0.85, strategies: ['swarm', 'curiosity', 'random'] },
    desc: 'Swarm-driven wide search with curiosity bias',
  },
  {
    tag: 'evo-explore',
    config: { maxEvals: 2500, explorationRate: 0.75, strategies: ['evolutionary', 'swarm', 'curiosity', 'random'] },
    desc: 'Evolutionary with strong exploration pressure',
  },

  // ── Tier 2: Exploration-Leaning ───────────────────────────────────────────
  {
    tag: 'diverse-mix',
    config: { maxEvals: 2000, explorationRate: 0.65, strategies: ['evolutionary', 'swarm', 'random', 'annealing'] },
    desc: 'Diverse strategy mix with exploration lean',
  },
  {
    tag: 'annealing-hot',
    config: { maxEvals: 2500, explorationRate: 0.60, strategies: ['annealing', 'swarm', 'curiosity'] },
    desc: 'High-temperature annealing, lots of jumps',
  },

  // ── Tier 3: Balanced ──────────────────────────────────────────────────────
  {
    tag: 'balanced',
    config: { maxEvals: 2000, explorationRate: 0.50 },
    desc: 'All strategies, 50/50 explore-exploit balance',
  },
  {
    tag: 'full-suite-deep',
    config: { maxEvals: 5000, explorationRate: 0.50 },
    desc: 'All strategies, balanced, high eval budget',
  },

  // ── Tier 4: Exploitation-Leaning ──────────────────────────────────────────
  {
    tag: 'bayesian-refine',
    config: { maxEvals: 3000, explorationRate: 0.35, strategies: ['bayesian', 'gradient', 'annealing', 'exploit'] },
    desc: 'Surrogate-guided with gradient refinement',
  },
  {
    tag: 'gradient-anneal',
    config: { maxEvals: 2500, explorationRate: 0.25, strategies: ['gradient', 'annealing', 'exploit'] },
    desc: 'Gradient descent + cold annealing',
  },

  // ── Tier 5: Maximum Exploitation ──────────────────────────────────────────
  {
    tag: 'surgical-exploit',
    config: { maxEvals: 4000, explorationRate: 0.10, strategies: ['gradient', 'bayesian', 'exploit'] },
    desc: 'Surgical precision, minimal exploration',
  },
  {
    tag: 'pure-refine',
    config: { maxEvals: 8000, explorationRate: 0.05, strategies: ['gradient', 'exploit'] },
    desc: 'Pure gradient refinement, maximum budget',
  },
];

const SPECTRUM_LEN = spectrum.length;

// ═══════════════════════════════════════════════════════════════════════════════
// TASK SETS — ordered by difficulty/dimensionality (easy → hard)
// ═══════════════════════════════════════════════════════════════════════════════

function makeTask(id, name, evalFn, dim, range, optimum = 0) {
  const params = [];
  for (let i = 0; i < dim; i++) params.push({ name: `x${i}`, min: -range, max: range });
  return { id, name, evaluate: evalFn, parameters: params, optimum };
}

const rosenbrock = (dim, range = 5) => makeTask(
  `rosenbrock-${dim}d${range !== 5 ? `-r${range}` : ''}`,
  `Rosenbrock ${dim}D${range !== 5 ? ` [±${range}]` : ''}`,
  (p) => {
    const k = Object.keys(p); let s = 0;
    for (let i = 0; i < k.length - 1; i++) {
      s += 100 * Math.pow(p[k[i + 1]] - p[k[i]] * p[k[i]], 2) + Math.pow(1 - p[k[i]], 2);
    }
    return s;
  }, dim, range
);

const rastrigin = (dim, range = 5.12) => makeTask(
  `rastrigin-${dim}d${range !== 5.12 ? `-r${range}` : ''}`,
  `Rastrigin ${dim}D${range !== 5.12 ? ` [±${range}]` : ''}`,
  (p) => {
    const k = Object.keys(p);
    return 10 * k.length + k.reduce((s, ki) => s + p[ki] * p[ki] - 10 * Math.cos(2 * Math.PI * p[ki]), 0);
  }, dim, range
);

const ackley = (dim, range = 5) => makeTask(
  `ackley-${dim}d${range !== 5 ? `-r${range}` : ''}`,
  `Ackley ${dim}D${range !== 5 ? ` [±${range}]` : ''}`,
  (p) => {
    const k = Object.keys(p), n = k.length;
    const s1 = k.reduce((s, ki) => s + p[ki] * p[ki], 0);
    const s2 = k.reduce((s, ki) => s + Math.cos(2 * Math.PI * p[ki]), 0);
    return -20 * Math.exp(-0.2 * Math.sqrt(s1 / n)) - Math.exp(s2 / n) + 20 + Math.E;
  }, dim, range
);

const sphere = (dim) => makeTask(
  `sphere-${dim}d`, `Sphere ${dim}D`,
  (p) => Object.values(p).reduce((s, v) => s + v * v, 0),
  dim, 5.12
);

const schwefel = (dim) => makeTask(
  `schwefel-${dim}d`, `Schwefel ${dim}D`,
  (p) => {
    const k = Object.keys(p);
    return 418.9829 * k.length - k.reduce((s, ki) => s + p[ki] * Math.sin(Math.sqrt(Math.abs(p[ki]))), 0);
  }, dim, 500
);

const griewank = (dim) => makeTask(
  `griewank-${dim}d`, `Griewank ${dim}D`,
  (p) => {
    const k = Object.keys(p);
    const s = k.reduce((a, ki) => a + p[ki] * p[ki], 0);
    const c = k.reduce((a, ki, i) => a * Math.cos(p[ki] / Math.sqrt(i + 1)), 1);
    return 1 + s / 4000 - c;
  }, dim, 600
);

const styblinskiTang = (dim) => makeTask(
  `styblinski-${dim}d`, `Styblinski-Tang ${dim}D`,
  (p) => {
    const k = Object.keys(p);
    return k.reduce((s, ki) => s + (Math.pow(p[ki], 4) - 16 * p[ki] * p[ki] + 5 * p[ki]) / 2, 0) + 39.16599 * k.length;
  }, dim, 5
);

const levyN13 = () => ({
  id: 'levy-n13', name: 'Levy N.13', optimum: 0,
  parameters: [{ name: 'x0', min: -10, max: 10 }, { name: 'x1', min: -10, max: 10 }],
  evaluate: (p) => {
    const x = p.x0, y = p.x1;
    return Math.pow(Math.sin(3 * Math.PI * x), 2) +
      Math.pow(x - 1, 2) * (1 + Math.pow(Math.sin(3 * Math.PI * y), 2)) +
      Math.pow(y - 1, 2) * (1 + Math.pow(Math.sin(2 * Math.PI * y), 2));
  },
});

// Ordered: small/easy → large/hard
// 50/50 split: torsion tasks interleaved with benchmarks at every difficulty tier
const tasksByDifficulty = [
  // ── Easy tier ─────────────────────────────────────────────────────────────
  sphere(2),
  aegis.einsteinCartanTask,                          // EC — small param space
  rosenbrock(2),
  aegis.fTGravityTask,                               // f(T) — 5 params, well-constrained
  levyN13(),
  aegis.ufeTorsionTask,                              // UFE Mexican hat — 8 params

  // ── Medium tier ───────────────────────────────────────────────────────────
  ackley(3),
  aegis.torsionWaveTask,                             // Wave dispersion — 7 params
  rosenbrock(5),
  aegis.crossDomainTask,                             // Cross-domain unified — 10 params
  styblinskiTang(3),
  aegis.einsteinCartanTask,                          // EC again with different spectrum slot
  rastrigin(3),
  aegis.fTGravityTask,                               // f(T) again

  // ── Hard tier ─────────────────────────────────────────────────────────────
  ackley(5),
  aegis.ufeTorsionTask,                              // UFE again — harder spectrum profile
  rastrigin(5),
  aegis.torsionWaveTask,                             // Wave again
  rosenbrock(10),
  aegis.crossDomainTask,                             // Cross-domain again

  // ── Extreme tier ──────────────────────────────────────────────────────────
  sphere(20),
  aegis.crossDomainTask,                             // Cross-domain — most budget here
  ackley(8),
  aegis.ufeTorsionTask,                              // UFE — third pass, extreme exploitation
  rastrigin(10),
  aegis.einsteinCartanTask,                          // EC — extreme
  schwefel(5),
  aegis.fTGravityTask,                               // f(T) — extreme
  griewank(5),
  aegis.torsionWaveTask,                             // Wave — extreme
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
    const significant = anomalies.filter(a => a.significance === 'high');

    if (significant.length > 0) {
      console.log(`\n🌌 [${engine}] ${runId} — ${significant.length} HIGH-SIGNIFICANCE spatial anomalies:`);
      for (const a of significant) {
        console.log(`   📍 z=${a.redshift.toFixed(3)} | ${a.survey} | RA ${a.ra} Dec ${a.dec}`);
        console.log(`      ${a.type}: Δ=${a.deviation_sigma.toFixed(1)}σ | ${a.field_description}`);
        console.log(`      d=${a.comoving_Mpc.toFixed(0)} Mpc | lookback ${a.lookback_Gyr.toFixed(1)} Gyr | ref: ${a.reference}`);
      }

      // Register as alert
      monitor.registerAlert({
        id: `spatial-${runId}`,
        title: `${significant.length} sky anomalies from ${runId}`,
        severity: 'critical',
        category: 'anomaly',
        detail: significant.map(a => `z=${a.redshift.toFixed(3)} ${a.survey} ${a.type} ${a.deviation_sigma.toFixed(1)}σ`).join('; '),
        data: { anomalyCount: significant.length, topAnomaly: significant[0] },
      });
    }
  } catch (e) {
    // Silent — don't crash the runner
  }
}

function logEquation(engine, runId, taskId, bestParams, bestScore, writer) {
  try {
    if (!writer || !bestParams) return;
    // Only for torsion tasks with good scores
    if (!taskId.match(/ufe-torsion|cross-domain|ft-gravity|einstein-cartan|torsion-wave/)) return;
    if (bestScore > 500) return; // only log good results

    const eq = writer.synthesize(taskId, bestParams, bestScore);
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

async function runAegisLoop() {
  while (true) {
    aegisCycle++;
    // AEGIS: odd cycles start from exploration, even from exploitation
    const fromExploration = aegisCycle % 2 === 1;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[AEGIS] ━━ Cycle ${aegisCycle} ━━ ${direction} ━━ ${queue.length} runs`);

    for (const { task, profile } of queue) {
      aegisTotal++;
      const runId = `aegis-${task.id}-${profile.tag}-c${aegisCycle}`;
      const runName = `AEGIS: ${task.name} [${profile.tag}]`;

      aegisMonitor.registerRun(runId, runName);
      const agent = new aegis.AegisAgent(task, {
        ...profile.config,
        seed: aegisTotal * 1000 + Date.now() % 10000,
        verbosity: 'silent',
      });
      agent.on(aegisMonitor.createHandler(runId));

      try {
        const result = await agent.run(task.optimum);
        // Log spatial anomalies + equations for torsion runs
        const snap = aegisMonitor.getRunSnapshot ? aegisMonitor.getRunSnapshot(runId) : null;
        const bp = snap?.bestParams || (result && result.bestParams);
        const bs = snap?.bestScore ?? (result && result.bestScore);
        if (bp && task.id.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('AEGIS', runId, bp, aegisMonitor);
          logEquation('AEGIS', runId, task.id, bp, bs, aegisWriter);
        }
      } catch (err) {
        console.error(`[AEGIS] Error: ${task.name} [${profile.tag}]: ${err.message}`);
      }
      await new Promise(r => setTimeout(r, 800));
    }
    console.log(`[AEGIS] Cycle ${aegisCycle} done — ${aegisTotal} lifetime runs`);
  }
}

async function runSeekerLoop() {
  while (true) {
    seekerCycle++;
    // Seeker: odd cycles start from exploitation (opposite of AEGIS), even from exploration
    const fromExploration = seekerCycle % 2 === 0;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[Seeker] ━━ Cycle ${seekerCycle} ━━ ${direction} ━━ ${queue.length} runs`);

    for (const { task, profile } of queue) {
      seekerTotal++;
      const runId = `seeker-${task.id}-${profile.tag}-c${seekerCycle}`;
      const runName = `Seeker: ${task.name} [${profile.tag}]`;

      seekerMonitor.registerRun(runId, runName);
      const agent = new seeker.SeekerAgent(task, {
        ...profile.config,
        seed: seekerTotal * 2000 + Date.now() % 10000,
        verbosity: 'silent',
      });
      agent.on(seekerMonitor.createHandler(runId));

      try {
        const result = await agent.run(task.optimum);
        const snap = seekerMonitor.getRunSnapshot ? seekerMonitor.getRunSnapshot(runId) : null;
        const bp = snap?.bestParams || (result && result.bestParams);
        const bs = snap?.bestScore ?? (result && result.bestScore);
        if (bp && task.id.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('Seeker', runId, bp, seekerMonitor);
          logEquation('Seeker', runId, task.id, bp, bs, seekerWriter);
        }
      } catch (err) {
        console.error(`[Seeker] Error: ${task.name} [${profile.tag}]: ${err.message}`);
      }
      await new Promise(r => setTimeout(r, 800));
    }
    console.log(`[Seeker] Cycle ${seekerCycle} done — ${seekerTotal} lifetime runs`);
  }
}

// Status printer
setInterval(() => {
  const aegisDir = aegisCycle % 2 === 1 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  const seekerDir = seekerCycle % 2 === 0 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  console.log(`\n${'━'.repeat(70)}`);
  console.log(`AEGIS  │ cycle ${aegisCycle} (${aegisDir}) │ ${aegisTotal} total runs`);
  console.log(`Seeker │ cycle ${seekerCycle} (${seekerDir}) │ ${seekerTotal} total runs`);
  aegisMonitor.printStatus();
  seekerMonitor.printStatus();
}, 60000);

Promise.all([runAegisLoop(), runSeekerLoop()]).catch(err => {
  console.error('Fatal error:', err);
});

process.on('SIGINT', () => {
  console.log('\nShutting down...');
  aegisMonitor.stopDashboard();
  seekerMonitor.stopDashboard();
  process.exit(0);
});
