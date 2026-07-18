#!/usr/bin/env node
/**
 * AEGIS Optimizer CLI
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Usage:
 *   npx @aegis/optimizer optimize --config task.json
 *   npx @aegis/optimizer dual --config task.json
 *   npx @aegis/optimizer benchmark
 *   npx @aegis/optimizer serve --port 3000
 */

const { optimize, dualOptimize, optimizeWithMonitor } = require('./index');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const command = args[0];

function getFlag(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

function hasFlag(name) {
  return args.includes(`--${name}`);
}

function printBanner() {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ⚡ AEGIS Optimizer CLI v1.0.0                               ║
║  The engine that discovered the Unified Field Equation.      ║
║  Copyright (c) 2012-2026 Danny Lee Eldridge.                 ║
╚═══════════════════════════════════════════════════════════════╝
`);
}

function printHelp() {
  printBanner();
  console.log(`Commands:
  optimize    Run single-engine optimization
  dual        Run dual-engine with cross-pollination
  monitor     Run with live web dashboard
  benchmark   Run built-in benchmark suite
  serve       Start SaaS API server

Options:
  --config <file>    JSON config file with objective & parameters
  --objective <fn>   Inline objective function (JS expression)
  --params <json>    Inline parameter definitions
  --evals <n>        Max evaluations (default: 1000)
  --cycles <n>       Optimization cycles for dual mode (default: 5)
  --port <n>         Dashboard/server port (default: 8080)
  --output <file>    Write results to JSON file
  --quiet            Suppress progress output

Examples:
  # From config file
  aegis optimize --config my-problem.json --output result.json

  # Inline objective
  aegis optimize --objective "(p) => (p.x-3)**2 + (p.y+2)**2" \\
    --params '[{"name":"x","min":-10,"max":10},{"name":"y","min":-10,"max":10}]'

  # Dual engine with dashboard
  aegis monitor --config my-problem.json --port 9000

  # Run benchmarks
  aegis benchmark

Config file format (task.json):
  {
    "objective": "(p) => yourFunction(p)",
    "parameters": [
      { "name": "x", "min": 0, "max": 100 },
      { "name": "y", "min": -50, "max": 50 }
    ],
    "maxEvals": 2000,
    "cycles": 10
  }
`);
}

function loadConfig() {
  const configFile = getFlag('config');
  if (configFile) {
    const raw = fs.readFileSync(path.resolve(configFile), 'utf8');
    const config = JSON.parse(raw);
    // Convert string objective to function
    if (typeof config.objective === 'string') {
      config.objective = new Function('return ' + config.objective)();
    }
    return config;
  }

  // Build from inline args
  const objStr = getFlag('objective');
  const paramsStr = getFlag('params');
  if (!objStr || !paramsStr) {
    console.error('Error: provide --config <file> or both --objective and --params');
    process.exit(1);
  }

  return {
    objective: new Function('return ' + objStr)(),
    parameters: JSON.parse(paramsStr),
    maxEvals: parseInt(getFlag('evals') || '1000'),
    cycles: parseInt(getFlag('cycles') || '5'),
  };
}

function formatResult(result) {
  const lines = [];
  lines.push('');
  lines.push('═══════════════════════════════════════════');
  lines.push('  OPTIMIZATION COMPLETE');
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
  if (result.phase) lines.push(`  Final Phase: ${result.phase}`);
  lines.push('═══════════════════════════════════════════');
  lines.push('');
  return lines.join('\n');
}

async function runOptimize() {
  const config = loadConfig();
  const quiet = hasFlag('quiet');

  if (!quiet) {
    printBanner();
    console.log('🔍 Running single-engine optimization...');
    console.log(`   Parameters: ${config.parameters.length}`);
    console.log(`   Max evals: ${config.maxEvals || 1000}`);
    console.log('');
  }

  const result = await optimize({
    objective: config.objective,
    parameters: config.parameters,
    maxEvals: config.maxEvals || 1000,
  });

  if (!quiet) console.log(formatResult(result));

  const output = getFlag('output');
  if (output) {
    fs.writeFileSync(path.resolve(output), JSON.stringify(result, null, 2));
    if (!quiet) console.log(`📁 Results saved to ${output}`);
  }

  return result;
}

async function runDual() {
  const config = loadConfig();
  const quiet = hasFlag('quiet');

  if (!quiet) {
    printBanner();
    console.log('🧬 Running dual-engine with cross-pollination...');
    console.log(`   Parameters: ${config.parameters.length}`);
    console.log(`   Cycles: ${config.cycles || 5}`);
    console.log('');
  }

  const result = await dualOptimize({
    objective: config.objective,
    parameters: config.parameters,
    maxEvals: config.maxEvals || 1000,
    cycles: config.cycles || 5,
  });

  if (!quiet) console.log(formatResult(result));

  const output = getFlag('output');
  if (output) {
    fs.writeFileSync(path.resolve(output), JSON.stringify(result, null, 2));
    if (!quiet) console.log(`📁 Results saved to ${output}`);
  }

  return result;
}

async function runMonitor() {
  const config = loadConfig();
  const port = parseInt(getFlag('port') || '8080');

  printBanner();
  console.log(`📊 Starting optimization with live dashboard on port ${port}...`);

  const result = await optimizeWithMonitor({
    objective: config.objective,
    parameters: config.parameters,
    maxEvals: config.maxEvals || 1000,
    port,
  });

  console.log(formatResult(result));
}

async function runBenchmark() {
  printBanner();
  console.log('🏎️  Running AEGIS Benchmark Suite\n');

  const benchmarks = [
    {
      name: 'Sphere (2D)',
      objective: (p) => p.x * p.x + p.y * p.y,
      parameters: [{ name: 'x', min: -10, max: 10 }, { name: 'y', min: -10, max: 10 }],
      target: 0,
      maxEvals: 500,
    },
    {
      name: 'Rosenbrock (2D)',
      objective: (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2),
      parameters: [{ name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }],
      target: 0,
      maxEvals: 2000,
    },
    {
      name: 'Rastrigin (5D)',
      objective: (p) => {
        let sum = 50;
        for (const k of Object.keys(p)) {
          const x = p[k];
          sum += x * x - 10 * Math.cos(2 * Math.PI * x);
        }
        return sum;
      },
      parameters: Array.from({ length: 5 }, (_, i) => ({ name: `x${i}`, min: -5.12, max: 5.12 })),
      target: 0,
      maxEvals: 5000,
    },
    {
      name: 'Ackley (3D)',
      objective: (p) => {
        const vals = Object.values(p);
        const n = vals.length;
        const sumSq = vals.reduce((s, x) => s + x * x, 0) / n;
        const sumCos = vals.reduce((s, x) => s + Math.cos(2 * Math.PI * x), 0) / n;
        return -20 * Math.exp(-0.2 * Math.sqrt(sumSq)) - Math.exp(sumCos) + 20 + Math.E;
      },
      parameters: Array.from({ length: 3 }, (_, i) => ({ name: `x${i}`, min: -5, max: 5 })),
      target: 0,
      maxEvals: 2000,
    },
    {
      name: 'Supply Chain (6D)',
      objective: (p) => {
        const holding = p.inventory * 2.5;
        const transport = p.routes * p.distance * 0.08;
        const labor = p.workers * 45;
        const waste = Math.max(0, p.inventory - p.demand) * 12;
        const shortage = Math.max(0, p.demand - p.inventory) * 50;
        return holding + transport + labor + waste + shortage;
      },
      parameters: [
        { name: 'inventory', min: 100, max: 10000 },
        { name: 'routes', min: 1, max: 50 },
        { name: 'distance', min: 10, max: 500 },
        { name: 'workers', min: 5, max: 200 },
        { name: 'demand', min: 500, max: 8000 },
        { name: 'price', min: 10, max: 200 },
      ],
      target: null,
      maxEvals: 3000,
    },
  ];

  const results = [];

  for (const bench of benchmarks) {
    process.stdout.write(`  ${bench.name.padEnd(25)}`);
    const start = Date.now();

    const singleResult = await optimize({
      objective: bench.objective,
      parameters: bench.parameters,
      maxEvals: bench.maxEvals,
    });

    const dualResult = await dualOptimize({
      objective: bench.objective,
      parameters: bench.parameters,
      maxEvals: bench.maxEvals,
      cycles: 3,
    });

    const singleTime = Date.now() - start;
    const sScore = singleResult.best ? singleResult.best.score : Infinity;
    const dScore = dualResult.best ? dualResult.best.score : Infinity;
    const improvement = sScore > 0 ? ((sScore - dScore) / sScore * 100).toFixed(0) : '∞';

    results.push({ name: bench.name, single: sScore, dual: dScore, improvement, time: singleTime });

    console.log(`Single: ${sScore.toFixed(6).padStart(12)} | Dual: ${dScore.toFixed(6).padStart(12)} | Δ ${improvement}%`);
  }

  console.log('\n═══════════════════════════════════════════════════════════════════');
  console.log('  BENCHMARK RESULTS SUMMARY');
  console.log('═══════════════════════════════════════════════════════════════════');
  console.log(`  ${'Problem'.padEnd(25)} ${'Single'.padStart(12)} ${'Dual'.padStart(12)} ${'Improvement'.padStart(12)}`);
  console.log('  ' + '─'.repeat(63));
  for (const r of results) {
    console.log(`  ${r.name.padEnd(25)} ${r.single.toFixed(6).padStart(12)} ${r.dual.toFixed(6).padStart(12)} ${(r.improvement + '%').padStart(12)}`);
  }
  console.log('═══════════════════════════════════════════════════════════════════\n');

  const output = getFlag('output');
  if (output) {
    fs.writeFileSync(path.resolve(output), JSON.stringify(results, null, 2));
    console.log(`📁 Benchmark results saved to ${output}`);
  }
}

async function runServe() {
  const port = parseInt(getFlag('port') || '3000');
  process.env.PORT = String(port);
  printBanner();
  console.log(`🚀 Starting SaaS API server on port ${port}...`);
  require('../saas/server');
}

// ── Main dispatch ────────────────────────────────────────────────────────────

(async () => {
  try {
    switch (command) {
      case 'optimize':
      case 'run':
        await runOptimize();
        break;
      case 'dual':
      case 'dual-optimize':
        await runDual();
        break;
      case 'monitor':
      case 'dashboard':
        await runMonitor();
        break;
      case 'benchmark':
      case 'bench':
        await runBenchmark();
        break;
      case 'serve':
      case 'server':
      case 'api':
        await runServe();
        break;
      case 'help':
      case '--help':
      case '-h':
        printHelp();
        break;
      case 'version':
      case '--version':
      case '-v':
        console.log('AEGIS Optimizer v1.0.0');
        break;
      default:
        printHelp();
        break;
    }
  } catch (err) {
    console.error(`\n❌ Error: ${err.message}`);
    process.exit(1);
  }
})();
