"use strict";
/**
 * AEGIS — Plugin System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Extensible plugin architecture for custom strategies, reporters,
 * and evaluation transforms. Add your own optimization algorithms.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.jsonReporterPlugin = exports.differentialEvolutionPlugin = exports.latinHypercubePlugin = exports.plugins = void 0;
// ─── Plugin Registry ─────────────────────────────────────────────────────────
class PluginRegistry {
    constructor() {
        this.strategies = new Map();
        this.reporters = new Map();
        this.transforms = new Map();
    }
    registerStrategy(plugin) {
        this.strategies.set(plugin.name, plugin);
    }
    registerReporter(plugin) {
        this.reporters.set(plugin.name, plugin);
    }
    registerTransform(plugin) {
        this.transforms.set(plugin.name, plugin);
    }
    getStrategy(name) {
        return this.strategies.get(name);
    }
    getAllStrategies() {
        return [...this.strategies.values()];
    }
    getAllReporters() {
        return [...this.reporters.values()];
    }
    getAllTransforms() {
        return [...this.transforms.values()];
    }
    listPlugins() {
        return {
            strategies: [...this.strategies.keys()],
            reporters: [...this.reporters.keys()],
            transforms: [...this.transforms.keys()],
        };
    }
}
exports.plugins = new PluginRegistry();
// ─── Built-in Plugin Examples ────────────────────────────────────────────────
/** Latin Hypercube Sampling — better coverage than pure random */
exports.latinHypercubePlugin = {
    name: 'latin-hypercube',
    description: 'Latin Hypercube Sampling for uniform coverage of parameter space',
    defaultConfig: { divisions: 20 },
    suggest(params, best, history, config) {
        const n = config.divisions || 20;
        const result = {};
        for (const p of params) {
            const bin = Math.floor(Math.random() * n);
            const binSize = (p.max - p.min) / n;
            result[p.name] = p.min + bin * binSize + Math.random() * binSize;
        }
        return result;
    },
};
/** Differential Evolution — powerful for non-convex problems */
exports.differentialEvolutionPlugin = {
    name: 'differential-evolution',
    description: 'Differential Evolution (DE/rand/1/bin) for rugged landscapes',
    defaultConfig: { F: 0.8, CR: 0.9 },
    suggest(params, best, history, config) {
        const F = config.F || 0.8;
        const CR = config.CR || 0.9;
        const result = {};
        if (history.length < 4) {
            // Not enough history, random sample
            for (const p of params) {
                result[p.name] = p.min + Math.random() * (p.max - p.min);
            }
            return result;
        }
        // Pick 3 random distinct solutions
        const pool = history.slice(-50);
        const indices = new Set();
        while (indices.size < 3)
            indices.add(Math.floor(Math.random() * pool.length));
        const [a, b, c] = [...indices].map(i => pool[i].params);
        // DE mutation + crossover
        const jRand = Math.floor(Math.random() * params.length);
        for (let j = 0; j < params.length; j++) {
            const p = params[j];
            if (Math.random() < CR || j === jRand) {
                result[p.name] = Math.max(p.min, Math.min(p.max, a[p.name] + F * (b[p.name] - c[p.name])));
            }
            else {
                result[p.name] = best ? best.params[p.name] : (p.min + p.max) / 2;
            }
        }
        return result;
    },
};
/** JSON file reporter — saves all events to a file */
exports.jsonReporterPlugin = {
    name: 'json-file',
    onEvent(event) {
        // In production, would append to file
        if (event.type === 'new_best' || event.type === 'discovery') {
            // Could write to disk here
        }
    },
    onComplete(state) {
        // Write final state
    },
};
// Register built-in plugins
exports.plugins.registerStrategy(exports.latinHypercubePlugin);
exports.plugins.registerStrategy(exports.differentialEvolutionPlugin);
exports.plugins.registerReporter(exports.jsonReporterPlugin);
//# sourceMappingURL=plugins.js.map