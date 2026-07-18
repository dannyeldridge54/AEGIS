/**
 * Seeker — Public API
 * Autonomous discovery engine that solves UFE optimization,
 * hunts anomalies, surfaces discoveries, scripts, records, and learns.
 */
export { SeekerAgent, seeker, optimize } from './agent';
export { Task, Goal, AgentConfig, AgentState, EvalResult, Discovery, AgentEvent, EventHandler, ParameterDef, Constraint, StrategyType, Strategy, UFEMetrics, ModelConfig, TrialResult, ComparisonConfig, LeaderboardEntry, StatisticalTest, } from './interfaces';
export { SeededRNG } from './rng';
export { UFETracker, AnomalyDetector } from './ufe';
export { MetaLearner } from './strategies';
export { getMessages, formatDuration, LangCode } from './language';
export { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating, CIResult, TestResult, } from './statistics';
export { compareModels, ComparisonReport } from './comparison';
export { runBenchmarks, benchmarkFunctions, BenchmarkResult } from './benchmarks';
export { parallelOptimize, ParallelConfig } from './parallel';
export { multiOptimize, MultiObjective, ParetoResult, ParetoFront } from './multi-objective';
export { Swarm, SwarmAgent, AgentMessage } from './swarm';
export { SelfEvolver, EvolutionConfig } from './self-evolve';
export { SeekerDaemon, DaemonConfig, DaemonJob, startDaemon } from './daemon';
export { DataRecorder, createRecorder, RecorderConfig } from './recorder';
export { Memory, MemoryEntry, KnowledgeNode, KnowledgeEdge } from './memory';
export { plugins, StrategyPlugin, ReporterPlugin, TransformPlugin, latinHypercubePlugin, differentialEvolutionPlugin } from './plugins';
export { saveCheckpoint, loadCheckpoint, autoSave, warmStartFrom, WarmStartData } from './warm-start';
export { LiveMonitor, createMonitor, Alert, AlertSeverity, MonitorConfig, MonitorSnapshot, RunTracker } from './monitor';
export { torsionTasks, einsteinCartanTask, fTGravityTask, ufeTorsionTask, torsionWaveTask, crossDomainTask, crossDomainUFE, einsteinCartanResidual, fTCosmologyResidual, ufeTorsionFunctional, torsionWaveResidual, fTGravity_PowerLaw, fTGravity_BornInfeld, fTGravity_Logarithmic, fTGravity_Exponential, computeTorsionScalar, computeTraceVector, computeAxialTorsion, computeSpatialAnomalies, HZ_OBSERVATIONS, TorsionTensor, ContorsionTensor, HzObservation, SpatialAnomaly, } from './torsion';
export { EquationWriter, createEquationWriter } from './equation-writer';
//# sourceMappingURL=index.d.ts.map