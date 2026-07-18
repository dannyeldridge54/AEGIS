"use strict";
/**
 * Seeker — Multi-Agent Swarm
 * Coordinated agents with discovery sharing, space partitioning,
 * and competitive racing. All seeded for reproducibility.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Swarm = void 0;
const events_1 = require("events");
const agent_1 = require("./agent");
class Swarm extends events_1.EventEmitter {
    constructor(config) {
        super();
        this.config = config;
        this.agents = new Map();
        this.globalBest = null;
        this.discoveries = [];
        this.baseSeed = config?.seed || 42;
    }
    /** Add an agent to the swarm */
    addAgent(id, task, role = 'explorer', agentConfig) {
        const agentSeed = this.baseSeed + this.agents.size * 1000;
        const agent = new agent_1.SeekerAgent(task, {
            ...agentConfig,
            verbosity: 'silent',
            seed: agentSeed,
        });
        agent.on((event) => {
            if (event.type === 'new_best') {
                this.updateGlobalBest(event.result, id);
            }
        });
        const swarmAgent = { id, role, agent, state: 'idle' };
        this.agents.set(id, swarmAgent);
        return swarmAgent;
    }
    /** Broadcast a message to all agents */
    broadcast(from, type, payload) {
        this.emit('message', { from, to: 'broadcast', type, payload, timestamp: Date.now() });
    }
    /** Run the swarm — all agents work in parallel */
    async run(maxEvals) {
        const agents = [...this.agents.values()];
        const perAgent = maxEvals ? Math.ceil(maxEvals / agents.length) : undefined;
        console.log(`[Seeker-Swarm] Launching ${agents.length} agents...${perAgent ? ` (${perAgent} evals each)` : ''}`);
        if (perAgent) {
            for (const sa of agents) {
                sa.agent.config.maxEvals = perAgent;
            }
        }
        // Cross-pollination: inject discoveries into other agents
        for (const sa of agents) {
            sa.agent.on((event) => {
                if (event.type === 'new_best') {
                    for (const other of agents) {
                        if (other.id !== sa.id && other.state === 'running') {
                            const otherState = other.agent.getState();
                            otherState.history.push(event.result);
                        }
                    }
                }
            });
        }
        const promises = agents.map(async (sa) => {
            sa.state = 'running';
            try {
                const state = await sa.agent.run();
                sa.state = 'done';
                return { id: sa.id, role: sa.role, best: state.best, evals: state.totalEvals, ufeRatio: state.ufe.ufeRatio };
            }
            catch (err) {
                sa.state = 'done';
                console.log(`[Seeker-Swarm] Agent ${sa.id} failed: ${err.message}`);
                return { id: sa.id, role: sa.role, best: null, evals: 0, ufeRatio: 0 };
            }
        });
        const results = await Promise.all(promises);
        const totalEvals = results.reduce((s, r) => s + r.evals, 0);
        console.log(`[Seeker-Swarm] Complete! ${totalEvals} total evals across ${agents.length} agents`);
        if (this.globalBest) {
            console.log(`[Seeker-Swarm] Global best: ${this.globalBest.score.toFixed(6)}`);
        }
        return { globalBest: this.globalBest, agentResults: results, discoveries: this.discoveries, totalEvals };
    }
    /** Divide parameter space among agents */
    static partition(task, nAgents, config) {
        const swarm = new Swarm({ seed: config?.seed });
        const splitParam = task.parameters[0];
        const rangeSize = (splitParam.max - splitParam.min) / nAgents;
        for (let i = 0; i < nAgents; i++) {
            const partitionedParams = task.parameters.map((p, idx) => {
                if (idx === 0)
                    return { ...p, min: p.min + i * rangeSize, max: p.min + (i + 1) * rangeSize };
                return p;
            });
            const partitionedTask = {
                ...task, id: `${task.id}-p${i}`, name: `${task.name} [${i + 1}/${nAgents}]`,
                parameters: partitionedParams,
            };
            swarm.addAgent(`agent-${i}`, partitionedTask, i === 0 ? 'coordinator' : 'explorer', {
                ...config, maxEvals: (config?.maxEvals || 5000) / nAgents,
            });
        }
        return swarm;
    }
    /** Create a competitive swarm (different strategies race) */
    static compete(task, strategies, seed) {
        const swarm = new Swarm({ seed });
        for (const strat of strategies) {
            swarm.addAgent(strat.name, task, 'specialist', strat.config);
        }
        return swarm;
    }
    updateGlobalBest(result, agentId) {
        if (!this.globalBest || result.score < this.globalBest.score) {
            this.globalBest = result;
            this.discoveries.push({
                agent: agentId, result,
                description: `Agent ${agentId} found new global best: ${result.score.toFixed(6)}`,
            });
            this.emit('global_best', { agent: agentId, result });
        }
    }
    getGlobalBest() { return this.globalBest; }
    getAgentCount() { return this.agents.size; }
}
exports.Swarm = Swarm;
//# sourceMappingURL=swarm.js.map