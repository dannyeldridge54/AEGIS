#!/usr/bin/env node
/**
 * Seeker — CLI Entry Point
 * Commands: benchmark, compare, optimize
 */

import { runBenchmarks } from './benchmarks';
import { compareModels } from './comparison';
import { optimize } from './agent';

const args = process.argv.slice(2);
const command = args[0] || 'benchmark';

async function main() {
  switch (command) {
    case 'benchmark': {
      const evals = parseInt(args[1]) || 5000;
      const seed = args.includes('--seed') ? parseInt(args[args.indexOf('--seed') + 1]) : undefined;
      console.log(`\nRunning benchmarks (budget=${evals}${seed ? `, seed=${seed}` : ''})...\n`);
      await runBenchmarks({ maxEvals: evals, seed });
      break;
    }

    case 'compare': {
      const evals = parseInt(args[1]) || 2000;
      const trials = parseInt(args[2]) || 5;
      console.log(`\nRunning model comparison (budget=${evals}, trials=${trials})...\n`);
      await compareModels({
        models: [
          { id: 'high-explore', name: 'High Explore', agentConfig: { explorationRate: 0.7 } },
          { id: 'balanced', name: 'Balanced', agentConfig: { explorationRate: 0.3 } },
          { id: 'greedy', name: 'Greedy', agentConfig: { explorationRate: 0.1 } },
          { id: 'evo-only', name: 'Evolutionary Only', agentConfig: { strategies: ['evolutionary', 'exploit'] } },
          { id: 'gradient-focus', name: 'Gradient Focus', agentConfig: { strategies: ['gradient', 'exploit', 'random'] } },
        ],
        benchmarks: 'all',
        budget: evals,
        trials,
        rankBy: 'final_score',
        baseSeed: 42,
      });
      break;
    }

    case 'optimize': {
      const expr = args[1] || 'x^2+y^2';
      const evals = parseInt(args[2]) || 3000;
      console.log(`\nOptimizing: ${expr} (budget=${evals})...\n`);

      // Simple expression parser for demo
      const fn = new Function('p', `with(p) { return ${expr.replace(/\^/g, '**')}; }`) as
        (p: Record<string, number>) => number;

      // Extract variable names
      const vars = expr.match(/[a-z]/g) || ['x'];
      const unique = [...new Set(vars)];
      const params = unique.map(v => ({ name: v, min: -10, max: 10 }));

      const result = await optimize(fn, params, { maxEvals: evals, verbosity: 'normal', seed: 42 });
      console.log(`\n✅ Best: score=${result.score.toFixed(8)}`);
      console.log(`   Params: ${JSON.stringify(result.params)}`);
      break;
    }

    case 'help':
    default:
      console.log(`
Seeker — Autonomous Discovery Engine

Usage:
  seeker benchmark [evals] [--seed N]     Run standard benchmarks
  seeker compare [evals] [trials]         Head-to-head model comparison
  seeker optimize "expr" [evals]          Optimize a math expression
  seeker help                             Show this help

Examples:
  seeker benchmark 5000 --seed 42
  seeker compare 2000 10
  seeker optimize "x^2 + y^2" 3000
`);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
