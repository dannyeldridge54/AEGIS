/**
 * AEGIS — Live Web Dashboard
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Serves a real-time web dashboard showing agent progress.
 * Zero dependencies — uses Node's built-in http module.
 */
import { AgentState, AgentEvent } from './interfaces';
export interface DashboardServer {
    start(): void;
    stop(): void;
    updateState(state: AgentState): void;
    addLog(entry: {
        type: string;
        text: string;
    }): void;
}
export declare function createDashboard(port?: number): DashboardServer;
/**
 * Event handler that feeds the dashboard.
 * Usage: agent.on(dashboardHandler(dashboard));
 */
export declare function dashboardHandler(dashboard: DashboardServer): (event: AgentEvent) => void;
//# sourceMappingURL=dashboard.d.ts.map