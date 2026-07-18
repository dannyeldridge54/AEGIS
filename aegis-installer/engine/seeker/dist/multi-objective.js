"use strict";
/**
 * Seeker — Multi-Objective Optimizer (Pareto Front)
 * NSGA-II inspired. UFE-tracked. Seeded RNG.
 * Returns the full Pareto frontier of non-dominated solutions.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.multiOptimize = multiOptimize;
const strategies_1 = require("./strategies");
const rng_1 = require("./rng");
const ufe_1 = require("./ufe");
function dominates(a, b, minimize) {
    let dominated = false;
    for (const key of Object.keys(a)) {
        const min = minimize[key] !== false;
        if (min ? a[key] > b[key] : a[key] < b[key])
            return false;
        if (min ? a[key] < b[key] : a[key] > b[key])
            dominated = true;
    }
    return dominated;
}
function computeCrowding(solutions, objectives) {
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
        if (range === 0)
            continue;
        for (let i = 1; i < n - 1; i++) {
            solutions[i].crowdingDistance += (solutions[i + 1].scores[obj] - solutions[i - 1].scores[obj]) / range;
        }
    }
}
/**
 * Multi-objective optimization using NSGA-II inspired approach.
 * Returns Pareto frontier with UFE metrics.
 */
async function multiOptimize(objectives, parameters, options) {
    const maxEvals = options?.maxEvals || 5000;
    const popSize = options?.populationSize || 50;
    const verbosity = options?.verbosity || 'normal';
    const startTime = Date.now();
    const rng = new rng_1.SeededRNG(options?.seed || undefined);
    const ufeTracker = new ufe_1.UFETracker(parameters, true);
    const minimizeMap = {};
    for (const obj of objectives)
        minimizeMap[obj.name] = obj.minimize !== false;
    const metaLearner = new strategies_1.MetaLearner(['random', 'evolutionary', 'curiosity', 'exploit', 'annealing'], 0.3, rng.fork());
    const allResults = [];
    let totalEvals = 0;
    let best = null;
    if (verbosity !== 'silent') {
        console.log(`[Seeker-Pareto] ${objectives.length} objectives, ${parameters.length} params, max ${maxEvals} evals (seed=${rng.seed})`);
    }
    while (totalEvals < maxEvals) {
        const strategy = metaLearner.selectStrategy();
        const batchSize = Math.min(popSize, maxEvals - totalEvals);
        const batch = [];
        for (let i = 0; i < batchSize; i++) {
            const history = allResults.map(r => ({
                params: r.params,
                score: Object.values(r.scores).reduce((a, b) => a + b, 0),
                timestamp: Date.now(),
                strategy: strategy.type,
            }));
            batch.push((0, strategies_1.generateNextPoint)(strategy, parameters, best, history, rng));
        }
        for (const params of batch) {
            const scores = {};
            for (const obj of objectives) {
                scores[obj.name] = await obj.evaluate(params);
            }
            allResults.push({ params, scores, dominated: false, crowdingDistance: 0 });
            totalEvals++;
            const scalar = objectives.reduce((sum, obj) => sum + scores[obj.name] * (obj.weight || 1) * (obj.minimize !== false ? 1 : -1), 0);
            const evalResult = { params, score: scalar, timestamp: Date.now(), strategy: strategy.type };
            ufeTracker.record(evalResult);
            if (!best || scalar < best.score) {
                best = evalResult;
                metaLearner.updateStrategy(strategy.type, 1);
            }
        }
        if (verbosity === 'normal' && totalEvals % (popSize * 5) === 0) {
            const front = allResults.filter(r => !r.dominated);
            console.log(`  [${totalEvals}/${maxEvals}] Pareto front size: ${front.length}`);
        }
    }
    // Compute final Pareto front
    for (let i = 0; i < allResults.length; i++) {
        for (let j = 0; j < allResults.length; j++) {
            if (i === j)
                continue;
            if (dominates(allResults[j].scores, allResults[i].scores, minimizeMap)) {
                allResults[i].dominated = true;
                break;
            }
        }
    }
    const front = allResults.filter(r => !r.dominated);
    const objNames = objectives.map(o => o.name);
    computeCrowding(front, objNames);
    front.sort((a, b) => b.crowdingDistance - a.crowdingDistance);
    if (verbosity !== 'silent') {
        console.log(`[Seeker-Pareto] Done! ${front.length} Pareto-optimal solutions from ${totalEvals} evals`);
    }
    return {
        solutions: front,
        totalEvals,
        runtime: (Date.now() - startTime) / 1000,
        ufe: ufeTracker.getMetrics(),
    };
}
//# sourceMappingURL=multi-objective.js.map