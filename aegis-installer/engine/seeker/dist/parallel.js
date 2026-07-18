"use strict";
/**
 * Seeker — Parallel Batch Evaluator
 * Runs evaluations in parallel batches with UFE tracking,
 * seeded RNG, concurrency limits, timeout, and retry logic.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parallelOptimize = parallelOptimize;
const strategies_1 = require("./strategies");
const rng_1 = require("./rng");
const ufe_1 = require("./ufe");
const language_1 = require("./language");
async function withTimeout(promise, ms) {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(new Error('Evaluation timeout')), ms);
        promise.then((val) => { clearTimeout(timer); resolve(val); }, (err) => { clearTimeout(timer); reject(err); });
    });
}
/**
 * Parallel batch optimizer with full UFE tracking.
 * Ideal for network calls, simulations, or any async evaluation.
 */
async function parallelOptimize(task, config, optimum) {
    const concurrency = config?.concurrency || 4;
    const evalTimeout = config?.evalTimeout || 30000;
    const retries = config?.retries || 1;
    const batchSize = config?.batchSize || concurrency * 2;
    const maxEvals = config?.maxEvals || 5000;
    const verbosity = config?.verbosity || 'normal';
    const lang = config?.language || 'en';
    const msg = (0, language_1.getMessages)(lang);
    const rng = new rng_1.SeededRNG(config?.seed || undefined);
    const metaLearner = new strategies_1.MetaLearner(config?.strategies || ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'], config?.explorationRate || 0.3, rng.fork());
    const minimize = !config?.goal || (typeof config.goal === 'string'
        ? !/(maximize|maximise|highest|largest)/i.test(config.goal)
        : config.goal.minimize !== false);
    const ufeTracker = new ufe_1.UFETracker(task.parameters, minimize, config?.noveltyResolution || 20);
    const anomalyDetector = new ufe_1.AnomalyDetector(50);
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
    let failedBatches = 0;
    if (verbosity !== 'silent') {
        console.log(`${msg.started} [parallel: ${concurrency}x, seed=${rng.seed}]`);
        console.log(`  Task: ${task.name} (${task.parameters.length} params, batch=${batchSize})`);
    }
    while (state.totalEvals < maxEvals) {
        const currentBatch = Math.min(batchSize, maxEvals - state.totalEvals);
        // Generate batch of candidates
        const candidates = [];
        for (let i = 0; i < currentBatch; i++) {
            const strategy = metaLearner.selectStrategy();
            const params = (0, strategies_1.generateNextPoint)(strategy, task.parameters, state.best, state.history, rng, task.constraints, state.totalEvals);
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
                            return null;
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
                if (r)
                    results.push(r);
                else
                    batchFailures++;
            }
        }
        state.totalEvals += results.length;
        // Abort on consecutive full-batch failures
        if (results.length === 0 && batchFailures > 0) {
            failedBatches++;
            if (failedBatches >= 3) {
                if (verbosity !== 'silent')
                    console.log('⚠️ 3 consecutive batches failed. Stopping.');
                break;
            }
        }
        else {
            failedBatches = 0;
        }
        // Process results
        for (const result of results) {
            state.history.push(result);
            ufeTracker.record(result);
            // Anomaly detection
            const anomaly = anomalyDetector.check(result.score);
            if (anomaly) {
                anomaly.result = result;
                state.discoveries.push(anomaly);
            }
            const previousBest = state.best?.score ?? (minimize ? Infinity : -Infinity);
            const isBetter = minimize ? result.score < previousBest : result.score > previousBest;
            if (!state.best || isBetter) {
                const improvement = Math.abs(previousBest - result.score);
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
        // Trim working history (convergence data preserved in UFETracker)
        if (state.history.length > 5000)
            state.history = state.history.slice(-2500);
        // Progress report
        if (verbosity === 'normal' && state.totalEvals % (batchSize * 5) < batchSize) {
            const elapsed = (0, language_1.formatDuration)((Date.now() - startTime) / 1000);
            const evalsPerSec = state.totalEvals / ((Date.now() - startTime) / 1000);
            const ufe = ufeTracker.getMetrics();
            console.log(`${msg.progress} ${state.totalEvals}/${maxEvals} | ${msg.bestScore}: ${state.best?.score.toFixed(6)} | UFE: ${(ufe.ufeRatio * 100).toFixed(1)}% | ${evalsPerSec.toFixed(0)}/s | ${elapsed}`);
        }
        // Periodic anomaly checks
        if (state.totalEvals % 100 < batchSize) {
            const plateau = anomalyDetector.checkPlateau();
            if (plateau)
                state.discoveries.push(plateau);
            const shift = anomalyDetector.checkShift();
            if (shift)
                state.discoveries.push(shift);
        }
    }
    state.runtime = (Date.now() - startTime) / 1000;
    state.strategies = metaLearner.getStrategies();
    state.ufe = ufeTracker.getMetrics(optimum);
    if (verbosity !== 'silent') {
        const evalsPerSec = state.totalEvals / state.runtime;
        console.log(`\n✅ Done! ${state.totalEvals} evals in ${(0, language_1.formatDuration)(state.runtime)} (${evalsPerSec.toFixed(0)}/s)`);
        console.log(`   Best: ${state.best?.score.toFixed(8)} | UFE: ${(state.ufe.ufeRatio * 100).toFixed(1)}% | Discoveries: ${state.discoveries.length}`);
    }
    return state;
}
//# sourceMappingURL=parallel.js.map