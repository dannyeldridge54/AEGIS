/**
 * AEGIS — Public API
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 */

export { AegisAgent, aegis, optimize } from './agent';
export {
  Task, Goal, AgentConfig, AgentState, EvalResult,
  Discovery, AgentEvent, EventHandler, ParameterDef,
  Constraint, StrategyType, Strategy,
} from './interfaces';
export { MetaLearner } from './strategies';
export { getMessages, formatDuration, LangCode } from './language';
export { multiOptimize, MultiObjective, ParetoResult, ParetoFront } from './multi-objective';
export { parallelOptimize, ParallelConfig } from './parallel';
export { plugins, StrategyPlugin, ReporterPlugin, TransformPlugin, latinHypercubePlugin, differentialEvolutionPlugin } from './plugins';
export { SelfEvolver, EvolutionConfig } from './self-evolve';
export { createDashboard, dashboardHandler, DashboardServer } from './dashboard';
export { saveCheckpoint, loadCheckpoint, autoSave, warmStartFrom, WarmStartData } from './warm-start';
export { CodingAgent, createCoder, Sandbox, OpenAIProvider, OllamaProvider, LLMProvider, CodingTask, CodingResult, ExecutionResult } from './coding-agent';
export { physics, finance, environment, engineering, math, live } from './real-data';
