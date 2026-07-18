/**
 * AEGIS — Public API
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 */

export { AegisAgent, aegis, optimize } from './agent';
export {
  Task, Goal, AgentConfig, AgentState, EvalResult,
  Discovery, AgentEvent, EventHandler, ParameterDef,
  Constraint, StrategyType, Strategy, UFEMetrics,
  ModelConfig, TrialResult, ComparisonConfig, LeaderboardEntry, StatisticalTest,
} from './interfaces';
export { MetaLearner } from './strategies';
export { SeededRNG } from './rng';
export { UFETracker, AnomalyDetector } from './ufe';
export { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating } from './statistics';
export { compareModels, ComparisonReport } from './comparison';
export { DataRecorder, createRecorder, RecorderConfig } from './recorder';
export { getMessages, formatDuration, LangCode } from './language';
export { multiOptimize, MultiObjective, ParetoResult, ParetoFront } from './multi-objective';
export { parallelOptimize, ParallelConfig } from './parallel';
export { plugins, StrategyPlugin, ReporterPlugin, TransformPlugin, latinHypercubePlugin, differentialEvolutionPlugin } from './plugins';
export { SelfEvolver, EvolutionConfig } from './self-evolve';
export { createDashboard, dashboardHandler, DashboardServer } from './dashboard';
export { saveCheckpoint, loadCheckpoint, autoSave, warmStartFrom, WarmStartData } from './warm-start';
export { CodingAgent, createCoder, Sandbox, OpenAIProvider, OllamaProvider, LLMProvider, CodingTask, CodingResult, ExecutionResult } from './coding-agent';
export { physics, finance, environment, engineering, math, live } from './real-data';
export { Memory, MemoryEntry, KnowledgeNode, KnowledgeEdge } from './memory';
export { Swarm, SwarmAgent, AgentMessage } from './swarm';
export { parseNaturalLanguage, runNatural } from './natural-cli';
export { generateDocs, writeDocs, DocConfig } from './auto-docs';
export { runBenchmarks, benchmarkFunctions, BenchmarkResult } from './benchmarks';
export { AegisDaemon, DaemonConfig, DaemonJob, startDaemon } from './daemon';
export { LiveMonitor, createMonitor, Alert, AlertSeverity, MonitorConfig, MonitorSnapshot, RunTracker } from './monitor';
export {
  torsionTasks, einsteinCartanTask, fTGravityTask, ufeTorsionTask, torsionWaveTask,
  crossDomainTask, crossDomainUFE,
  einsteinCartanResidual, fTCosmologyResidual, ufeTorsionFunctional, torsionWaveResidual,
  fTGravity_PowerLaw, fTGravity_BornInfeld, fTGravity_Logarithmic, fTGravity_Exponential,
  computeTorsionScalar, computeTraceVector, computeAxialTorsion,
  computeSpatialAnomalies, HZ_OBSERVATIONS,
  TorsionTensor, ContorsionTensor, HzObservation, SpatialAnomaly,
} from './torsion';
export { EquationWriter, createEquationWriter } from './equation-writer';
