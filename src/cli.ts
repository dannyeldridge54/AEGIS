/**
 * AEGIS — CLI Entry Point
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 */

import { AegisAgent } from './agent';
import { Task, AgentConfig } from './interfaces';
import * as fs from 'fs';

const BANNER = `
╔═══════════════════════════════════════════════════════╗
║     _    _____ ____ ___ ____                          ║
║    / \\  | ____/ ___|_ _/ ___|                        ║
║   / _ \\ |  _|| |  _ | |\\___ \\                        ║
║  / ___ \\| |__| |_| || | ___) |                       ║
║ /_/   \\_\\_____\\____|___|____/                        ║
║                                                       ║
║  Autonomous Evolving General Intelligence System      ║
║  v1.0.0 — Danny Lee Eldridge © 2012-2026             ║
╚═══════════════════════════════════════════════════════╝
`;

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(BANNER);
    console.log('Usage:');
    console.log('  aegis --task <task.json>     Run agent on task definition');
    console.log('  aegis --demo                 Run built-in demo');
    console.log('  aegis --lang <code>          Set language (en/es/fr/de/ja/zh/pt/ko)');
    console.log('  aegis --evals <n>            Max evaluations');
    console.log('  aegis --verbose              Verbose output');
    console.log('  aegis --silent               No output');
    return;
  }

  if (args.includes('--demo') || args.length === 0) {
    console.log(BANNER);
    console.log('Running demo: find minimum of Rosenbrock function...\n');

    const lang = args[args.indexOf('--lang') + 1] || 'en';
    const maxEvals = parseInt(args[args.indexOf('--evals') + 1]) || 3000;

    const task: Task = {
      id: 'rosenbrock',
      name: 'Rosenbrock Function Minimization',
      evaluate: (p) => {
        // Global minimum at (1, 1) with f(1,1) = 0
        return Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2);
      },
      parameters: [
        { name: 'x', min: -5, max: 5, description: 'First coordinate' },
        { name: 'y', min: -5, max: 5, description: 'Second coordinate' },
      ],
    };

    const config: AgentConfig = {
      maxEvals,
      reportInterval: 5,
      verbosity: args.includes('--verbose') ? 'verbose' : args.includes('--silent') ? 'silent' : 'normal',
      language: lang,
      explorationRate: 0.3,
    };

    const agent = new AegisAgent(task, config);
    const state = await agent.run();

    console.log('\n════════════════════════════════════════');
    console.log('FINAL RESULT:');
    console.log(`  Best score: ${state.best!.score.toFixed(8)}`);
    console.log(`  Parameters: x=${state.best!.params.x.toFixed(6)}, y=${state.best!.params.y.toFixed(6)}`);
    console.log(`  Expected:   x=1.000000, y=1.000000 (score=0)`);
    console.log(`  Evaluations: ${state.totalEvals}`);
    console.log(`  Runtime: ${state.runtime.toFixed(1)}s`);
    console.log(`  Discoveries: ${state.discoveries.length}`);
    console.log(`  Top strategy: ${state.strategies[0]?.type}`);
    console.log('════════════════════════════════════════');
    return;
  }

  // Task from JSON file
  const taskIdx = args.indexOf('--task');
  if (taskIdx !== -1) {
    const taskFile = args[taskIdx + 1];
    if (!taskFile || !fs.existsSync(taskFile)) {
      console.error('Error: --task requires a valid JSON file path');
      process.exit(1);
    }
    console.log(`Loading task from ${taskFile}...`);
    // Task file loading would go here for production
    console.log('Task file loading not yet implemented in CLI. Use the API directly.');
  }
}

main().catch(console.error);
