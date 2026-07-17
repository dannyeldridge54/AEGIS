/**
 * AEGIS — Multi-Agent Swarm Communication
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Agent-to-agent messaging, task delegation, and swarm coordination.
 * Agents can specialize, share discoveries, and cooperate on problems.
 */

import { EventEmitter } from 'events';
import { AegisAgent } from './agent';
import { Task, AgentConfig, EvalResult, AgentState, ParameterDef } from './interfaces';

// ─── Message Protocol ────────────────────────────────────────────────────────

export interface AgentMessage {
  from: string;
  to: string | 'broadcast';
  type: 'discovery' | 'request' | 'result' | 'heartbeat' | 'delegate' | 'merge';
  payload: any;
  timestamp: number;
}

export interface SwarmAgent {
  id: string;
  role: 'explorer' | 'exploiter' | 'scout' | 'coordinator' | 'specialist';
  agent: AegisAgent;
  state: 'idle' | 'running' | 'waiting' | 'done';
  specialization?: string;
}

// ─── Swarm Coordinator ───────────────────────────────────────────────────────

export class Swarm extends EventEmitter {
  private agents: Map<string, SwarmAgent> = new Map();
  private messageQueue: AgentMessage[] = [];
  private globalBest: EvalResult | null = null;
  private discoveries: Array<{ agent: string; result: EvalResult; description: string }> = [];

  constructor(private config?: { maxAgents?: number; shareInterval?: number }) {
    super();
  }

  /** Add an agent to the swarm */
  addAgent(
    id: string,
    task: Task,
    role: SwarmAgent['role'] = 'explorer',
    agentConfig?: AgentConfig
  ): SwarmAgent {
    const agent = new AegisAgent(task, {
      ...agentConfig,
      verbosity: 'silent',
    });

    // Wire up discovery sharing
    agent.on((event) => {
      if (event.type === 'new_best') {
        this.broadcast(id, 'discovery', {
          score: event.result.score,
          params: event.result.params,
          strategy: event.result.strategy,
        });
        this.updateGlobalBest(event.result, id);
      }
    });

    const swarmAgent: SwarmAgent = { id, role, agent, state: 'idle' };
    this.agents.set(id, swarmAgent);
    return swarmAgent;
  }

  /** Send message to specific agent or broadcast */
  send(message: AgentMessage): void {
    this.messageQueue.push(message);
    this.emit('message', message);
  }

  /** Broadcast to all agents */
  broadcast(from: string, type: AgentMessage['type'], payload: any): void {
    this.send({ from, to: 'broadcast', type, payload, timestamp: Date.now() });
  }

  /**
   * Run the swarm — all agents work in parallel.
   * Agents share discoveries: when one finds a new best, others are seeded with it.
   */
  async run(maxEvals?: number): Promise<{
    globalBest: EvalResult | null;
    agentResults: Array<{ id: string; role: string; best: EvalResult | null; evals: number }>;
    discoveries: Array<{ agent: string; result: EvalResult; description: string }>;
    totalEvals: number;
  }> {
    const agents = [...this.agents.values()];
    const perAgent = maxEvals ? Math.ceil(maxEvals / agents.length) : undefined;
    console.log(`[AEGIS-Swarm] Launching ${agents.length} agents...${perAgent ? ` (${perAgent} evals each)` : ''}`);

    // Override maxEvals if specified
    if (perAgent) {
      for (const sa of agents) {
        (sa.agent as any).config.maxEvals = perAgent;
      }
    }

    // Cross-pollination: when one agent finds a best, inject it into others' histories
    for (const sa of agents) {
      sa.agent.on((event) => {
        if (event.type === 'new_best') {
          // Inject discovery into other agents' evaluation history for better convergence
          for (const other of agents) {
            if (other.id !== sa.id && other.state === 'running') {
              const otherState = other.agent.getState();
              otherState.history.push(event.result);
            }
          }
        }
      });
    }

    // Start all agents in parallel
    const promises = agents.map(async (sa) => {
      sa.state = 'running';
      try {
        const state = await sa.agent.run();
        sa.state = 'done';
        return { id: sa.id, role: sa.role, best: state.best, evals: state.totalEvals };
      } catch (err: any) {
        sa.state = 'done';
        console.log(`[AEGIS-Swarm] Agent ${sa.id} failed: ${err.message}`);
        return { id: sa.id, role: sa.role, best: null, evals: 0 };
      }
    });

    const results = await Promise.all(promises);
    const totalEvals = results.reduce((s, r) => s + r.evals, 0);

    console.log(`[AEGIS-Swarm] Complete! ${totalEvals} total evals across ${agents.length} agents`);
    if (this.globalBest) {
      console.log(`[AEGIS-Swarm] Global best: ${this.globalBest.score.toFixed(6)}`);
    }

    return {
      globalBest: this.globalBest,
      agentResults: results,
      discoveries: this.discoveries,
      totalEvals,
    };
  }

  /** Divide parameter space among agents (partition strategy) */
  static partition(
    task: Task,
    nAgents: number,
    config?: AgentConfig
  ): Swarm {
    const swarm = new Swarm();
    const params = task.parameters;

    // Split the most important parameter range among agents
    const splitParam = params[0]; // Split on first param
    const rangeSize = (splitParam.max - splitParam.min) / nAgents;

    for (let i = 0; i < nAgents; i++) {
      const partitionedParams = params.map((p, idx) => {
        if (idx === 0) {
          return { ...p, min: p.min + i * rangeSize, max: p.min + (i + 1) * rangeSize };
        }
        return p;
      });

      const partitionedTask: Task = {
        ...task,
        id: `${task.id}-partition-${i}`,
        name: `${task.name} [${i + 1}/${nAgents}]`,
        parameters: partitionedParams,
      };

      const role: SwarmAgent['role'] = i === 0 ? 'coordinator' : 'explorer';
      swarm.addAgent(`agent-${i}`, partitionedTask, role, {
        ...config,
        maxEvals: (config?.maxEvals || 5000) / nAgents,
      });
    }

    return swarm;
  }

  /** Create a competitive swarm (different strategies race) */
  static compete(
    task: Task,
    strategies: Array<{ name: string; config: AgentConfig }>,
  ): Swarm {
    const swarm = new Swarm();

    for (const strat of strategies) {
      swarm.addAgent(strat.name, task, 'specialist', strat.config);
    }

    return swarm;
  }

  private updateGlobalBest(result: EvalResult, agentId: string): void {
    if (!this.globalBest || result.score < this.globalBest.score) {
      this.globalBest = result;
      this.discoveries.push({
        agent: agentId,
        result,
        description: `Agent ${agentId} found new global best: ${result.score.toFixed(6)}`,
      });
      this.emit('global_best', { agent: agentId, result });
    }
  }

  getGlobalBest(): EvalResult | null { return this.globalBest; }
  getAgentCount(): number { return this.agents.size; }
}
