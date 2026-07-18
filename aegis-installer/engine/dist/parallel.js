"use strict";
/**
 * AEGIS — Parallel Batch Evaluator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Runs evaluations in parallel batches for massive speedup on async tasks.
 * Supports concurrency limits, timeout, and retry logic.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parallelOptimize = parallelOptimize;
const strategies_1 = require("./strategies");
const language_1 = require("./language");
async function withTimeout(promise, ms) {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(new Error('Evaluation timeout')), ms);
        promise.then((val) => { clearTimeout(timer); resolve(val); }, (err) => { clearTimeout(timer); reject(err); });
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
async function parallelOptimize(task, config) {
    const concurrency = config?.concurrency || 4;
    const evalTimeout = config?.evalTimeout || 30000;
    const retries = config?.retries || 1;
    const batchSize = config?.batchSize || concurrency * 2;
    const maxEvals = config?.maxEvals || 5000;
    const verbosity = config?.verbosity || 'normal';
    const lang = config?.language || 'en';
    const msg = (0, language_1.getMessages)(lang);
    const metaLearner = new strategies_1.MetaLearner(config?.strategies || ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'], config?.explorationRate || 0.3);
    const state = {
        best: null,
        totalEvals: 0,
        history: [],
        strategies: metaLearner.getStrategies(),
        discoveries: [],
        runtime: 0,
        phase: 'exploring',
        ufe: {
            totalEvals: 0, usefulEvals: 0, ufeRatio: 0,
            convergenceVelocity: 0, aucc: 0,
            timeToTarget: { pct10: null, pct50: null, pct90: null },
            convergenceCurve: [],
        },
    };
    const startTime = Date.now();
    if (verbosity !== 'silent') {
        console.log(`${msg.started} [parallel: ${concurrency}x]`);
        console.log(`  Task: ${task.name} (${task.parameters.length} params, batch=${batchSize})`);
    }
    while (state.totalEvals < maxEvals) {
        const currentBatch = Math.min(batchSize, maxEvals - state.totalEvals);
        // Generate batch of candidates
        const candidates = [];
        for (let i = 0; i < currentBatch; i++) {
            const strategy = metaLearner.selectStrategy();
            const params = (0, strategies_1.generateNextPoint)(strategy, task.parameters, state.best, state.history, task.constraints);
            candidates.push({ params, strategy: strategy.type });
        }
        // Evaluate in parallel with concurrency limit
        const results = [];
        let batchFailures = 0;
        for (let i = 0; i < candidates.length; i += concurrency) {
            const chunk = candidates.slice(i, i + concurrency);
            const promises = chunk.map(async ({ params, strategy }) => {
                for (let attempt = 0; attempt <= retries; attempt++) {
                    try {
                        const score = await withTimeout(Promise.resolve(task.evaluate(params)), evalTimeout);
                        if (!isFinite(score))
                            return null; // Reject non-finite results
                        return { params, score, timestamp: Date.now(), strategy };
                    }
                    catch {
                        if (attempt === retries)
                            return null;
                    }
                }
                return null;
            });
            const chunkResults = await Promise.all(promises);
            for (const r of chunkResults) {
                if (r) {
                    results.push(r);
                }
                else {
                    batchFailures++;
                }
            }
        }
        // Count all attempted evaluations (successful + failed) toward the limit
        state.totalEvals += results.length;
        // Abort if entire batch failed (prevents infinite loop)
        if (results.length === 0 && batchFailures > 0) {
            const consecutiveFailThreshold = 3;
            state.__failedBatches = (state.__failedBatches || 0) + 1;
            if (state.__failedBatches >= consecutiveFailThreshold) {
                if (verbosity !== 'silent') {
                    console.log(`⚠️ ${consecutiveFailThreshold} consecutive batches failed. Stopping.`);
                }
                break;
            }
        }
        else {
            state.__failedBatches = 0;
        }
        // Process results
        for (const result of results) {
            state.history.push(result);
            const previousBest = state.best?.score ?? Infinity;
            if (!state.best || result.score < previousBest) {
                const improvement = previousBest - result.score;
                state.best = result;
                metaLearner.updateStrategy(result.strategy, Math.min(Math.max(improvement, 0.001), 100));
                if (verbosity !== 'silent') {
                    console.log(`${msg.newBest} score=${result.score.toFixed(6)} [${result.strategy}] (${state.totalEvals} evals)`);
                }
            }
            else {
                metaLearner.updateStrategy(result.strategy, 0);
            }
        }
        // Trim history
        if (state.history.length > 5000) {
            state.history = state.history.slice(-2500);
        }
        // Progress report
        if (verbosity === 'normal' && state.totalEvals % (batchSize * 5) < batchSize) {
            const elapsed = (0, language_1.formatDuration)((Date.now() - startTime) / 1000);
            const evalsPerSec = state.totalEvals / ((Date.now() - startTime) / 1000);
            console.log(`${msg.progress} ${state.totalEvals}/${maxEvals} | ${msg.bestScore}: ${state.best?.score.toFixed(6)} | ${evalsPerSec.toFixed(0)} evals/s | ${elapsed}`);
        }
    }
    state.runtime = (Date.now() - startTime) / 1000;
    state.strategies = metaLearner.getStrategies();
    if (verbosity !== 'silent') {
        const evalsPerSec = state.totalEvals / state.runtime;
        console.log(`\n✅ Done! ${state.totalEvals} evals in ${(0, language_1.formatDuration)(state.runtime)} (${evalsPerSec.toFixed(0)}/s)`);
        console.log(`   Best: ${state.best?.score.toFixed(8)}`);
    }
    return state;
}
//# sourceMappingURL=parallel.js.map