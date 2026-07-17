/**
 * AEGIS — Quickstart Example
 *
 * Shows how simple it is to use AEGIS for any optimization task.
 */

import { aegis, optimize } from '../src';

async function main() {
  console.log('═══ Example 1: One-liner optimization ═══\n');

  const best = await optimize(
    (p) => (p.x - 3) ** 2 + (p.y + 1) ** 2 + (p.z - 7) ** 2,
    [
      { name: 'x', min: -10, max: 10 },
      { name: 'y', min: -10, max: 10 },
      { name: 'z', min: 0, max: 15 },
    ],
    { maxEvals: 2000, verbosity: 'minimal' }
  );

  console.log(`\nBest: x=${best.params.x.toFixed(3)}, y=${best.params.y.toFixed(3)}, z=${best.params.z.toFixed(3)}`);
  console.log(`Score: ${best.score.toFixed(6)} (target: 0)\n`);

  console.log('═══ Example 2: Full agent with events ═══\n');

  const agent = aegis({
    id: 'ml-tuning',
    name: 'Neural Network Hyperparameter Tuning',
    evaluate: (p) => {
      // Simulate training loss as function of hyperparams
      const lrPenalty = Math.abs(Math.log10(p.lr) + 3) * 0.5;
      const dropoutSweet = Math.abs(p.dropout - 0.3) * 2;
      const layerPenalty = Math.abs(p.layers - 4) * 0.3;
      return lrPenalty + dropoutSweet + layerPenalty + Math.random() * 0.1;
    },
    parameters: [
      { name: 'lr', min: 0.0001, max: 0.1, description: 'Learning rate' },
      { name: 'dropout', min: 0, max: 0.8, description: 'Dropout rate' },
      { name: 'layers', min: 1, max: 8, description: 'Hidden layers' },
    ],
  }, {
    maxEvals: 1500,
    reportInterval: 3,
    language: 'en',
  });

  agent.on((event) => {
    if (event.type === 'discovery') {
      console.log(`  💡 ${event.discovery.description}`);
    }
  });

  const state = await agent.run();
  console.log(`\nFinal: lr=${state.best!.params.lr.toFixed(5)}, dropout=${state.best!.params.dropout.toFixed(3)}, layers=${state.best!.params.layers.toFixed(1)}`);
  console.log(`Score: ${state.best!.score.toFixed(4)} | Discoveries: ${state.discoveries.length}`);
}

main().catch(console.error);
