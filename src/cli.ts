#!/usr/bin/env node
// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: a4c1c0c1b8f0f2e1
/**
 * AEGIS — CLI Entry Point
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 *   aegis                         run the demo (Rosenbrock)
 *   aegis --task task.json        optimize a task file (see --help)
 *   aegis --bench                 run the benchmark suite
 *   aegis "tune lr between 0.0001 and 0.1" --objective loss.js
 */

import * as fs from 'fs';
import * as path from 'path';
import { AegisAgent } from './agent';
import { Task, AgentConfig, AgentState, ParameterDef } from './interfaces';
import { runNatural, loadObjective } from './natural-cli';
import { runBenchmarks } from './benchmarks';

function version(): string {
  for (const rel of ['../package.json', '../../package.json']) {
    try { return JSON.parse(fs.readFileSync(path.join(__dirname, rel), 'utf-8')).version; } catch { /* next */ }
  }
  return 'dev';
}

const BANNER = `
╔═══════════════════════════════════════════════════════╗
║     _    _____ ____ ___ ____                          ║
║    / \\  | ____/ ___|_ _/ ___|                        ║
║   / _ \\ |  _|| |  _ | |\\___ \\                        ║
║  / ___ \\| |__| |_| || | ___) |                       ║
║ /_/   \\_\\_____\\____|___|____/                        ║
║                                                       ║
║  Autonomous Evolving General Intelligence System      ║
║  ${('v' + version() + ' — Danny Lee Eldridge © 2012-2026').padEnd(53)}║
╚═══════════════════════════════════════════════════════╝
`;

const HELP = `Usage:
  aegis [--demo]                    Run the built-in demo (Rosenbrock)
  aegis --task <task.json>          Optimize a task file
  aegis --bench                     Run the benchmark suite
  aegis "<plain English goal>"      e.g. "tune lr between 0.0001 and 0.1"
        [--objective <file.js>]     module exporting the function to optimize
        [--file <path>]             file to review/explain/test (coding commands)

Options:
  --evals <n>        Max evaluations
  --lang <code>      Output language (en/es/fr/de/ja/zh/pt/ko)
  --out <file.json>  Write the final result as JSON
  --verbose | --silent
  --version | --help

Task file (paths are relative to the task file):
  {
    "name": "Tune my model",
    "objective": "./loss.js",              // exports (params) => number
    "parameters": [
      { "name": "lr", "min": 0.0001, "max": 0.1 },
      { "name": "layers", "min": 1, "max": 12, "step": 1 }
    ],
    "goal": "minimize",                    // or "maximize"
    "maxEvals": 2000
  }

Press Ctrl+C once to stop early and keep the best result found so far.`;

/** Value following a flag, or undefined (never another flag). */
function argValue(args: string[], flag: string): string | undefined {
  const i = args.indexOf(flag);
  if (i === -1) return undefined;
  const v = args[i + 1];
  return v !== undefined && !v.startsWith('--') ? v : undefined;
}

function fail(message: string): never {
  console.error(`Error: ${message}`);
  process.exit(1);
}

interface TaskFile {
  name?: string;
  objective: string;
  parameters: ParameterDef[];
  goal?: string;
  maxEvals?: number;
}

export function loadTaskFile(taskFile: string): { task: Task; goal?: string; maxEvals?: number } {
  let spec: TaskFile;
  try {
    spec = JSON.parse(fs.readFileSync(taskFile, 'utf-8'));
  } catch (err: any) {
    throw new Error(`could not read ${taskFile}: ${err.message}`);
  }
  if (!spec || typeof spec.objective !== 'string') throw new Error('task file needs "objective": "<path to module>"');
  if (!Array.isArray(spec.parameters) || spec.parameters.length === 0) throw new Error('task file needs a non-empty "parameters" array');
  for (const p of spec.parameters) {
    if (typeof p.name !== 'string' || !Number.isFinite(p.min) || !Number.isFinite(p.max) || p.min >= p.max) {
      throw new Error(`invalid parameter ${JSON.stringify(p)}: needs name and numeric min < max`);
    }
  }
  const evaluate = loadObjective(path.resolve(path.dirname(taskFile), spec.objective));
  const name = spec.name || path.basename(taskFile, '.json');
  return {
    task: { id: name.toLowerCase().replace(/[^a-z0-9]+/g, '-'), name, evaluate, parameters: spec.parameters },
    goal: spec.goal,
    maxEvals: spec.maxEvals,
  };
}

/** Run an agent, stopping cleanly on the first Ctrl+C. */
async function runWithInterrupt(agent: AegisAgent): Promise<AgentState> {
  const onSigint = () => {
    console.log('\nCtrl+C: stopping and keeping the best result so far (press again to force quit)');
    process.removeListener('SIGINT', onSigint);
    agent.stop('Interrupted');
  };
  process.on('SIGINT', onSigint);
  try {
    return await agent.run();
  } finally {
    process.removeListener('SIGINT', onSigint);
  }
}

function printResult(state: AgentState, expected?: string): void {
  console.log('\n════════════════════════════════════════');
  console.log('FINAL RESULT:');
  if (!state.best || !Number.isFinite(state.best.score)) {
    console.log('  No valid evaluation (every score was NaN/Infinity or the run was stopped at once).');
  } else {
    console.log(`  Best score: ${state.best.score.toFixed(8)}`);
    console.log(`  Parameters: ${Object.entries(state.best.params).map(([k, v]) => `${k}=${+v.toFixed(6)}`).join(', ')}`);
  }
  if (expected) console.log(`  Expected:   ${expected}`);
  console.log(`  Evaluations: ${state.totalEvals}`);
  console.log(`  Runtime: ${state.runtime.toFixed(1)}s`);
  console.log(`  Discoveries: ${state.discoveries.length}`);
  console.log(`  Top strategy: ${state.strategies[0]?.type}`);
  console.log('════════════════════════════════════════');
}

function writeOut(outFile: string | undefined, state: AgentState, taskName: string): void {
  if (!outFile) return;
  const { history, ...rest } = state;
  fs.writeFileSync(outFile, JSON.stringify({ task: taskName, ...rest, evaluations: history.length }, null, 2));
  console.log(`Result written to ${outFile}`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const evalsArg = argValue(args, '--evals');
  const maxEvals = evalsArg !== undefined ? parseInt(evalsArg, 10) : undefined;
  if (evalsArg !== undefined && (!Number.isFinite(maxEvals) || maxEvals! <= 0)) fail('--evals needs a positive number');
  const verbosity: AgentConfig['verbosity'] = args.includes('--verbose') ? 'verbose' : args.includes('--silent') ? 'silent' : 'normal';
  const language = argValue(args, '--lang') || 'en';
  const outFile = argValue(args, '--out');

  if (args.includes('--version') || args.includes('-v')) {
    console.log(version());
    return;
  }
  if (args.includes('--help') || args.includes('-h')) {
    console.log(BANNER);
    console.log(HELP);
    return;
  }

  if (args.includes('--bench')) {
    await runBenchmarks({ maxEvals: maxEvals || 5000 });
    return;
  }

  if (args.includes('--task')) {
    const taskFile = argValue(args, '--task');
    if (!taskFile || !fs.existsSync(taskFile)) fail('--task requires the path of an existing JSON file');
    let loaded;
    try { loaded = loadTaskFile(taskFile); } catch (err: any) { fail(err.message); }
    const { task, goal } = loaded;
    if (verbosity !== 'silent') console.log(`Loaded "${task.name}" (${task.parameters.length} params) from ${taskFile}`);
    const agent = new AegisAgent(task, {
      maxEvals: maxEvals || loaded.maxEvals || 3000,
      verbosity, language,
      goal: goal ? { description: goal, minimize: !/max/i.test(goal) } : undefined,
    });
    const state = await runWithInterrupt(agent);
    printResult(state);
    writeOut(outFile, state, task.name);
    return;
  }

  // Plain-English goal: the first argument that is not a flag or a flag's value
  const valueFlags = new Set(['--evals', '--lang', '--out', '--objective', '--file', '--task']);
  const words = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && valueFlags.has(args[i - 1])));
  if (words.length > 0 && !args.includes('--demo')) {
    await runNatural(words.join(' '), {
      file: argValue(args, '--file'),
      objective: argValue(args, '--objective'),
      maxEvals,
      verbose: verbosity !== 'silent',
      language,
    });
    return;
  }

  // Default: demo
  if (verbosity !== 'silent') {
    console.log(BANNER);
    console.log('Running demo: find minimum of Rosenbrock function...\n');
  }
  const task: Task = {
    id: 'rosenbrock',
    name: 'Rosenbrock Function Minimization',
    evaluate: (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2), // min f(1,1) = 0
    parameters: [
      { name: 'x', min: -5, max: 5, description: 'First coordinate' },
      { name: 'y', min: -5, max: 5, description: 'Second coordinate' },
    ],
  };
  const agent = new AegisAgent(task, { maxEvals: maxEvals || 3000, reportInterval: 5, verbosity, language, explorationRate: 0.3 });
  const state = await runWithInterrupt(agent);
  printResult(state, 'x=1, y=1 (score=0)');
  writeOut(outFile, state, task.name);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err?.message || err);
    process.exit(1);
  });
}
