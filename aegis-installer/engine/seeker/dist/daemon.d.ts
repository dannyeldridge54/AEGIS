/**
 * Seeker — Daemon Mode
 * Persistent background daemon: schedules jobs, tracks UFE per job,
 * learns across runs, serves results via HTTP API.
 */
import { Task, AgentConfig, EvalResult } from './interfaces';
import { Memory } from './memory';
export interface DaemonConfig {
    name?: string;
    workDir?: string;
    apiPort?: number;
    webhookUrl?: string;
    maxConcurrent?: number;
    saveInterval?: number;
    language?: string;
    logFile?: string;
    enableMemory?: boolean;
}
export interface DaemonJob {
    id: string;
    name: string;
    task: Task;
    config?: AgentConfig;
    schedule: 'continuous' | 'once' | number;
    chainTo?: string;
    watch?: string;
    priority?: number;
    tags?: string[];
}
interface JobState {
    id: string;
    status: 'queued' | 'running' | 'paused' | 'completed' | 'failed';
    runs: number;
    totalEvals: number;
    best: EvalResult | null;
    lastRun: number;
    nextRun: number;
    errors: string[];
    ufeRatio: number;
    discoveries: number;
    history: Array<{
        timestamp: number;
        score: number;
        evals: number;
        ufeRatio: number;
    }>;
}
export declare class SeekerDaemon {
    private config;
    private jobs;
    private jobStates;
    private running;
    private memory;
    private startTime;
    private server;
    private intervals;
    private activeAgents;
    private logStream;
    constructor(config?: DaemonConfig);
    addJob(job: DaemonJob): void;
    removeJob(id: string): boolean;
    pauseJob(id: string): void;
    resumeJob(id: string): void;
    getJobStates(): JobState[];
    start(): Promise<void>;
    stop(): void;
    private tick;
    private runJob;
    private startAPI;
    private alert;
    private saveState;
    private loadState;
    private log;
    private printBanner;
    getMemory(): Memory;
    getUptime(): number;
    isRunning(): boolean;
}
export declare function startDaemon(name: string, jobs: DaemonJob[], config?: Partial<DaemonConfig>): SeekerDaemon;
export {};
//# sourceMappingURL=daemon.d.ts.map