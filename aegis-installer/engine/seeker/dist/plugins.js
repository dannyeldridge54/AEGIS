"use strict";
/**
 * Seeker — Plugin System
 * Extensible strategies, reporters, and transforms.
 * Includes DE and Latin Hypercube built-in.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.differentialEvolutionPlugin = exports.latinHypercubePlugin = exports.plugins = void 0;
class PluginRegistry {
    constructor() {
        this.strategies = new Map();
        this.reporters = new Map();
        this.transforms = new Map();
    }
    registerStrategy(plugin) { this.strategies.set(plugin.name, plugin); }
    registerReporter(plugin) { this.reporters.set(plugin.name, plugin); }
    registerTransform(plugin) { this.transforms.set(plugin.name, plugin); }
    getStrategy(name) { return this.strategies.get(name); }
    getAllStrategies() { return [...this.strategies.values()]; }
    getAllReporters() { return [...this.reporters.values()]; }
    getAllTransforms() { return [...this.transforms.values()]; }
    listPlugins() {
        return {
            strategies: [...this.strategies.keys()],
            reporters: [...this.reporters.keys()],
            transforms: [...this.transforms.keys()],
        };
    }
}
exports.plugins = new PluginRegistry();
// ─── Built-in Plugins ────────────────────────────────────────────────────────
exports.latinHypercubePlugin = {
    name: 'latin-hypercube',
    description: 'Latin Hypercube Sampling for uniform parameter space coverage',
    defaultConfig: { divisions: 20 },
    suggest(params, _best, _history, config, rng) {
        const n = config.divisions || 20;
        const result = {};
        for (const p of params) {
            const bin = rng.int(0, n - 1);
            const binSize = (p.max - p.min) / n;
            result[p.name] = p.min + bin * binSize + rng.random() * binSize;
        }
        return result;
    },
};
exports.differentialEvolutionPlugin = {
    name: 'differential-evolution',
    description: 'DE/rand/1/bin for rugged landscapes',
    defaultConfig: { F: 0.8, CR: 0.9 },
    suggest(params, best, history, config, rng) {
        const F = config.F || 0.8;
        const CR = config.CR || 0.9;
        const result = {};
        if (history.length < 4) {
            for (const p of params)
                result[p.name] = rng.range(p.min, p.max);
            return result;
        }
        const pool = history.slice(-50);
        const indices = new Set();
        while (indices.size < 3)
            indices.add(rng.int(0, pool.length - 1));
        const [a, b, c] = [...indices].map(i => pool[i].params);
        const jRand = rng.int(0, params.length - 1);
        for (let j = 0; j < params.length; j++) {
            const p = params[j];
            if (rng.random() < CR || j === jRand) {
                result[p.name] = Math.max(p.min, Math.min(p.max, a[p.name] + F * (b[p.name] - c[p.name])));
            }
            else {
                result[p.name] = best ? best.params[p.name] : (p.min + p.max) / 2;
            }
        }
        return result;
    },
};
exports.plugins.registerStrategy(exports.latinHypercubePlugin);
exports.plugins.registerStrategy(exports.differentialEvolutionPlugin);
//# sourceMappingURL=plugins.js.map