/**
 * AEGIS — Multi-Agent Swarm Communication
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Agent-to-agent messaging, task delegation, and swarm coordination.
 * Agents can specialize, share discoveries, and cooperate on problems.
 */
import { EventEmitter } from 'events';
import { AegisAgent } from './agent';
import { Task, AgentConfig, EvalResult } from './interfaces';
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
export declare class Swarm extends EventEmitter {
    private config?;
    private agents;
    private messageQueue;
    private globalBest;
    private discoveries;
    constructor(config?: {
        maxAgents?: number;
        shareInterval?: number;
    } | undefined);
    /** Add an agent to the swarm */
    addAgent(id: string, task: Task, role?: SwarmAgent['role'], agentConfig?: AgentConfig): SwarmAgent;
    /** Send message to specific agent or broadcast */
    send(message: AgentMessage): void;
    /** Broadcast to all agents */
    broadcast(from: string, type: AgentMessage['type'], payload: any): void;
    /**
     * Run the swarm — all agents work in parallel.
     * Agents share discoveries: when one finds a new best, others are seeded with it.
     */
    run(maxEvals?: number): Promise<{
        globalBest: EvalResult | null;
        agentResults: Array<{
            id: string;
            role: string;
            best: EvalResult | null;
            evals: number;
        }>;
        discoveries: Array<{
            agent: string;
            result: EvalResult;
            description: string;
        }>;
        totalEvals: number;
    }>;
    /** Divide parameter space among agents (partition strategy) */
    static partition(task: Task, nAgents: number, config?: AgentConfig): Swarm;
    /** Create a competitive swarm (different strategies race) */
    static compete(task: Task, strategies: Array<{
        name: string;
        config: AgentConfig;
    }>): Swarm;
    private updateGlobalBest;
    getGlobalBest(): EvalResult | null;
    getAgentCount(): number;
}
//# sourceMappingURL=swarm.d.ts.map