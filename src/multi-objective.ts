/**
 * AEGIS — Multi-Objective Optimizer (Pareto Front)
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Supports multiple competing objectives simultaneously.
 * Returns the full Pareto frontier — the set of non-dominated solutions.
 */

import { ParameterDef, EvalResult } from './interfaces';
import { MetaLearner, generateNextPoint } from './strategies';

export interface MultiObjective {
  name: string;
  evaluate: (params: Record<string, number>) => number | Promise<number>;
  minimize?: boolean; // default true
  weight?: number;    // relative importance (for scalarization fallback)
}

export interface ParetoResult {
  params: Record<string, number>;
  scores: Record<string, number>;
  dominated: boolean;
  crowdingDistance: number;
}

export interface ParetoFront {
  solutions: ParetoResult[];
  totalEvals: number;
  runtime: number;
}

function dominates(a: Record<string, number>, b: Record<string, number>, minimize: Record<string, boolean>): boolean {
  let dominated = false;
  for (const key of Object.keys(a)) {
    const min = minimize[key] !== false;
    if (min ? a[key] > b[key] : a[key] < b[key]) return false;
    if (min ? a[key] < b[key] : a[key] > b[key]) dominated = true;
  }
  return dominated;
}

function computeCrowding(solutions: ParetoResult[], objectives: string[]): void {
  const n = solutions.length;
  if (n <= 2) {
    solutions.forEach(s => s.crowdingDistance = Infinity);
    return;
  }

  solutions.forEach(s => s.crowdingDistance = 0);

  for (const obj of objectives) {
    solutions.sort((a, b) => a.scores[obj] - b.scores[obj]);
    solutions[0].crowdingDistance = Infinity;
    solutions[n - 1].crowdingDistance = Infinity;

    const range = solutions[n - 1].scores[obj] - solutions[0].scores[obj];
    if (range === 0) continue;

    for (let i = 1; i < n - 1; i++) {
      solutions[i].crowdingDistance +=
        (solutions[i + 1].scores[obj] - solutions[i - 1].scores[obj]) / range;
    }
  }
}

/**
 * Multi-objective optimization using NSGA-II inspired approach.
 * Returns the Pareto frontier of non-dominated solutions.
 */
export async function multiOptimize(
  objectives: MultiObjective[],
  parameters: ParameterDef[],
  options?: {
    maxEvals?: number;
    populationSize?: number;
    verbosity?: 'silent' | 'minimal' | 'normal';
  }
): Promise<ParetoFront> {
  const maxEvals = options?.maxEvals || 5000;
  const popSize = options?.populationSize || 50;
  const verbosity = options?.verbosity || 'normal';
  const startTime = Date.now();

  const minimizeMap: Record<string, boolean> = {};
  for (const obj of objectives) minimizeMap[obj.name] = obj.minimize !== false;

  const metaLearner = new MetaLearner(
    ['random', 'evolutionary', 'curiosity', 'exploit', 'annealing'],
    0.3
  );

  const allResults: ParetoResult[] = [];
  let totalEvals = 0;
  let best: EvalResult | null = null;

  if (verbosity !== 'silent') {
    console.log(`[AEGIS-Pareto] ${objectives.length} objectives, ${parameters.length} params, max ${maxEvals} evals`);
  }

  while (totalEvals < maxEvals) {
    const strategy = metaLearner.selectStrategy();
    const batchSize = Math.min(popSize, maxEvals - totalEvals);
    const batch: Record<string, number>[] = [];

    for (let i = 0; i < batchSize; i++) {
      const history = allResults.map(r => ({
        params: r.params,
        score: Object.values(r.scores).reduce((a, b) => a + b, 0),
        timestamp: Date.now(),
        strategy: strategy.type,
      }));
      batch.push(generateNextPoint(strategy, parameters, best, history as EvalResult[]));
    }

    // Evaluate batch
    for (const params of batch) {
      const scores: Record<string, number> = {};
      for (const obj of objectives) {
        scores[obj.name] = await obj.evaluate(params);
      }
      allResults.push({ params, scores, dominated: false, crowdingDistance: 0 });
      totalEvals++;

      // Track scalar best for strategy learning
      const scalar = objectives.reduce((sum, obj, i) =>
        sum + scores[obj.name] * (obj.weight || 1) * (obj.minimize !== false ? 1 : -1), 0);
      if (!best || scalar < best.score) {
        best = { params, score: scalar, timestamp: Date.now(), strategy: strategy.type };
        metaLearner.updateStrategy(strategy.type, 1);
      }
    }

    if (verbosity === 'normal' && totalEvals % (popSize * 5) === 0) {
      const front = allResults.filter(r => !r.dominated);
      console.log(`  [${totalEvals}/${maxEvals}] Pareto front size: ${front.length}`);
    }
  }

  // Compute final Pareto front
  const objNames = objectives.map(o => o.name);
  for (let i = 0; i < allResults.length; i++) {
    for (let j = 0; j < allResults.length; j++) {
      if (i === j) continue;
      if (dominates(allResults[j].scores, allResults[i].scores, minimizeMap)) {
        allResults[i].dominated = true;
        break;
      }
    }
  }

  const front = allResults.filter(r => !r.dominated);
  computeCrowding(front, objNames);
  front.sort((a, b) => b.crowdingDistance - a.crowdingDistance);

  if (verbosity !== 'silent') {
    console.log(`[AEGIS-Pareto] Done! ${front.length} Pareto-optimal solutions from ${totalEvals} evals`);
  }

  return {
    solutions: front,
    totalEvals,
    runtime: (Date.now() - startTime) / 1000,
  };
}
