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
