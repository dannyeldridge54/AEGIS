/**
 * AEGIS — Live Monitor & Alert System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Real-time tracking of optimization runs with categorized alerts:
 *  • Breakthroughs — major score improvements
 *  • Anomalies — z-score outliers, landscape shifts
 *  • Insights — strategy effectiveness, phase transitions, convergence patterns
 *  • Plateaus — stagnation detection with suggested actions
 *
 * Serves a live HTTP dashboard + emits structured JSON events.
 */
import { AgentEvent, UFEMetrics } from './interfaces';
export type AlertSeverity = 'info' | 'warning' | 'critical' | 'breakthrough';
export interface Alert {
    id: string;
    timestamp: number;
    severity: AlertSeverity;
    category: 'breakthrough' | 'anomaly' | 'insight' | 'plateau' | 'milestone' | 'strategy';
    title: string;
    detail: string;
    data?: Record<string, any>;
    acknowledged: boolean;
}
export interface MonitorSnapshot {
    /** Current run status */
    status: 'running' | 'paused' | 'completed' | 'idle';
    /** Uptime in seconds */
    uptime: number;
    /** Active run states (keyed by run/job ID) */
    runs: Record<string, RunTracker>;
    /** All alerts (newest first) */
    alerts: Alert[];
    /** Summary counts */
    summary: {
        totalRuns: number;
        totalEvals: number;
        totalBreakthroughs: number;
        totalAnomalies: number;
        activeAlerts: number;
    };
}
export interface RunTracker {
    id: string;
    name: string;
    startedAt: number;
    status: 'running' | 'completed' | 'failed';
    totalEvals: number;
    bestScore: number | null;
    bestParams: Record<string, number> | null;
    ufe: UFEMetrics | null;
    phase: string;
    improvements: number;
    lastImprovedAt: number;
    scoreHistory: Array<{
        eval: number;
        score: number;
        timestamp: number;
    }>;
    strategyWins: Record<string, number>;
    discoveryCount: number;
}
export interface MonitorConfig {
    /** HTTP port for the live dashboard (0 = disabled) */
    port?: number;
    /** Max alerts to retain */
    maxAlerts?: number;
    /** Max score history points per run */
    maxScoreHistory?: number;
    /** Breakthrough threshold: improvement must be > this fraction of current best */
    breakthroughThreshold?: number;
    /** Stagnation window: evals without improvement to trigger plateau alert */
    stagnationWindow?: number;
    /** Log file path for alerts */
    alertLogFile?: string;
    /** Webhook URL for critical/breakthrough alerts */
    webhookUrl?: string;
}
export declare class LiveMonitor {
    private config;
    private runs;
    private alerts;
    private alertCounter;
    private server;
    private startTime;
    private alertLogStream;
    private listeners;
    private scoreboardData;
    private equationData;
    /** Set cross-engine scoreboard data (called by runner) */
    setScoreboard(data: typeof this.scoreboardData): void;
    /** Set best equation discovered (called by runner) */
    setEquation(data: typeof this.equationData): void;
    constructor(config?: MonitorConfig);
    /** Register a new optimization run to track */
    registerRun(id: string, name: string): RunTracker;
    /** Create an event handler to plug into agent.on() */
    createHandler(runId: string): (event: AgentEvent) => void;
    private onEvaluation;
    private onNewBest;
    private onDiscovery;
    private onPhaseChange;
    private onReport;
    private onStopped;
    private onConverged;
    private addAlert;
    /** Subscribe to alerts */
    onAlert(listener: (alert: Alert) => void): void;
    /** Acknowledge an alert */
    acknowledgeAlert(alertId: string): boolean;
    /** Get alerts filtered by category/severity */
    getAlerts(filter?: {
        category?: Alert['category'];
        severity?: AlertSeverity;
        unacknowledgedOnly?: boolean;
    }): Alert[];
    /** Get full monitoring snapshot */
    getSnapshot(): MonitorSnapshot;
    /** Start the live HTTP dashboard */
    startDashboard(): void;
    /** Stop the dashboard */
    stopDashboard(): void;
    /** Print a formatted status report to console */
    printStatus(): void;
    private getLastImprovedEval;
    private phaseAdvice;
    private sendWebhook;
    private renderDashboardHTML;
}
/**
 * Create a live monitor and start the dashboard.
 *
 * @example
 * const monitor = createMonitor({ port: 5555 });
 * const agent = new AegisAgent(task, config);
 * agent.on(monitor.createHandler('run-1'));
 * monitor.startDashboard();
 * await agent.run();
 * monitor.printStatus();
 */
export declare function createMonitor(config?: MonitorConfig): LiveMonitor;
//# sourceMappingURL=monitor.d.ts.map