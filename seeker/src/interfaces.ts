/**
 * Seeker — Core Interfaces
 * Evolved from AEGIS. Copyright (c) 2012-2026 Danny Lee Eldridge.
 *
 * Autonomous discovery engine: solves UFE optimization, hunts anomalies,
 * surfaces new discoveries. Scripts, records, and learns from every evaluation.
 */

// ─── Natural Language Goal ───────────────────────────────────────────────────

export interface Goal {
  description: string;
  metric?: string;
  target?: number;
  minimize?: boolean;
  timeBudget?: number;
  priority?: number;
}

// ─── Task (what Seeker operates on) ──────────────────────────────────────────

export interface Task {
  id: string;
  name: string;
  evaluate: (params: Record<string, number>) => number | Promise<number>;
  parameters: ParameterDef[];
  constraints?: Constraint[];
  meta?: Record<string, any>;
}

export interface ParameterDef {
  name: string;
  min: number;
  max: number;
  default?: number;
  step?: number;
  description?: string;
}

export interface Constraint {
  params: string[];
  check: (values: Record<string, number>) => boolean;
  description?: string;
}

// ─── Strategy System ─────────────────────────────────────────────────────────

export type StrategyType =
  | 'grid'
  | 'random'
  | 'bayesian'
  | 'evolutionary'
  | 'gradient'
  | 'swarm'
  | 'annealing'
  | 'bandit'
  | 'curiosity'
  | 'exploit';

export interface Strategy {
  type: StrategyType;
  score: number;
  uses: number;
  avgImprovement: number;
  config: Record<string, any>;
}

// ─── Agent State ─────────────────────────────────────────────────────────────

export interface AgentState {
  best: EvalResult | null;
  totalEvals: number;
  history: EvalResult[];
  strategies: Strategy[];
  discoveries: Discovery[];
  runtime: number;
  phase: 'exploring' | 'exploiting' | 'curious' | 'converged';
  /** UFE metrics tracked throughout the run */
  ufe: UFEMetrics;
}

export interface EvalResult {
  params: Record<string, number>;
  score: number;
  timestamp: number;
  strategy: StrategyType;
  metadata?: Record<string, any>;
}

export interface Discovery {
  type: 'new_best' | 'anomaly' | 'plateau' | 'convergence' | 'constraint_boundary' | 'landscape_shift';
  description: string;
  result: EvalResult;
  confidence: number;
  timestamp: number;
}

// ─── Agent Configuration ─────────────────────────────────────────────────────

export interface AgentConfig {
  goal?: string | Goal;
  reportInterval?: number;
  maxEvals?: number;
  convergenceThreshold?: number;
  explorationRate?: number;
  strategies?: StrategyType[];
  verbosity?: 'silent' | 'minimal' | 'normal' | 'verbose';
  persistence?: { enabled: boolean; path?: string; interval?: number };
  language?: string;
  /** RNG seed for reproducibility. Omit for random seed. */
  seed?: number;
  /** Novelty resolution for curiosity-driven UFE tracking */
  noveltyResolution?: number;
}

// ─── UFE Metrics ─────────────────────────────────────────────────────────────

export interface UFEMetrics {
  totalEvals: number;
  /** Evaluations that improved score OR explored a genuinely novel region */
  usefulEvals: number;
  /** useful / total */
  ufeRatio: number;
  /** Score improvement per useful eval */
  convergenceVelocity: number;
  /** Area Under Convergence Curve (normalized, lower = faster convergence) */
  aucc: number;
  /** Evals to reach 10/50/90% of optimum gap closure */
  timeToTarget: { pct10: number | null; pct50: number | null; pct90: number | null };
  /** Full convergence curve: [evalIndex, bestScoreSoFar] */
  convergenceCurve: Array<[number, number]>;
}

// ─── Model Comparison ────────────────────────────────────────────────────────

export interface ModelConfig {
  id: string;
  name: string;
  agentConfig: AgentConfig;
  description?: string;
}

export interface TrialResult {
  modelId: string;
  benchmarkId: string;
  trial: number;
  finalScore: number;
  ufe: UFEMetrics;
  wallTime: number;
  seed: number;
  discoveries: Discovery[];
}

export interface ComparisonConfig {
  models: ModelConfig[];
  benchmarks: string[] | 'all';
  budget: number;
  trials: number;
  rankBy: 'final_score' | 'ufe_ratio' | 'aucc' | 'time_to_target_50';
  optima?: Record<string, number>;
  baseSeed?: number;
  verbosity?: 'silent' | 'minimal' | 'normal' | 'verbose';
}

export interface LeaderboardEntry {
  modelId: string;
  modelName: string;
  meanScore: number;
  meanUFE: number;
  meanAUCC: number;
  wins: number;
  losses: number;
  ties: number;
  elo: number;
  ci95: [number, number];
}

export interface StatisticalTest {
  test: string;
  pValue: number;
  effectSize: number;
  significant: boolean;
  direction: 'a_better' | 'b_better' | 'no_difference';
}

// ─── Events ──────────────────────────────────────────────────────────────────

export type AgentEvent =
  | { type: 'started'; config: AgentConfig }
  | { type: 'evaluation'; result: EvalResult }
  | { type: 'new_best'; result: EvalResult; improvement: number }
  | { type: 'discovery'; discovery: Discovery }
  | { type: 'strategy_switch'; from: StrategyType; to: StrategyType; reason: string }
  | { type: 'phase_change'; from: string; to: string }
  | { type: 'report'; state: AgentState }
  | { type: 'converged'; result: EvalResult; totalEvals: number }
  | { type: 'stopped'; reason: string; state: AgentState };

export type EventHandler = (event: AgentEvent) => void;
