/**
 * Seeker — Multi-Agent Swarm
 * Coordinated agents with discovery sharing, space partitioning,
 * and competitive racing. All seeded for reproducibility.
 */
import { EventEmitter } from 'events';
import { SeekerAgent } from './agent';
import { Task, AgentConfig, EvalResult } from './interfaces';
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
export declare class Swarm extends EventEmitter {
    private config?;
    private agents;
    private globalBest;
    private discoveries;
    private baseSeed;
    constructor(config?: {
        maxAgents?: number;
        shareInterval?: number;
        seed?: number;
    } | undefined);
    /** Add an agent to the swarm */
    addAgent(id: string, task: Task, role?: SwarmAgent['role'], agentConfig?: AgentConfig): SwarmAgent;
    /** Broadcast a message to all agents */
    broadcast(from: string, type: AgentMessage['type'], payload: any): void;
    /** Run the swarm — all agents work in parallel */
    run(maxEvals?: number): Promise<{
        globalBest: EvalResult | null;
        agentResults: Array<{
            id: string;
            role: string;
            best: EvalResult | null;
            evals: number;
            ufeRatio: number;
        }>;
        discoveries: Array<{
            agent: string;
            result: EvalResult;
            description: string;
        }>;
        totalEvals: number;
    }>;
    /** Divide parameter space among agents */
    static partition(task: Task, nAgents: number, config?: AgentConfig & {
        seed?: number;
    }): Swarm;
    /** Create a competitive swarm (different strategies race) */
    static compete(task: Task, strategies: Array<{
        name: string;
        config: AgentConfig;
    }>, seed?: number): Swarm;
    private updateGlobalBest;
    getGlobalBest(): EvalResult | null;
    getAgentCount(): number;
}
//# sourceMappingURL=swarm.d.ts.map