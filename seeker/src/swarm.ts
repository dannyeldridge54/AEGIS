/**
 * Seeker — Multi-Agent Swarm
 * Coordinated agents with discovery sharing, space partitioning,
 * and competitive racing. All seeded for reproducibility.
 */

import { EventEmitter } from 'events';
import { SeekerAgent } from './agent';
import { Task, AgentConfig, EvalResult, AgentState, AgentEvent, Discovery } from './interfaces';

export interface SwarmAgent {
  id: string;
  role: 'explorer' | 'exploiter' | 'scout' | 'coordinator' | 'specialist';
  agent: SeekerAgent;
  state: 'idle' | 'running' | 'waiting' | 'done';
  specialization?: string;
}

export interface AgentMessage {
  from: string;
  to: string | 'broadcast';
  type: 'discovery' | 'request' | 'result' | 'heartbeat' | 'delegate' | 'merge';
  payload: any;
  timestamp: number;
}

export class Swarm extends EventEmitter {
  private agents: Map<string, SwarmAgent> = new Map();
  private globalBest: EvalResult | null = null;
  private discoveries: Array<{ agent: string; result: EvalResult; description: string }> = [];
  private baseSeed: number;

  constructor(private config?: { maxAgents?: number; shareInterval?: number; seed?: number }) {
    super();
    this.baseSeed = config?.seed || 42;
  }

  /** Add an agent to the swarm */
  addAgent(
    id: string, task: Task,
    role: SwarmAgent['role'] = 'explorer',
    agentConfig?: AgentConfig
  ): SwarmAgent {
    const agentSeed = this.baseSeed + this.agents.size * 1000;
    const agent = new SeekerAgent(task, {
      ...agentConfig,
      verbosity: 'silent',
      seed: agentSeed,
    });

    agent.on((event) => {
      if (event.type === 'new_best') {
        this.updateGlobalBest(event.result, id);
      }
    });

    const swarmAgent: SwarmAgent = { id, role, agent, state: 'idle' };
    this.agents.set(id, swarmAgent);
    return swarmAgent;
  }

  /** Broadcast a message to all agents */
  broadcast(from: string, type: AgentMessage['type'], payload: any): void {
    this.emit('message', { from, to: 'broadcast', type, payload, timestamp: Date.now() });
  }

  /** Run the swarm — all agents work in parallel */
  async run(maxEvals?: number): Promise<{
    globalBest: EvalResult | null;
    agentResults: Array<{ id: string; role: string; best: EvalResult | null; evals: number; ufeRatio: number }>;
    discoveries: Array<{ agent: string; result: EvalResult; description: string }>;
    totalEvals: number;
  }> {
    const agents = [...this.agents.values()];
    const perAgent = maxEvals ? Math.ceil(maxEvals / agents.length) : undefined;
    console.log(`[Seeker-Swarm] Launching ${agents.length} agents...${perAgent ? ` (${perAgent} evals each)` : ''}`);

    if (perAgent) {
      for (const sa of agents) {
        (sa.agent as any).config.maxEvals = perAgent;
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
      } catch (err: any) {
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
  static partition(task: Task, nAgents: number, config?: AgentConfig & { seed?: number }): Swarm {
    const swarm = new Swarm({ seed: config?.seed });
    const splitParam = task.parameters[0];
    const rangeSize = (splitParam.max - splitParam.min) / nAgents;

    for (let i = 0; i < nAgents; i++) {
      const partitionedParams = task.parameters.map((p, idx) => {
        if (idx === 0) return { ...p, min: p.min + i * rangeSize, max: p.min + (i + 1) * rangeSize };
        return p;
      });

      const partitionedTask: Task = {
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
  static compete(task: Task, strategies: Array<{ name: string; config: AgentConfig }>, seed?: number): Swarm {
    const swarm = new Swarm({ seed });
    for (const strat of strategies) {
      swarm.addAgent(strat.name, task, 'specialist', strat.config);
    }
    return swarm;
  }

  private updateGlobalBest(result: EvalResult, agentId: string): void {
    if (!this.globalBest || result.score < this.globalBest.score) {
      this.globalBest = result;
      this.discoveries.push({
        agent: agentId, result,
        description: `Agent ${agentId} found new global best: ${result.score.toFixed(6)}`,
      });
      this.emit('global_best', { agent: agentId, result });
    }
  }

  getGlobalBest(): EvalResult | null { return this.globalBest; }
  getAgentCount(): number { return this.agents.size; }
}
