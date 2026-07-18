/**
 * AEGIS + Seeker — 24/7 Dual Runner with Live Monitoring
 * Runs both engines continuously with live dashboards.
 * Now includes torsion field theory optimization.
 *
 * AEGIS Monitor: http://localhost:5555
 * Seeker Monitor: http://localhost:5556
 */

const aegis = require('./dist/index.js');
const seeker = require('./seeker/dist/index.js');

// ─── Standard Benchmark Tasks ────────────────────────────────────────────────

const standardTasks = [
  {
    id: 'rosenbrock', name: 'Rosenbrock 2D',
    evaluate: (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2),
    parameters: [{ name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }],
    optimum: 0,
  },
  {
    id: 'rastrigin', name: 'Rastrigin 5D',
    evaluate: (p) => {
      const A = 10, keys = Object.keys(p);
      return A * keys.length + keys.reduce((s, k) => s + p[k] * p[k] - A * Math.cos(2 * Math.PI * p[k]), 0);
    },
    parameters: [
      { name: 'x1', min: -5.12, max: 5.12 }, { name: 'x2', min: -5.12, max: 5.12 },
      { name: 'x3', min: -5.12, max: 5.12 }, { name: 'x4', min: -5.12, max: 5.12 },
      { name: 'x5', min: -5.12, max: 5.12 },
    ],
    optimum: 0,
  },
  {
    id: 'ackley', name: 'Ackley 3D',
    evaluate: (p) => {
      const keys = Object.keys(p), n = keys.length;
      const sum1 = keys.reduce((s, k) => s + p[k] * p[k], 0);
      const sum2 = keys.reduce((s, k) => s + Math.cos(2 * Math.PI * p[k]), 0);
      return -20 * Math.exp(-0.2 * Math.sqrt(sum1 / n)) - Math.exp(sum2 / n) + 20 + Math.E;
    },
    parameters: [
      { name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }, { name: 'z', min: -5, max: 5 },
    ],
    optimum: 0,
  },
];

// ─── Torsion Tasks (loaded from the torsion module) ──────────────────────────

const torsionTasks = [
  aegis.einsteinCartanTask,
  aegis.fTGravityTask,
  aegis.ufeTorsionTask,
  aegis.torsionWaveTask,
];

const allTasks = [...standardTasks, ...torsionTasks];

// ─── Launch ──────────────────────────────────────────────────────────────────

console.log(`
╔═══════════════════════════════════════════════════════════════════╗
║       _    _____ ____ ___ ____                                   ║
║      / \\  | ____/ ___|_ _/ ___|                                  ║
║     / _ \\ |  _|| |  _ | |\\___ \\   +  Seeker                      ║
║    / ___ \\| |__| |_| || | ___) |     Discovery Engine            ║
║   /_/   \\_\\_____\\____|___|____/                                  ║
║                                                                   ║
║   24/7 Dual Engine — Live Monitoring + Torsion Field Theory      ║
║                                                                   ║
║   AEGIS  Monitor: http://localhost:5555                           ║
║   Seeker Monitor: http://localhost:5556                           ║
║                                                                   ║
║   Tasks: Rosenbrock | Rastrigin | Ackley                         ║
║          Einstein-Cartan | f(T) Gravity | UFE Torsion | Waves    ║
╚═══════════════════════════════════════════════════════════════════╝
`);

const aegisMonitor = aegis.createMonitor({ port: 5555 });
const seekerMonitor = seeker.createMonitor({ port: 5556 });

aegisMonitor.startDashboard();
seekerMonitor.startDashboard();

let aegisRun = 0;
let seekerRun = 0;

async function runAegisLoop() {
  while (true) {
    for (const task of allTasks) {
      aegisRun++;
      const runId = `aegis-${task.id}-${aegisRun}`;
      const runName = `AEGIS: ${task.name} #${aegisRun}`;

      aegisMonitor.registerRun(runId, runName);
      const agent = new aegis.AegisAgent(task, {
        maxEvals: 2000,
        seed: aegisRun * 1000 + Date.now() % 1000,
        verbosity: 'silent',
      });
      agent.on(aegisMonitor.createHandler(runId));

      await agent.run(task.optimum);
      await new Promise(r => setTimeout(r, 2000));
    }
  }
}

async function runSeekerLoop() {
  while (true) {
    for (const task of allTasks) {
      seekerRun++;
      const runId = `seeker-${task.id}-${seekerRun}`;
      const runName = `Seeker: ${task.name} #${seekerRun}`;

      seekerMonitor.registerRun(runId, runName);
      const agent = new seeker.SeekerAgent(task, {
        maxEvals: 2000,
        seed: seekerRun * 2000 + Date.now() % 1000,
        verbosity: 'silent',
      });
      agent.on(seekerMonitor.createHandler(runId));

      await agent.run(task.optimum);
      await new Promise(r => setTimeout(r, 2000));
    }
  }
}

// Status printer — every 60 seconds
setInterval(() => {
  console.log('\n' + '='.repeat(70));
  aegisMonitor.printStatus();
  seekerMonitor.printStatus();
}, 60000);

// Launch both engines
Promise.all([runAegisLoop(), runSeekerLoop()]).catch(err => {
  console.error('Fatal error:', err);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  aegisMonitor.stopDashboard();
  seekerMonitor.stopDashboard();
  process.exit(0);
});
