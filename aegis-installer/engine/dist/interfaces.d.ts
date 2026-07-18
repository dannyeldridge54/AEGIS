/**
 * AEGIS — Autonomous Evolving General Intelligence System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Core interfaces for the AEGIS agent framework.
 */
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
export type StrategyType = 'grid' | 'random' | 'bayesian' | 'evolutionary' | 'gradient' | 'swarm' | 'annealing' | 'bandit' | 'curiosity' | 'exploit';
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
    persistence?: {
        enabled: boolean;
        path?: string;
        interval?: number;
    };
    /** Language for output ('en' | 'es' | 'fr' | 'de' | 'ja' | 'zh' | 'pt' | 'ko') */
    language?: string;
    /** RNG seed for reproducible runs (0 = random seed) */
    seed?: number;
    /** Resolution for novelty grid (UFE tracking) */
    noveltyResolution?: number;
}
export interface UFEMetrics {
    /** Total function evaluations performed */
    totalEvals: number;
    /** Useful function evaluations (improved score OR explored novel region) */
    usefulEvals: number;
    /** UFE efficiency ratio: useful / total */
    ufeRatio: number;
    /** Improvement per useful evaluation */
    convergenceVelocity: number;
    /** Area Under Convergence Curve (lower = better for minimization) */
    aucc: number;
    /** Evaluations needed to reach [10%, 50%, 90%] of known optimum gap reduction */
    timeToTarget: {
        pct10: number | null;
        pct50: number | null;
        pct90: number | null;
    };
    /** Full convergence curve: (eval_index, best_score_so_far) */
    convergenceCurve: Array<[number, number]>;
}
export interface ModelConfig {
    /** Unique identifier for this model/configuration */
    id: string;
    /** Human-readable name */
    name: string;
    /** Agent configuration to use */
    agentConfig: AgentConfig;
    /** Optional description */
    description?: string;
}
export interface TrialResult {
    /** Which model produced this */
    modelId: string;
    /** Which benchmark function */
    benchmarkId: string;
    /** Trial index (for repeated runs) */
    trial: number;
    /** Final best score */
    finalScore: number;
    /** UFE metrics for this trial */
    ufe: UFEMetrics;
    /** Total wall-clock time in seconds */
    wallTime: number;
    /** RNG seed used */
    seed: number;
}
export interface ComparisonConfig {
    /** Models to compare */
    models: ModelConfig[];
    /** Benchmark function IDs (or 'all') */
    benchmarks: string[] | 'all';
    /** Fixed evaluation budget per trial */
    budget: number;
    /** Number of repeated trials per model×benchmark */
    trials: number;
    /** Primary metric for ranking */
    rankBy: 'final_score' | 'ufe_ratio' | 'aucc' | 'time_to_target_50';
    /** Known optimum per benchmark (for time-to-target). Auto-filled for built-in benchmarks */
    optima?: Record<string, number>;
    /** Base seed (each trial uses baseSeed + trialIndex) */
    baseSeed?: number;
    /** Verbosity */
    verbosity?: 'silent' | 'minimal' | 'normal' | 'verbose';
}
export interface LeaderboardEntry {
    modelId: string;
    modelName: string;
    /** Mean final score across all trials and benchmarks */
    meanScore: number;
    /** Mean UFE ratio */
    meanUFE: number;
    /** Mean AUCC */
    meanAUCC: number;
    /** Win count (statistically significantly better in pairwise comparisons) */
    wins: number;
    /** Loss count */
    losses: number;
    /** Tie count */
    ties: number;
    /** ELO rating */
    elo: number;
    /** 95% confidence interval on mean score [low, high] */
    ci95: [number, number];
}
export interface StatisticalTest {
    /** Test name (e.g. 'Mann-Whitney U', 'Wilcoxon') */
    test: string;
    /** p-value */
    pValue: number;
    /** Effect size (Cohen's d) */
    effectSize: number;
    /** Whether the difference is statistically significant at α=0.05 */
    significant: boolean;
    /** Direction: 'a_better' | 'b_better' | 'no_difference' */
    direction: 'a_better' | 'b_better' | 'no_difference';
}
export type AgentEvent = {
    type: 'started';
    config: AgentConfig;
} | {
    type: 'evaluation';
    result: EvalResult;
} | {
    type: 'new_best';
    result: EvalResult;
    improvement: number;
} | {
    type: 'discovery';
    discovery: Discovery;
} | {
    type: 'strategy_switch';
    from: StrategyType;
    to: StrategyType;
    reason: string;
} | {
    type: 'phase_change';
    from: string;
    to: string;
} | {
    type: 'report';
    state: AgentState;
} | {
    type: 'converged';
    result: EvalResult;
    totalEvals: number;
} | {
    type: 'stopped';
    reason: string;
    state: AgentState;
};
export type EventHandler = (event: AgentEvent) => void;
//# sourceMappingURL=interfaces.d.ts.map