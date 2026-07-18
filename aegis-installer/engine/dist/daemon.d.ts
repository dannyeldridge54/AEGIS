/**
 * AEGIS — Universal Daemon Mode
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Runs AEGIS as a persistent background daemon that:
 * - Continuously optimizes any registered task
 * - Self-schedules work (cron-like or continuous)
 * - Watches files/APIs for changes and re-optimizes
 * - Chains tasks (output of one feeds into another)
 * - Serves results via HTTP API
 * - Sends alerts on discoveries (webhook, file, console)
 * - Manages multiple concurrent optimization jobs
 * - Learns across runs (persistent memory)
 *
 * Think of it as a never-sleeping optimization engine for anything.
 */
import { Task, AgentConfig, EvalResult } from './interfaces';
import { Memory } from './memory';
export interface DaemonConfig {
    /** Daemon name (shows in dashboard/logs) */
    name?: string;
    /** Working directory for state/logs */
    workDir?: string;
    /** HTTP API port (0 = disabled) */
    apiPort?: number;
    /** Dashboard port (0 = disabled) */
    dashboardPort?: number;
    /** Alert webhook URL */
    webhookUrl?: string;
    /** Max concurrent jobs */
    maxConcurrent?: number;
    /** Auto-save interval (seconds) */
    saveInterval?: number;
    /** Language */
    language?: string;
    /** Log file path */
    logFile?: string;
    /** Enable persistent memory */
    enableMemory?: boolean;
}
export interface DaemonJob {
    id: string;
    name: string;
    task: Task;
    config?: AgentConfig;
    /** Schedule: 'continuous' | 'once' | cron-like interval in seconds */
    schedule: 'continuous' | 'once' | number;
    /** Chain: feed results to another job */
    chainTo?: string;
    /** Watch: re-run when this file/URL changes */
    watch?: string;
    /** Priority (higher = runs first) */
    priority?: number;
    /** Tags for filtering */
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
    history: Array<{
        timestamp: number;
        score: number;
        evals: number;
    }>;
}
export declare class AegisDaemon {
    private config;
    private jobs;
    private jobStates;
    private running;
    private memory;
    private startTime;
    private server;
    private dashboard;
    private intervals;
    private activeAgents;
    private logStream;
    constructor(config?: DaemonConfig);
    /** Register a job */
    addJob(job: DaemonJob): void;
    /** Remove a job (stops it if running) */
    removeJob(id: string): boolean;
    /** Pause a job */
    pauseJob(id: string): void;
    /** Resume a job */
    resumeJob(id: string): void;
    /** Get all job statuses */
    getJobStates(): JobState[];
    /** Start the daemon */
    start(): Promise<void>;
    /** Stop the daemon gracefully */
    stop(): void;
    /** Main tick — schedules and runs jobs */
    private tick;
    /** Execute a single job */
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
/**
 * Create and start a daemon in one call.
 *
 * @example
 * const daemon = startDaemon('My Optimizer', [
 *   { id: 'tune-api', name: 'API Tuning', task: apiTask, schedule: 3600 },
 *   { id: 'explore', name: 'Parameter Space', task: exploreTask, schedule: 'continuous' },
 * ]);
 */
export declare function startDaemon(name: string, jobs: DaemonJob[], config?: Partial<DaemonConfig>): AegisDaemon;
export {};
//# sourceMappingURL=daemon.d.ts.map