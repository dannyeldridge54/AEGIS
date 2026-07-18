"use strict";
/**
 * Seeker — Self-Evolving Strategy Engine
 * Strategies that learn to modify their own hyperparameters.
 * Meta-optimizes mutation rate, temperature schedule, learning rate, etc.
 * Uses seeded RNG for reproducible evolution.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.SelfEvolver = void 0;
const rng_1 = require("./rng");
/**
 * Self-evolving strategy system.
 * Treats strategy hyperparameters as their own optimization problem.
 * The meta-meta-learner evolves these automatically.
 */
class SelfEvolver {
    constructor(config) {
        this.population = [];
        this.generation = 0;
        this.bestGenome = null;
        this.config = {
            generations: config?.generations || 20,
            populationSize: config?.populationSize || 12,
            mutationRate: config?.mutationRate || 0.3,
            eliteRatio: config?.eliteRatio || 0.25,
            seed: config?.seed || 0,
        };
        this.rng = new rng_1.SeededRNG(this.config.seed || undefined);
        this.initPopulation();
    }
    initPopulation() {
        const strategySpace = [
            { type: 'evolutionary', paramRanges: { mutationRate: [0.01, 0.5], populationSize: [5, 50] } },
            { type: 'annealing', paramRanges: { initialTemp: [0.1, 5.0], coolingRate: [0.9, 0.999] } },
            { type: 'gradient', paramRanges: { learningRate: [0.001, 0.5] } },
            { type: 'exploit', paramRanges: { mutationMagnitude: [0.005, 0.2] } },
            { type: 'curiosity', paramRanges: { noveltyWeight: [0.3, 1.0] } },
        ];
        for (let i = 0; i < this.config.populationSize; i++) {
            const template = strategySpace[i % strategySpace.length];
            const config = {};
            for (const [key, [min, max]] of Object.entries(template.paramRanges)) {
                config[key] = this.rng.range(min, max);
            }
            this.population.push({ type: template.type, config, fitness: 0, generation: 0 });
        }
    }
    /** Evaluate a genome by running a mini-optimization */
    async evaluateGenome(genome, task, budget = 200) {
        const childRng = this.rng.fork();
        let best = Infinity;
        let improvement = 0;
        for (let i = 0; i < budget; i++) {
            const params = {};
            const magnitude = genome.config.mutationMagnitude || genome.config.mutationRate || 0.1;
            if (best < Infinity && childRng.random() > 0.3) {
                // Mutate from best
                for (const p of task.parameters) {
                    const range = p.max - p.min;
                    params[p.name] = Math.max(p.min, Math.min(p.max, best + (childRng.random() - 0.5) * 2 * magnitude * range));
                }
            }
            else {
                for (const p of task.parameters) {
                    params[p.name] = childRng.range(p.min, p.max);
                }
            }
            const score = task.evaluate(params);
            if (score < best) {
                improvement += best === Infinity ? 0 : best - score;
                best = score;
            }
        }
        return improvement;
    }
    /** Run one generation of evolution */
    async evolveGeneration(task) {
        for (const genome of this.population) {
            genome.fitness = await this.evaluateGenome(genome, task);
        }
        this.population.sort((a, b) => b.fitness - a.fitness);
        if (!this.bestGenome || this.population[0].fitness > this.bestGenome.fitness) {
            this.bestGenome = { ...this.population[0] };
        }
        const eliteCount = Math.ceil(this.config.populationSize * this.config.eliteRatio);
        const elites = this.population.slice(0, eliteCount);
        const newPop = [...elites];
        while (newPop.length < this.config.populationSize) {
            const parent = this.rng.pick(elites);
            const child = {
                type: parent.type,
                config: { ...parent.config },
                fitness: 0,
                generation: this.generation + 1,
            };
            for (const key of Object.keys(child.config)) {
                if (this.rng.random() < this.config.mutationRate) {
                    child.config[key] *= 0.5 + this.rng.random();
                }
            }
            newPop.push(child);
        }
        this.population = newPop;
        this.generation++;
    }
    /** Full evolution run — returns the best strategy configuration */
    async evolve(task, verbose = true) {
        if (verbose) {
            console.log(`[Seeker-Evolve] Self-evolving over ${this.config.generations} generations (seed=${this.rng.seed})...`);
        }
        for (let g = 0; g < this.config.generations; g++) {
            await this.evolveGeneration(task);
            if (verbose && g % 5 === 0) {
                const best = this.population[0];
                console.log(`  Gen ${g}: best=${best.type} fitness=${best.fitness.toFixed(4)} config=${JSON.stringify(best.config)}`);
            }
        }
        const winner = this.bestGenome || this.population[0];
        if (verbose) {
            console.log(`[Seeker-Evolve] Winner: ${winner.type} with config:`, winner.config);
        }
        return { type: winner.type, config: winner.config };
    }
}
exports.SelfEvolver = SelfEvolver;
//# sourceMappingURL=self-evolve.js.map