/**
 * AEGIS — Autonomous Evolving General Intelligence System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Core interfaces for the AEGIS agent framework.
 */

// ─── Natural Language Goal Definition ────────────────────────────────────────

export interface Goal {
  /** Plain English description of what to achieve */
  description: string;
  /** How to measure success (agent infers if not provided) */
  metric?: string;
  /** Target value for the metric (lower = better by default) */
  target?: number;
  /** Whether lower is better (true) or higher is better (false) */
  minimize?: boolean;
  /** Maximum time budget in seconds (0 = unlimited) */
  timeBudget?: number;
  /** Priority level 1-10 (10 = highest) */
  priority?: number;
}

// ─── Task Interface (what AEGIS operates on) ─────────────────────────────────

export interface Task {
  /** Unique task identifier */
  id: string;
  /** Human-readable name */
  name: string;
  /** The function to optimize/explore */
  evaluate: (params: Record<string, number>) => number | Promise<number>;
  /** Parameter space definition */
  parameters: ParameterDef[];
  /** Optional constraints */
  constraints?: Constraint[];
  /** Metadata */
  meta?: Record<string, any>;
}

export interface ParameterDef {
  name: string;
  min: number;
  max: number;
  /** Default starting value */
  default?: number;
  /** Step size hint (for discrete params) */
  step?: number;
  /** Plain English description */
  description?: string;
}

export interface Constraint {
  /** Which parameters this constraint applies to */
  params: string[];
  /** Constraint function — returns true if satisfied */
  check: (values: Record<string, number>) => boolean;
  /** Human description */
  description?: string;
}

// ─── Strategy System ─────────────────────────────────────────────────────────

export type StrategyType =
  | 'grid'           // Systematic grid search
  | 'random'         // Random sampling
  | 'bayesian'       // Bayesian optimization (surrogate model)
  | 'evolutionary'   // Genetic algorithm
  | 'gradient'       // Gradient descent / hill climbing
  | 'swarm'          // Particle swarm optimization
  | 'annealing'      // Simulated annealing
  | 'bandit'         // Multi-armed bandit (strategy selection)
  | 'curiosity'      // Novelty-seeking exploration
  | 'exploit';       // Pure exploitation of known best

export interface Strategy {
  type: StrategyType;
  /** Confidence/performance score (updated by meta-learner) */
  score: number;
  /** Times this strategy has been used */
  uses: number;
  /** Average improvement when this strategy runs */
  avgImprovement: number;
  /** Configuration for this strategy */
  config: Record<string, any>;
}

// ─── Agent State ─────────────────────────────────────────────────────────────

export interface AgentState {
  /** Current best result */
  best: EvalResult | null;
  /** Total evaluations performed */
  totalEvals: number;
  /** Evaluation history (ring buffer) */
  history: EvalResult[];
  /** Strategy performance tracking */
  strategies: Strategy[];
  /** Discoveries log */
  discoveries: Discovery[];
  /** Running time in seconds */
  runtime: number;
  /** Current phase */
  phase: 'exploring' | 'exploiting' | 'curious' | 'converged';
}

export interface EvalResult {
  params: Record<string, number>;
  score: number;
  timestamp: number;
  strategy: StrategyType;
  metadata?: Record<string, any>;
}

export interface Discovery {
  type: 'new_best' | 'anomaly' | 'plateau' | 'convergence' | 'constraint_boundary';
  description: string;
  result: EvalResult;
  confidence: number;
  timestamp: number;
}

// ─── Agent Configuration ─────────────────────────────────────────────────────

export interface AgentConfig {
  /** Natural language goal (parsed into Goal internally) */
  goal?: string | Goal;
  /** How often to report progress (seconds, 0 = silent) */
  reportInterval?: number;
  /** Maximum total evaluations (0 = unlimited) */
  maxEvals?: number;
  /** Convergence threshold (stop when improvement < this) */
  convergenceThreshold?: number;
  /** How aggressively to explore vs exploit (0-1, 0.5 = balanced) */
  explorationRate?: number;
  /** Strategies to use (default: all) */
  strategies?: StrategyType[];
  /** Verbosity: 'silent' | 'minimal' | 'normal' | 'verbose' */
  verbosity?: 'silent' | 'minimal' | 'normal' | 'verbose';
  /** Auto-save state to disk */
  persistence?: { enabled: boolean; path?: string; interval?: number };
  /** Language for output ('en' | 'es' | 'fr' | 'de' | 'ja' | 'zh' | 'pt' | 'ko') */
  language?: string;
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
