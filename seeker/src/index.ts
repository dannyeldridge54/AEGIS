/**
 * Seeker — Public API
 * Autonomous discovery engine that solves UFE optimization,
 * hunts anomalies, surfaces discoveries, scripts, records, and learns.
 */

// Core
export { SeekerAgent, seeker, optimize } from './agent';
export {
  Task, Goal, AgentConfig, AgentState, EvalResult,
  Discovery, AgentEvent, EventHandler, ParameterDef,
  Constraint, StrategyType, Strategy,
  UFEMetrics, ModelConfig, TrialResult, ComparisonConfig,
  LeaderboardEntry, StatisticalTest,
} from './interfaces';

// Seeded RNG
export { SeededRNG } from './rng';

// UFE + Anomaly Detection
export { UFETracker, AnomalyDetector } from './ufe';

// Strategies
export { MetaLearner } from './strategies';

// Language
export { getMessages, formatDuration, LangCode } from './language';

// Statistical Engine
export {
  bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD,
  ELORating, CIResult, TestResult,
} from './statistics';

// Model Comparison
export { compareModels, ComparisonReport } from './comparison';

// Benchmarks
export { runBenchmarks, benchmarkFunctions, BenchmarkResult } from './benchmarks';

// Parallel
export { parallelOptimize, ParallelConfig } from './parallel';

// Multi-Objective
export { multiOptimize, MultiObjective, ParetoResult, ParetoFront } from './multi-objective';

// Swarm
export { Swarm, SwarmAgent, AgentMessage } from './swarm';

// Self-Evolution
export { SelfEvolver, EvolutionConfig } from './self-evolve';

// Daemon
export { SeekerDaemon, DaemonConfig, DaemonJob, startDaemon } from './daemon';

// Data Recorder
export { DataRecorder, createRecorder, RecorderConfig } from './recorder';

// Memory
export { Memory, MemoryEntry, KnowledgeNode, KnowledgeEdge } from './memory';

// Plugins
export { plugins, StrategyPlugin, ReporterPlugin, TransformPlugin, latinHypercubePlugin, differentialEvolutionPlugin } from './plugins';

// Warm Start
export { saveCheckpoint, loadCheckpoint, autoSave, warmStartFrom, WarmStartData } from './warm-start';
