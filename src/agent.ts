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
import { MetaLearner, generateNextPoint } from './strategies';
import { getMessages, formatDuration } from './language';
import * as fs from 'fs';
import * as path from 'path';

// ─── Default Configuration ───────────────────────────────────────────────────

const DEFAULT_CONFIG: Required<AgentConfig> = {
  goal: 'minimize',
  reportInterval: 10,
  maxEvals: 0,
  convergenceThreshold: 1e-8,
  explorationRate: 0.3,
  strategies: ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'],
  verbosity: 'normal',
  persistence: { enabled: false, path: './aegis-state.json', interval: 60 },
  language: 'en',
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

    while (this.running) {
      await this.step();

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
    const strategy = this.metaLearner.selectStrategy();
    const params = generateNextPoint(
      strategy,
      this.task.parameters,
      this.state.best,
      this.state.history,
      this.task.constraints,
      this.gridIndex++
    );

    const score = await this.task.evaluate(params);
    const result: EvalResult = {
      params,
      score,
      timestamp: Date.now(),
      strategy: strategy.type,
    };

    this.state.totalEvals++;
    this.state.history.push(result);
    if (this.state.history.length > 5000) {
      this.state.history = this.state.history.slice(-2500);
    }

    // Track improvement
    const previousBest = this.state.best?.score ?? Infinity;
    const improvement = previousBest - score;

    if (!this.state.best || score < previousBest) {
      this.state.best = result;
      this.lastBestTime = Date.now();
      this.metaLearner.updateStrategy(strategy.type, Math.max(improvement, 0.001));

      this.emit({ type: 'new_best', result, improvement });

      if (this.config.verbosity !== 'silent') {
        this.log(`${this.msg.newBest} score=${score.toFixed(6)} (${this.msg.improvement}: ${improvement.toFixed(6)}) [${strategy.type}]`);
      }

      // Log discovery
      if (improvement > previousBest * 0.05) {
        const discovery: Discovery = {
          type: 'new_best',
          description: `Major improvement: ${previousBest.toFixed(4)} → ${score.toFixed(4)} via ${strategy.type}`,
          result,
          confidence: Math.min(improvement / previousBest, 1),
          timestamp: Date.now(),
        };
        this.state.discoveries.push(discovery);
        this.emit({ type: 'discovery', discovery });
      }
    } else {
      this.metaLearner.updateStrategy(strategy.type, Math.max(improvement, 0));
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
    return { ...this.state, runtime: (Date.now() - this.startTime) / 1000 };
  }

  /** Change language at runtime */
  setLanguage(lang: string): void {
    (this.config as any).language = lang;
    this.msg = getMessages(lang);
  }

  // ─── Internal ────────────────────────────────────────────────────────────

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

  private checkConvergence(): boolean {
    if (this.state.totalEvals < 200) return false;
    if (!this.state.best) return false;

    // No improvement in last 500 evals
    const recentWindow = this.state.history.slice(-500);
    if (recentWindow.length < 500) return false;

    const recentBest = Math.min(...recentWindow.map(r => r.score));
    const olderBest = Math.min(...this.state.history.slice(-1000, -500).map(r => r.score));

    return Math.abs(recentBest - olderBest) < this.config.convergenceThreshold;
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
    const dir = path.dirname(statePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(statePath, JSON.stringify(this.getState(), null, 2));
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
