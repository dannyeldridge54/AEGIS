/**
 * AEGIS — Parallel Batch Evaluator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Runs evaluations in parallel batches for massive speedup on async tasks.
 * Supports concurrency limits, timeout, and retry logic.
 */

import { Task, ParameterDef, EvalResult, AgentConfig, AgentState } from './interfaces';
import { MetaLearner, generateNextPoint } from './strategies';
import { getMessages, formatDuration } from './language';

export interface ParallelConfig extends AgentConfig {
  /** Number of concurrent evaluations (default: 4) */
  concurrency?: number;
  /** Timeout per evaluation in ms (default: 30000) */
  evalTimeout?: number;
  /** Retry failed evaluations (default: 1) */
  retries?: number;
  /** Batch size (default: concurrency * 2) */
  batchSize?: number;
}

async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Evaluation timeout')), ms);
    promise.then(
      (val) => { clearTimeout(timer); resolve(val); },
      (err) => { clearTimeout(timer); reject(err); }
    );
  });
}

/**
 * Parallel batch optimizer — evaluates multiple parameter sets concurrently.
 * Ideal for network calls, simulations, or any async evaluation function.
 *
 * @example
 * const result = await parallelOptimize({
 *   id: 'api-tune',
 *   name: 'API Config Tuning',
 *   evaluate: async (p) => await benchmarkEndpoint(p),
 *   parameters: [...],
 * }, { concurrency: 8, maxEvals: 5000 });
 */
export async function parallelOptimize(
  task: Task,
  config?: ParallelConfig
): Promise<AgentState> {
  const concurrency = config?.concurrency || 4;
  const evalTimeout = config?.evalTimeout || 30000;
  const retries = config?.retries || 1;
  const batchSize = config?.batchSize || concurrency * 2;
  const maxEvals = config?.maxEvals || 5000;
  const verbosity = config?.verbosity || 'normal';
  const lang = config?.language || 'en';
  const msg = getMessages(lang);

  const metaLearner = new MetaLearner(
    config?.strategies || ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'],
    config?.explorationRate || 0.3
  );

  const state: AgentState = {
    best: null,
    totalEvals: 0,
    history: [],
    strategies: metaLearner.getStrategies(),
    discoveries: [],
    runtime: 0,
    phase: 'exploring',
  };

  const startTime = Date.now();

  if (verbosity !== 'silent') {
    console.log(`${msg.started} [parallel: ${concurrency}x]`);
    console.log(`  Task: ${task.name} (${task.parameters.length} params, batch=${batchSize})`);
  }

  while (state.totalEvals < maxEvals) {
    const currentBatch = Math.min(batchSize, maxEvals - state.totalEvals);

    // Generate batch of candidates
    const candidates: Array<{ params: Record<string, number>; strategy: string }> = [];
    for (let i = 0; i < currentBatch; i++) {
      const strategy = metaLearner.selectStrategy();
      const params = generateNextPoint(
        strategy,
        task.parameters,
        state.best,
        state.history,
        task.constraints
      );
      candidates.push({ params, strategy: strategy.type });
    }

    // Evaluate in parallel with concurrency limit
    const results: EvalResult[] = [];
    for (let i = 0; i < candidates.length; i += concurrency) {
      const chunk = candidates.slice(i, i + concurrency);
      const promises = chunk.map(async ({ params, strategy }) => {
        for (let attempt = 0; attempt <= retries; attempt++) {
          try {
            const score = await withTimeout(
              Promise.resolve(task.evaluate(params)),
              evalTimeout
            );
            return { params, score, timestamp: Date.now(), strategy } as EvalResult;
          } catch {
            if (attempt === retries) return null;
          }
        }
        return null;
      });

      const chunkResults = await Promise.all(promises);
      for (const r of chunkResults) {
        if (r) results.push(r);
      }
    }

    // Process results
    for (const result of results) {
      state.totalEvals++;
      state.history.push(result);

      const previousBest = state.best?.score ?? Infinity;
      if (!state.best || result.score < previousBest) {
        const improvement = previousBest - result.score;
        state.best = result;
        metaLearner.updateStrategy(result.strategy as any, Math.max(improvement, 0.001));

        if (verbosity !== 'silent') {
          console.log(`${msg.newBest} score=${result.score.toFixed(6)} [${result.strategy}] (${state.totalEvals} evals)`);
        }
      } else {
        metaLearner.updateStrategy(result.strategy as any, 0);
      }
    }

    // Trim history
    if (state.history.length > 5000) {
      state.history = state.history.slice(-2500);
    }

    // Progress report
    if (verbosity === 'normal' && state.totalEvals % (batchSize * 5) < batchSize) {
      const elapsed = formatDuration((Date.now() - startTime) / 1000);
      const evalsPerSec = state.totalEvals / ((Date.now() - startTime) / 1000);
      console.log(`${msg.progress} ${state.totalEvals}/${maxEvals} | ${msg.bestScore}: ${state.best?.score.toFixed(6)} | ${evalsPerSec.toFixed(0)} evals/s | ${elapsed}`);
    }
  }

  state.runtime = (Date.now() - startTime) / 1000;
  state.strategies = metaLearner.getStrategies();

  if (verbosity !== 'silent') {
    const evalsPerSec = state.totalEvals / state.runtime;
    console.log(`\n✅ Done! ${state.totalEvals} evals in ${formatDuration(state.runtime)} (${evalsPerSec.toFixed(0)}/s)`);
    console.log(`   Best: ${state.best?.score.toFixed(8)}`);
  }

  return state;
}
