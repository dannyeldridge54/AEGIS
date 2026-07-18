"use strict";
/**
 * AEGIS — Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Implements all optimization strategies + meta-learner that picks
 * the best strategy adaptively based on past performance.
 * Now with seeded RNG, real gradient estimation, quadratic surrogate,
 * and eval-count-based annealing.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.MetaLearner = void 0;
exports.gridSample = gridSample;
exports.mutateParams = mutateParams;
exports.crossover = crossover;
exports.gradientStep = gradientStep;
exports.surrogateStep = surrogateStep;
exports.annealingSample = annealingSample;
exports.swarmUpdate = swarmUpdate;
exports.noveltySample = noveltySample;
exports.generateNextPoint = generateNextPoint;
const rng_1 = require("./rng");
// ─── Parameter Sampling Helpers ──────────────────────────────────────────────
function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
}
function randomParams(params, rng) {
    const result = {};
    for (const p of params) {
        result[p.name] = rng.range(p.min, p.max);
    }
    return result;
}
function satisfiesConstraints(values, constraints) {
    if (!constraints || constraints.length === 0)
        return true;
    return constraints.every(c => c.check(values));
}
// ─── Strategy Implementations ────────────────────────────────────────────────
function gridSample(params, resolution, index) {
    const result = {};
    let remaining = index;
    for (const p of params) {
        const step = (p.max - p.min) / (resolution - 1);
        const gridIdx = remaining % resolution;
        remaining = Math.floor(remaining / resolution);
        result[p.name] = p.min + gridIdx * step;
    }
    return result;
}
function mutateParams(base, params, magnitude = 0.1, rng) {
    const result = {};
    for (const p of params) {
        const range = p.max - p.min;
        const r = rng ? rng.random() : Math.random();
        const noise = (r - 0.5) * 2 * magnitude * range;
        result[p.name] = clamp(base[p.name] + noise, p.min, p.max);
    }
    return result;
}
function crossover(a, b, params, rng) {
    const result = {};
    for (const p of params) {
        result[p.name] = (rng ? rng.random() : Math.random()) < 0.5 ? a[p.name] : b[p.name];
    }
    return result;
}
/** Real finite-difference gradient estimation from recent history */
function gradientStep(best, params, history, rng) {
    if (history.length < params.length * 2) {
        return mutateParams(best.params, params, 0.05, rng);
    }
    const recent = history.slice(-Math.min(history.length, 50));
    const result = { ...best.params };
    const lr = 0.1;
    for (const p of params) {
        // Estimate gradient from nearby points
        let sumGrad = 0;
        let count = 0;
        for (let i = 1; i < recent.length; i++) {
            const dx = recent[i].params[p.name] - recent[i - 1].params[p.name];
            const dy = recent[i].score - recent[i - 1].score;
            if (Math.abs(dx) > 1e-12) {
                sumGrad += dy / dx;
                count++;
            }
        }
        if (count > 0) {
            const grad = sumGrad / count;
            const range = p.max - p.min;
            result[p.name] = clamp(best.params[p.name] - lr * grad * range * 0.1, p.min, p.max);
        }
        else {
            result[p.name] = clamp(best.params[p.name] + rng.normal(0, (p.max - p.min) * 0.02), p.min, p.max);
        }
    }
    return result;
}
/** Quadratic surrogate model for bayesian strategy */
function surrogateStep(best, params, history, rng) {
    if (history.length < 10) {
        return randomParams(params, rng);
    }
    const recent = history.slice(-Math.min(history.length, 100));
    const result = {};
    for (const p of params) {
        // Fit quadratic: score ≈ a*x² + b*x + c per dimension
        let sumX = 0, sumX2 = 0, sumX3 = 0, sumX4 = 0;
        let sumY = 0, sumXY = 0, sumX2Y = 0;
        const n = recent.length;
        for (const r of recent) {
            const x = r.params[p.name];
            const y = r.score;
            sumX += x;
            sumX2 += x * x;
            sumX3 += x * x * x;
            sumX4 += x * x * x * x;
            sumY += y;
            sumXY += x * y;
            sumX2Y += x * x * y;
        }
        // Solve least-squares for quadratic coefficients
        const det = n * (sumX2 * sumX4 - sumX3 * sumX3)
            - sumX * (sumX * sumX4 - sumX3 * sumX2)
            + sumX2 * (sumX * sumX3 - sumX2 * sumX2);
        if (Math.abs(det) > 1e-20) {
            const a = (sumY * (sumX2 * sumX4 - sumX3 * sumX3)
                - sumXY * (sumX * sumX4 - sumX3 * sumX2)
                + sumX2Y * (sumX * sumX3 - sumX2 * sumX2)) / det;
            const b = (n * (sumXY * sumX4 - sumX2Y * sumX3)
                - sumY * (sumX * sumX4 - sumX3 * sumX2)
                + sumX2 * (sumX * sumX2Y - sumXY * sumX2)) / det;
            // Predicted minimum at x = -b/(2a) if a > 0
            if (a > 1e-12) {
                const xMin = clamp(-b / (2 * a), p.min, p.max);
                // Add small noise around predicted minimum
                result[p.name] = clamp(xMin + rng.normal(0, (p.max - p.min) * 0.05), p.min, p.max);
            }
            else {
                result[p.name] = rng.range(p.min, p.max);
            }
        }
        else {
            result[p.name] = rng.range(p.min, p.max);
        }
    }
    return result;
}
function annealingSample(best, params, temperature, rng) {
    return mutateParams(best, params, temperature, rng);
}
function swarmUpdate(position, velocity, personalBest, globalBest, params, rng, inertia = 0.7, cognitive = 1.5, social = 1.5) {
    const newVel = {};
    const newPos = {};
    for (const p of params) {
        const r1 = rng ? rng.random() : Math.random();
        const r2 = rng ? rng.random() : Math.random();
        newVel[p.name] = inertia * (velocity[p.name] || 0)
            + cognitive * r1 * ((personalBest[p.name] || position[p.name]) - position[p.name])
            + social * r2 * ((globalBest[p.name] || position[p.name]) - position[p.name]);
        newPos[p.name] = clamp(position[p.name] + newVel[p.name], p.min, p.max);
    }
    return { position: newPos, velocity: newVel };
}
// ─── Novelty / Curiosity ─────────────────────────────────────────────────────
function noveltySample(params, history, resolution = 20, rng) {
    const bins = new Map();
    for (const entry of history) {
        const key = params.map(p => {
            const normalized = (entry.params[p.name] - p.min) / (p.max - p.min);
            return Math.floor(normalized * resolution);
        }).join(',');
        bins.set(key, (bins.get(key) || 0) + 1);
    }
    let minVisits = Infinity;
    let bestCandidate = null;
    for (let attempt = 0; attempt < 100; attempt++) {
        const candidate = randomParams(params, rng || new rng_1.SeededRNG());
        const key = params.map(p => {
            const normalized = (candidate[p.name] - p.min) / (p.max - p.min);
            return Math.floor(normalized * resolution);
        }).join(',');
        const visits = bins.get(key) || 0;
        if (visits < minVisits) {
            minVisits = visits;
            bestCandidate = candidate;
            if (visits === 0)
                return candidate;
        }
    }
    return bestCandidate || randomParams(params, rng || new rng_1.SeededRNG());
}
// ─── Meta-Learner (picks best strategy) ──────────────────────────────────────
class MetaLearner {
    constructor(strategyTypes, explorationRate = 0.3, rng) {
        this.explorationRate = explorationRate;
        this.rng = rng || new rng_1.SeededRNG();
        this.strategies = strategyTypes.map(type => ({
            type,
            score: 1.0,
            uses: 0,
            avgImprovement: 0,
            config: this.defaultConfig(type),
        }));
    }
    defaultConfig(type) {
        switch (type) {
            case 'grid': return { resolution: 20 };
            case 'random': return {};
            case 'bayesian': return { acquisitionFn: 'ei', kappa: 2.5 };
            case 'evolutionary': return { populationSize: 20, mutationRate: 0.1 };
            case 'gradient': return { learningRate: 0.01, momentum: 0.9 };
            case 'swarm': return { particles: 10, inertia: 0.7 };
            case 'annealing': return { initialTemp: 1.0, coolingRate: 0.995 };
            case 'bandit': return { epsilon: 0.1 };
            case 'curiosity': return { noveltyWeight: 0.8 };
            case 'exploit': return { mutationMagnitude: 0.02 };
            default: return {};
        }
    }
    /** Select next strategy using UCB1 (Upper Confidence Bound) */
    selectStrategy() {
        const totalUses = this.strategies.reduce((s, st) => s + st.uses, 0) || 1;
        if (this.rng.random() < this.explorationRate) {
            return this.rng.pick(this.strategies);
        }
        let best = null;
        let bestUCB = -Infinity;
        for (const s of this.strategies) {
            if (s.uses === 0)
                return s;
            const exploitation = s.avgImprovement;
            const exploration = Math.sqrt(2 * Math.log(totalUses) / s.uses);
            const ucb = exploitation + exploration;
            if (ucb > bestUCB) {
                bestUCB = ucb;
                best = s;
            }
        }
        return best || this.strategies[0];
    }
    updateStrategy(type, improvement) {
        const s = this.strategies.find(st => st.type === type);
        if (!s)
            return;
        s.uses++;
        s.avgImprovement = (s.avgImprovement * (s.uses - 1) + improvement) / s.uses;
        s.score = s.avgImprovement;
    }
    getStrategies() {
        return [...this.strategies].sort((a, b) => b.score - a.score);
    }
}
exports.MetaLearner = MetaLearner;
// ─── Generate Next Point ─────────────────────────────────────────────────────
function generateNextPoint(strategy, params, best, history, constraints, gridIndex, rng, evalCount) {
    let candidate;
    const maxAttempts = 50;
    const r = rng || new rng_1.SeededRNG();
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        switch (strategy.type) {
            case 'grid':
                candidate = gridSample(params, strategy.config.resolution || 20, gridIndex || r.int(0, 9999));
                break;
            case 'random':
                candidate = randomParams(params, r);
                break;
            case 'evolutionary':
                if (best && history.length > 2) {
                    const parent2 = history[r.int(0, Math.min(history.length - 1, 9))];
                    candidate = mutateParams(crossover(best.params, parent2.params, params, r), params, strategy.config.mutationRate || 0.1, r);
                }
                else {
                    candidate = randomParams(params, r);
                }
                break;
            case 'gradient':
                // Real finite-difference gradient estimation
                if (best && history.length > params.length * 2) {
                    candidate = gradientStep(best, params, history, r);
                }
                else {
                    candidate = best ? mutateParams(best.params, params, 0.05, r) : randomParams(params, r);
                }
                break;
            case 'bayesian':
                // Quadratic surrogate model
                if (best && history.length > 10) {
                    candidate = surrogateStep(best, params, history, r);
                }
                else {
                    candidate = randomParams(params, r);
                }
                break;
            case 'annealing': {
                // Eval-count-based temperature (not history.length which resets on trim)
                const evals = evalCount || history.length;
                const temp = (strategy.config.initialTemp || 1.0) * Math.pow(strategy.config.coolingRate || 0.995, evals);
                candidate = best ? annealingSample(best.params, params, temp, r) : randomParams(params, r);
                break;
            }
            case 'curiosity':
                candidate = noveltySample(params, history, 20, r);
                break;
            case 'exploit':
                candidate = best ? mutateParams(best.params, params, strategy.config.mutationMagnitude || 0.02, r) : randomParams(params, r);
                break;
            case 'swarm':
                candidate = best ? mutateParams(best.params, params, 0.15, r) : randomParams(params, r);
                break;
            case 'bandit':
            default:
                candidate = best ? mutateParams(best.params, params, 0.1, r) : randomParams(params, r);
                break;
        }
        if (satisfiesConstraints(candidate, constraints)) {
            return candidate;
        }
    }
    return randomParams(params, r);
}
//# sourceMappingURL=strategies.js.map