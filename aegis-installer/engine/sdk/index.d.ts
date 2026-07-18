/**
 * AEGIS Optimizer — TypeScript Type Definitions
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 */

export interface Parameter {
  name: string;
  min: number;
  max: number;
  description?: string;
}

export interface OptimizeOptions {
  /** The objective function to minimize. Receives a params object, returns a number. */
  objective: (params: Record<string, number>) => number;
  /** Parameter definitions with bounds. */
  parameters: Parameter[];
  /** Maximum number of function evaluations (default: 1000). */
  maxEvals?: number;
  /** Random seed for reproducibility. */
  seed?: number;
  /** Logging verbosity: 'silent' | 'minimal' | 'verbose' (default: 'silent'). */
  verbosity?: 'silent' | 'minimal' | 'verbose';
}

export interface DualOptimizeOptions extends OptimizeOptions {
  /** Number of dual-engine cycles (default: 5). */
  cycles?: number;
}

export interface MonitorOptions extends OptimizeOptions {
  /** HTTP port for the live dashboard (default: 8080). */
  port?: number;
}

export interface UFEMetrics {
  totalEvals: number;
  usefulEvals: number;
  ufeRatio: number;
  convergenceVelocity: number;
  aucc: number | null;
  timeToTarget: {
    pct10: number | null;
    pct50: number | null;
    pct90: number | null;
  };
  convergenceCurve: [number, number | null][];
}

export interface OptimizeResult {
  best: {
    params: Record<string, number>;
    score: number;
  } | null;
  totalEvals: number;
  runtime: number;
  ufe: UFEMetrics;
  phase: string;
  discoveries: Array<{
    params: Record<string, number>;
    score: number;
    strategy: string;
  }>;
}

/**
 * Run single-engine optimization.
 * Uses 7 auto-balanced strategies to find the global minimum.
 */
export function optimize(options: OptimizeOptions): Promise<OptimizeResult>;

/**
 * Run dual-engine optimization with cross-pollination.
 * AEGIS explores wide, Seeker refines deep. They share discoveries.
 * Typically 20-40% better than single engine.
 */
export function dualOptimize(options: DualOptimizeOptions): Promise<OptimizeResult>;

/**
 * Run optimization with a live web dashboard.
 * Opens an HTTP server showing real-time convergence curves and strategy stats.
 */
export function optimizeWithMonitor(options: MonitorOptions): Promise<OptimizeResult>;

/**
 * The AEGIS agent class for advanced usage.
 */
export class AegisAgent {
  constructor(task: any, options?: any);
  seed(params: Record<string, number>, score: number): void;
  run(optimum?: number): Promise<any>;
  on(handler: (event: any) => void): void;
}

/**
 * The Seeker agent class for advanced usage.
 */
export class SeekerAgent {
  constructor(task: any, options?: any);
  seed(params: Record<string, number>, score: number): void;
  run(optimum?: number): Promise<any>;
  on(handler: (event: any) => void): void;
}
