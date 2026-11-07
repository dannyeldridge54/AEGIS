// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 951561ff45ec710d
/**
 * AEGIS — Core Agent
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * The main autonomous agent that self-learns, adapts strategies,
 * and optimizes any objective with zero configuration.
 */

import {
  Task, Goal, AgentConfig, AgentState, EvalResult,
  Discovery, AgentEvent, EventHandler, StrategyType,
} from './interfaces';
import { MetaLearner, generateNextPoint, observeResult } from './strategies';
import { getMessages, formatDuration } from './language';
import { writeFileAtomic } from './fs-util';

/** Strategies that search around the current best (their step size is adapted). */
const LOCAL_STRATEGIES = new Set<StrategyType>(['gradient', 'exploit', 'annealing', 'evolutionary']);

// ─── Default Configuration ───────────────────────────────────────────────────

const DEFAULT_CONFIG: Required<AgentConfig> = {
  goal: 'minimize',
  reportInterval: 10,
  maxEvals: 0,
  convergenceThreshold: 1e-8,
  explorationRate: 0.3,
  strategies: ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit', 'swarm', 'bayesian', 'bandit'],
  verbosity: 'normal',
  persistence: { enabled: false, path: './aegis-state.json', interval: 60 },
  language: 'en',
  restartAfter: -1,
};

// ─── AEGIS Agent ─────────────────────────────────────────────────────────────

export class AegisAgent {
  private task: Task;
  private config: Required<AgentConfig>;
  private state: AgentState;
  private metaLearner: MetaLearner;
  private handlers: EventHandler[] = [];
  private running = false;
  private startTime = 0;
  private lastReportTime = 0;
  private lastBestTime = 0;
  private gridIndex = 0;
  private msg;
  // Local search state (reset on restart); the global best lives in state.best
  private localBest: EvalResult | null = null;
  private localHistory: EvalResult[] = [];
  private sinceLocalImprovement = 0;
  private sinceGlobalImprovement = 0;
  private restarts = 0;
  private finalPhase = false;
  /** Step-size multiplier for local strategies, adapted by the 1/5th success rule */
  private stepScale = 1;

  constructor(task: Task, config?: AgentConfig) {
    this.task = task;
    this.config = { ...DEFAULT_CONFIG, ...config } as Required<AgentConfig>;
    this.msg = getMessages(this.config.language);

    this.metaLearner = new MetaLearner(
      this.config.strategies,
      this.config.explorationRate
    );

    this.state = {
      best: null,
      totalEvals: 0,
      history: [],
      strategies: this.metaLearner.getStrategies(),
      discoveries: [],
      runtime: 0,
      phase: 'exploring',
    };
  }

  // ─── Public API ──────────────────────────────────────────────────────────

  /** Subscribe to agent events */
  on(handler: EventHandler): this {
    this.handlers.push(handler);
    return this;
  }

  /** Run the agent (async, runs until convergence or maxEvals) */
  async run(): Promise<AgentState> {
    this.running = true;
    this.startTime = Date.now();
    this.lastReportTime = this.startTime;
    this.lastBestTime = this.startTime;

    this.emit({ type: 'started', config: this.config });
    this.log(this.msg.started);
    this.log(`  Task: ${this.task.name} (${this.task.parameters.length} params)`);

    let lastYield = Date.now();
    while (this.running) {
      await this.step();

      // Yield to the event loop every ~16 ms. Without this a synchronous objective
      // starves timers, HTTP servers (daemon API, dashboard) and stop() calls, and
      // "parallel" swarm agents run strictly one after another.
      if (Date.now() - lastYield >= 16) {
        await new Promise<void>(resolve => setImmediate(resolve));
        lastYield = Date.now();
        if (!this.running) break;
      }

      // Check stopping conditions
      if (this.config.maxEvals > 0 && this.state.totalEvals >= this.config.maxEvals) {
        this.stop('Max evaluations reached');
        break;
      }

      if (this.checkConvergence()) {
        this.emit({ type: 'converged', result: this.state.best!, totalEvals: this.state.totalEvals });
        this.log(`${this.msg.converged} ${this.state.totalEvals} ${this.msg.evalCount}, ${this.msg.bestScore}: ${this.state.best!.score.toFixed(6)}`);
        this.running = false;
        break;
      }

      // Periodic report
      const now = Date.now();
      if (this.config.reportInterval > 0 && (now - this.lastReportTime) / 1000 >= this.config.reportInterval) {
        this.report();
        this.lastReportTime = now;
      }
    }

    // Final state
    this.state.runtime = (Date.now() - this.startTime) / 1000;
    this.state.strategies = this.metaLearner.getStrategies();

    if (this.config.persistence.enabled) {
      this.saveState();
    }

    return this.state;
  }

  /** Run a single step */
  async step(): Promise<EvalResult> {
    // Final phase: spend the last quarter of a fixed budget polishing the global best
    if (!this.finalPhase && this.config.maxEvals > 0 && this.state.totalEvals >= 0.75 * this.config.maxEvals
        && this.state.best && Number.isFinite(this.state.best.score)) {
      this.finalPhase = true;
      if (this.localBest !== this.state.best) {
        this.localBest = this.state.best;
        this.localHistory = this.state.history.slice(-1000);
        this.sinceLocalImprovement = 0;
        this.stepScale = Math.min(this.stepScale, 0.5);
      }
    }
    const strategy = this.metaLearner.selectStrategy();
    // Local strategies work around the current basin (since the last restart);
    // curiosity looks at everything ever sampled so restarts go somewhere new.
    const params = generateNextPoint(
      strategy,
      this.task.parameters,
      this.localBest,
      strategy.type === 'curiosity' || strategy.type === 'bandit' ? this.state.history : this.localHistory,
      this.task.constraints,
      this.gridIndex++,
      this.isMinimizing(),
      this.stepScale
    );

    const raw = await this.task.evaluate(params);
    const minimize = this.isMinimizing();
    // A NaN/Infinity score must never become the best (NaN compares false with everything,
    // which would freeze the search). Record it as the worst possible value instead.
    const score = Number.isFinite(raw) ? raw : (minimize ? Infinity : -Infinity);
    const result: EvalResult = {
      params,
      score,
      timestamp: Date.now(),
      strategy: strategy.type,
    };

    observeResult(strategy, params, score, minimize);

    this.state.totalEvals++;
    this.state.history.push(result);
    if (this.state.history.length > 5000) {
      this.state.history = this.state.history.slice(-2500);
    }

    this.localHistory.push(result);
    if (this.localHistory.length > 2500) this.localHistory = this.localHistory.slice(-1250);

    // Local improvement drives strategy rewards and restarts
    const prevLocal = this.localBest?.score ?? (minimize ? Infinity : -Infinity);
    const localBetter = Number.isFinite(score) && (minimize ? score < prevLocal : score > prevLocal);
    const localGain = localBetter && Number.isFinite(prevLocal)
      ? Math.min(Math.max(Math.abs(prevLocal - score) / (Math.abs(prevLocal) + 1e-12), 0.01), 1)
      : (localBetter ? 1 : 0);
    if (localBetter) {
      this.localBest = result;
      this.sinceLocalImprovement = 0;
    } else {
      this.sinceLocalImprovement++;
    }
    // 1/5th success rule: success ×1.5, failure ×1.5^(-1/4) → steps settle where ~20% succeed
    if (LOCAL_STRATEGIES.has(strategy.type)) {
      this.stepScale = localBetter
        ? Math.min(4, this.stepScale * 1.5)
        : Math.max(1e-6, this.stepScale * 0.9036);
    }
    this.metaLearner.updateStrategy(strategy.type, localGain);

    // Track improvement (supports both minimize and maximize goals)
    const previousBest = this.state.best?.score ?? (minimize ? Infinity : -Infinity);
    const isBetter = minimize ? score < previousBest : score > previousBest;
    const improvement = minimize ? (previousBest - score) : (score - previousBest);

    if (Number.isFinite(score) && (!this.state.best || !Number.isFinite(this.state.best.score) || isBetter)) {
      this.state.best = result;
      this.lastBestTime = Date.now();
      if (!Number.isFinite(previousBest) || improvement > this.config.convergenceThreshold) {
        this.sinceGlobalImprovement = 0;
      } else {
        this.sinceGlobalImprovement++;
      }

      this.emit({ type: 'new_best', result, improvement: Math.max(improvement, 0) });

      if (this.config.verbosity !== 'silent') {
        this.log(`${this.msg.newBest} score=${score.toFixed(6)} (${this.msg.improvement}: ${improvement.toFixed(6)}) [${strategy.type}]`);
      }

      // Log discovery (only after initial baseline)
      if (Number.isFinite(previousBest) && Math.abs(improvement) > Math.abs(previousBest) * 0.05) {
        const discovery: Discovery = {
          type: 'new_best',
          description: `Major improvement: ${previousBest.toFixed(4)} → ${score.toFixed(4)} via ${strategy.type}`,
          result,
          confidence: Math.min(Math.abs(improvement) / (Math.abs(previousBest) || 1), 1),
          timestamp: Date.now(),
        };
        this.state.discoveries.push(discovery);
        this.emit({ type: 'discovery', discovery });
      }
    } else {
      if (!this.state.best) this.state.best = result; // keep a placeholder until a finite score arrives
      this.sinceGlobalImprovement++;
    }

    // Restart the local search when it has stalled (global best is kept)
    const restartAfter = this.restartWindow();
    // Stalled = no local improvement for a window, or the adapted step has collapsed
    // (the basin is solved to ~1e-4 of the range; further polishing is the final phase's job)
    const stalled = this.sinceLocalImprovement >= restartAfter || this.stepScale < 1e-2;
    if (restartAfter > 0 && !this.finalPhase && this.localBest && stalled) {
      this.restarts++;
      const discovery: Discovery = {
        type: 'restart',
        description: `Restart #${this.restarts}: local search converged at ${this.localBest.score.toFixed(6)}`,
        result: this.localBest,
        confidence: 1,
        timestamp: Date.now(),
      };
      this.state.discoveries.push(discovery);
      this.emit({ type: 'discovery', discovery });
      this.localBest = null;
      this.localHistory = [];
      this.sinceLocalImprovement = 0;
      this.stepScale = 1;
    }

    // Phase management
    this.updatePhase();

    this.emit({ type: 'evaluation', result });
    return result;
  }

  /** Stop the agent */
  stop(reason: string = 'User requested'): void {
    this.running = false;
    this.state.runtime = (Date.now() - this.startTime) / 1000;
    this.emit({ type: 'stopped', reason, state: this.state });
    this.log(`${this.msg.stopped} ${reason}`);
  }

  /** Get current state */
  getState(): AgentState {
    const runtime = this.startTime ? (Date.now() - this.startTime) / 1000 : 0;
    return { ...this.state, runtime };
  }

  /** Change language at runtime */
  setLanguage(lang: string): void {
    (this.config as any).language = lang;
    this.msg = getMessages(lang);
  }

  // ─── Internal ────────────────────────────────────────────────────────────

  /** Determine if we're minimizing based on goal config */
  private isMinimizing(): boolean {
    const goal = this.config.goal;
    if (!goal) return true;
    if (typeof goal === 'string') {
      return !/(maximize|maximise|highest|largest|most|best score)/i.test(goal);
    }
    return goal.minimize !== false;
  }

  private updatePhase(): void {
    const timeSinceBest = (Date.now() - this.lastBestTime) / 1000;
    const oldPhase = this.state.phase;

    if (this.state.totalEvals < 100) {
      this.state.phase = 'exploring';
    } else if (timeSinceBest > 30) {
      this.state.phase = 'curious';
      this.config.explorationRate = Math.min(0.8, this.config.explorationRate + 0.01);
    } else if (timeSinceBest < 5) {
      this.state.phase = 'exploiting';
      this.config.explorationRate = Math.max(0.1, this.config.explorationRate - 0.01);
    }

    if (oldPhase !== this.state.phase) {
      this.emit({ type: 'phase_change', from: oldPhase, to: this.state.phase });
      if (this.config.verbosity === 'verbose') {
        this.log(`${this.msg.phaseChange} ${oldPhase} → ${this.state.phase}`);
      }
    }
  }

  /** Evaluations without local improvement before a restart (0 = never). */
  private restartWindow(): number {
    const r = this.config.restartAfter;
    if (r === 0) return 0;
    if (r > 0) return r;
    return Math.max(150, 50 * this.task.parameters.length);
  }

  /** Number of local-search restarts so far. */
  getRestarts(): number { return this.restarts; }

  private checkConvergence(): boolean {
    if (this.state.totalEvals < 200) return false;
    if (!this.state.best || !Number.isFinite(this.state.best.score)) return false;
    // Converged when the global best has not improved (by more than the threshold) for
    // a whole window. With restarts on, the window spans several restarts first.
    const restart = this.restartWindow();
    const window = restart > 0 ? Math.max(1000, 4 * restart) : 500;
    return this.sinceGlobalImprovement >= window;
  }

  private report(): void {
    const elapsed = formatDuration((Date.now() - this.startTime) / 1000);
    const best = this.state.best?.score.toFixed(6) ?? 'N/A';
    const strategies = this.metaLearner.getStrategies();
    const topStrategy = strategies[0];

    this.log(`${this.msg.progress} ${this.state.totalEvals} ${this.msg.evalCount} | ${this.msg.bestScore}: ${best} | ${this.msg.timeElapsed}: ${elapsed} | Top: ${topStrategy.type}`);
    this.emit({ type: 'report', state: this.getState() });
  }

  private saveState(): void {
    const statePath = this.config.persistence.path || './aegis-state.json';
    writeFileAtomic(statePath, JSON.stringify(this.getState(), null, 2));
  }

  private emit(event: AgentEvent): void {
    for (const handler of this.handlers) {
      try { handler(event); } catch { /* ignore handler errors */ }
    }
  }

  private log(msg: string): void {
    if (this.config.verbosity === 'silent') return;
    console.log(msg);
  }
}

// ─── Quick-Start Factory ─────────────────────────────────────────────────────

/**
 * Create an AEGIS agent with minimal setup.
 *
 * @example
 * const agent = aegis({
 *   name: 'tune-model',
 *   evaluate: (p) => myModel.loss(p.lr, p.dropout),
 *   parameters: [
 *     { name: 'lr', min: 0.0001, max: 0.1 },
 *     { name: 'dropout', min: 0, max: 0.5 },
 *   ],
 * });
 * const result = await agent.run();
 */
export function aegis(task: Task, config?: AgentConfig): AegisAgent {
  return new AegisAgent(task, config);
}

/**
 * One-liner: run AEGIS and return the best result.
 *
 * @example
 * const best = await optimize(
 *   (p) => (p.x - 3)**2 + (p.y + 1)**2,
 *   [{ name: 'x', min: -10, max: 10 }, { name: 'y', min: -10, max: 10 }]
 * );
 * console.log(best.params); // { x: ~3, y: ~-1 }
 */
export async function optimize(
  fn: (params: Record<string, number>) => number | Promise<number>,
  parameters: Array<{ name: string; min: number; max: number; description?: string }>,
  config?: AgentConfig
): Promise<EvalResult> {
  const agent = new AegisAgent({
    id: 'quick-optimize',
    name: 'Quick Optimization',
    evaluate: fn,
    parameters,
  }, { maxEvals: config?.maxEvals || 5000, verbosity: 'minimal', ...config });

  const state = await agent.run();
  return state.best!;
}
