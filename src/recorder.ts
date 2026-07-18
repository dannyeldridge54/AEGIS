/**
 * AEGIS — Data Recorder
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Scripts every evaluation to disk. CSV + JSON logs.
 * Export convergence curves, discovery logs, strategy stats.
 * The black box flight recorder for optimization runs.
 */

import * as fs from 'fs';
import * as path from 'path';
import { EvalResult, Discovery, AgentState, UFEMetrics, AgentEvent, Strategy } from './interfaces';

export interface RecorderConfig {
  dir: string;
  runId: string;
  logEvals?: boolean;
  logDiscoveries?: boolean;
  logStrategies?: boolean;
  flushInterval?: number;
}

export class DataRecorder {
  private config: Required<RecorderConfig>;
  private evalCount = 0;
  private csvStream: fs.WriteStream | null = null;
  private discoveryStream: fs.WriteStream | null = null;
  private paramNames: string[] = [];
  private initialized = false;

  constructor(config: RecorderConfig) {
    this.config = {
      dir: config.dir,
      runId: config.runId,
      logEvals: config.logEvals !== false,
      logDiscoveries: config.logDiscoveries !== false,
      logStrategies: config.logStrategies !== false,
      flushInterval: config.flushInterval || 100,
    };

    if (!fs.existsSync(this.config.dir)) {
      fs.mkdirSync(this.config.dir, { recursive: true });
    }
  }

  init(paramNames: string[]): void {
    this.paramNames = paramNames;
    this.initialized = true;

    if (this.config.logEvals) {
      const csvPath = path.join(this.config.dir, `${this.config.runId}-evals.csv`);
      this.csvStream = fs.createWriteStream(csvPath, { flags: 'w' });
      const header = ['eval_num', 'score', 'strategy', 'timestamp', 'useful', ...paramNames].join(',');
      this.csvStream.write(header + '\n');
    }

    if (this.config.logDiscoveries) {
      const discPath = path.join(this.config.dir, `${this.config.runId}-discoveries.jsonl`);
      this.discoveryStream = fs.createWriteStream(discPath, { flags: 'w' });
    }
  }

  recordEval(result: EvalResult, useful: boolean): void {
    this.evalCount++;
    if (!this.initialized || !this.csvStream) return;

    const paramValues = this.paramNames.map(n => result.params[n]?.toFixed(8) || '0');
    const line = [
      this.evalCount, result.score.toFixed(10), result.strategy,
      result.timestamp, useful ? 1 : 0, ...paramValues,
    ].join(',');
    this.csvStream.write(line + '\n');
  }

  recordDiscovery(discovery: Discovery): void {
    if (!this.discoveryStream) return;
    this.discoveryStream.write(JSON.stringify({
      eval: this.evalCount, type: discovery.type,
      description: discovery.description, confidence: discovery.confidence,
      score: discovery.result.score, timestamp: discovery.timestamp,
    }) + '\n');
  }

  recordStrategies(strategies: Strategy[]): void {
    if (!this.config.logStrategies) return;
    const stratPath = path.join(this.config.dir, `${this.config.runId}-strategies.json`);
    const data = strategies.map(s => ({
      type: s.type, uses: s.uses, score: s.score, avgImprovement: s.avgImprovement,
    }));
    fs.writeFileSync(stratPath, JSON.stringify(data, null, 2));
  }

  writeSummary(state: AgentState): void {
    const summaryPath = path.join(this.config.dir, `${this.config.runId}-summary.json`);
    fs.writeFileSync(summaryPath, JSON.stringify({
      runId: this.config.runId, totalEvals: state.totalEvals,
      bestScore: state.best?.score, bestParams: state.best?.params,
      bestStrategy: state.best?.strategy, runtime: state.runtime,
      phase: state.phase, discoveries: state.discoveries.length,
      ufe: state.ufe,
      strategies: state.strategies.map(s => ({
        type: s.type, uses: s.uses, score: s.score, avgImprovement: s.avgImprovement,
      })),
    }, null, 2));
  }

  exportConvergenceCurve(ufe: UFEMetrics): void {
    const curvePath = path.join(this.config.dir, `${this.config.runId}-convergence.csv`);
    const lines = ['eval,best_score'];
    for (const [evalIdx, score] of ufe.convergenceCurve) {
      lines.push(`${evalIdx},${score.toFixed(10)}`);
    }
    fs.writeFileSync(curvePath, lines.join('\n'));
  }

  createHandler(): (event: AgentEvent) => void {
    return (event: AgentEvent) => {
      if (event.type === 'discovery') this.recordDiscovery(event.discovery);
      if (event.type === 'report') this.recordStrategies(event.state.strategies);
      if (event.type === 'stopped' || event.type === 'converged') {
        const state = (event as any).state || event;
        if (state.strategies) this.recordStrategies(state.strategies);
      }
    };
  }

  close(): void {
    this.csvStream?.end();
    this.discoveryStream?.end();
  }
}

export function createRecorder(runId: string, dir: string = './aegis-data'): DataRecorder {
  return new DataRecorder({ runId, dir });
}
