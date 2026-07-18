/**
 * Seeker — Public API
 * Autonomous discovery engine that solves UFE optimization,
 * hunts anomalies, surfaces discoveries, scripts, records, and learns.
 */

export { SeekerAgent, seeker, optimize } from './agent';
export {
  Task, Goal, AgentConfig, AgentState, EvalResult,
  Discovery, AgentEvent, EventHandler, ParameterDef,
  Constraint, StrategyType, Strategy,
  UFEMetrics, ModelConfig, TrialResult, ComparisonConfig,
  LeaderboardEntry, StatisticalTest,
} from './interfaces';
export { SeededRNG } from './rng';
export { UFETracker, AnomalyDetector } from './ufe';
export { MetaLearner } from './strategies';
export { getMessages, formatDuration, LangCode } from './language';
export {
  bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD,
  ELORating, CIResult, TestResult,
} from './statistics';
export { compareModels, ComparisonReport } from './comparison';
export { runBenchmarks, benchmarkFunctions, BenchmarkResult } from './benchmarks';
export { Memory, MemoryEntry, KnowledgeNode, KnowledgeEdge } from './memory';
export { plugins, StrategyPlugin, ReporterPlugin, TransformPlugin, latinHypercubePlugin, differentialEvolutionPlugin } from './plugins';
export { saveCheckpoint, loadCheckpoint, autoSave, warmStartFrom, WarmStartData } from './warm-start';
