/**
 * AEGIS — Live Monitor & Alert System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Real-time tracking of optimization runs with categorized alerts:
 *  • Breakthroughs — major score improvements
 *  • Anomalies — z-score outliers, landscape shifts
 *  • Insights — strategy effectiveness, phase transitions, convergence patterns
 *  • Plateaus — stagnation detection with suggested actions
 *
 * Serves a live HTTP dashboard + emits structured JSON events.
 */

import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path';
import { AgentState, EvalResult, Discovery, AgentEvent, UFEMetrics, Strategy } from './interfaces';

// ─── Alert Types ─────────────────────────────────────────────────────────────

export type AlertSeverity = 'info' | 'warning' | 'critical' | 'breakthrough';

export interface Alert {
  id: string;
  timestamp: number;
  severity: AlertSeverity;
  category: 'breakthrough' | 'anomaly' | 'insight' | 'plateau' | 'milestone' | 'strategy';
  title: string;
  detail: string;
  data?: Record<string, any>;
  acknowledged: boolean;
}

export interface MonitorSnapshot {
  /** Current run status */
  status: 'running' | 'paused' | 'completed' | 'idle';
  /** Uptime in seconds */
  uptime: number;
  /** Active run states (keyed by run/job ID) */
  runs: Record<string, RunTracker>;
  /** All alerts (newest first) */
  alerts: Alert[];
  /** Summary counts */
  summary: {
    totalRuns: number;
    totalEvals: number;
    totalBreakthroughs: number;
    totalAnomalies: number;
    activeAlerts: number;
  };
}

export interface RunTracker {
  id: string;
  name: string;
  startedAt: number;
  status: 'running' | 'completed' | 'failed';
  totalEvals: number;
  bestScore: number | null;
  bestParams: Record<string, number> | null;
  ufe: UFEMetrics | null;
  phase: string;
  improvements: number;
  lastImprovedAt: number;
  scoreHistory: Array<{ eval: number; score: number; timestamp: number }>;
  strategyWins: Record<string, number>;
  discoveryCount: number;
}

export interface MonitorConfig {
  /** HTTP port for the live dashboard (0 = disabled) */
  port?: number;
  /** Max alerts to retain */
  maxAlerts?: number;
  /** Max score history points per run */
  maxScoreHistory?: number;
  /** Breakthrough threshold: improvement must be > this fraction of current best */
  breakthroughThreshold?: number;
  /** Stagnation window: evals without improvement to trigger plateau alert */
  stagnationWindow?: number;
  /** Log file path for alerts */
  alertLogFile?: string;
  /** Webhook URL for critical/breakthrough alerts */
  webhookUrl?: string;
}

// ─── Live Monitor ────────────────────────────────────────────────────────────

export class LiveMonitor {
  private config: Required<MonitorConfig>;
  private runs: Map<string, RunTracker> = new Map();
  private alerts: Alert[] = [];
  private alertCounter = 0;
  private server: http.Server | null = null;
  private startTime = Date.now();
  private alertLogStream: fs.WriteStream | null = null;
  private listeners: Array<(alert: Alert) => void> = [];

  constructor(config?: MonitorConfig) {
    this.config = {
      port: config?.port ?? 5555,
      maxAlerts: config?.maxAlerts ?? 500,
      maxScoreHistory: config?.maxScoreHistory ?? 2000,
      breakthroughThreshold: config?.breakthroughThreshold ?? 0.1,
      stagnationWindow: config?.stagnationWindow ?? 500,
      alertLogFile: config?.alertLogFile ?? '',
      webhookUrl: config?.webhookUrl ?? '',
    };

    if (this.config.alertLogFile) {
      const dir = path.dirname(this.config.alertLogFile);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      this.alertLogStream = fs.createWriteStream(this.config.alertLogFile, { flags: 'a' });
    }
  }

  // ─── Run Registration ────────────────────────────────────────────────────

  /** Register a new optimization run to track */
  registerRun(id: string, name: string): RunTracker {
    const tracker: RunTracker = {
      id, name,
      startedAt: Date.now(),
      status: 'running',
      totalEvals: 0,
      bestScore: null,
      bestParams: null,
      ufe: null,
      phase: 'exploring',
      improvements: 0,
      lastImprovedAt: Date.now(),
      scoreHistory: [],
      strategyWins: {},
      discoveryCount: 0,
    };
    this.runs.set(id, tracker);
    this.addAlert('info', 'milestone', `Run started: ${name}`, `Run "${name}" registered and tracking began.`, { runId: id });
    return tracker;
  }

  /** Create an event handler to plug into agent.on() */
  createHandler(runId: string): (event: AgentEvent) => void {
    return (event: AgentEvent) => {
      const run = this.runs.get(runId);
      if (!run) return;

      switch (event.type) {
        case 'evaluation':
          this.onEvaluation(run, event.result);
          break;
        case 'new_best':
          this.onNewBest(run, event.result, event.improvement);
          break;
        case 'discovery':
          this.onDiscovery(run, event.discovery);
          break;
        case 'phase_change':
          this.onPhaseChange(run, event.from, event.to);
          break;
        case 'report':
          this.onReport(run, event.state);
          break;
        case 'stopped':
          this.onStopped(run, event.reason, event.state);
          break;
        case 'converged':
          this.onConverged(run, event.result, event.totalEvals);
          break;
      }
    };
  }

  // ─── Event Handlers ──────────────────────────────────────────────────────

  private onEvaluation(run: RunTracker, result: EvalResult): void {
    run.totalEvals++;

    // Track score history (sample every ~10 evals to keep size manageable)
    if (run.totalEvals % 10 === 0 || run.totalEvals <= 20) {
      run.scoreHistory.push({
        eval: run.totalEvals,
        score: run.bestScore ?? result.score,
        timestamp: result.timestamp,
      });
      if (run.scoreHistory.length > this.config.maxScoreHistory) {
        run.scoreHistory = run.scoreHistory.slice(-this.config.maxScoreHistory);
      }
    }

    // Stagnation detection
    if (run.totalEvals - this.getLastImprovedEval(run) > this.config.stagnationWindow) {
      if (run.totalEvals % this.config.stagnationWindow === 0) {
        this.addAlert('warning', 'plateau',
          `Plateau: ${run.name}`,
          `No improvement in ${this.config.stagnationWindow} evals. Current best: ${run.bestScore?.toFixed(6)}. Consider adjusting exploration rate or strategy mix.`,
          { runId: run.id, evalsSinceImprovement: run.totalEvals - this.getLastImprovedEval(run) },
        );
      }
    }

    // Milestone alerts
    const milestones = [100, 500, 1000, 5000, 10000, 50000, 100000];
    if (milestones.includes(run.totalEvals)) {
      this.addAlert('info', 'milestone',
        `Milestone: ${run.name} — ${run.totalEvals.toLocaleString()} evals`,
        `Best score: ${run.bestScore?.toFixed(8) ?? 'N/A'} | Improvements: ${run.improvements} | Phase: ${run.phase}`,
        { runId: run.id, totalEvals: run.totalEvals, bestScore: run.bestScore },
      );
    }
  }

  private onNewBest(run: RunTracker, result: EvalResult, improvement: number): void {
    const prevBest = run.bestScore;
    run.bestScore = result.score;
    run.bestParams = result.params;
    run.improvements++;
    run.lastImprovedAt = Date.now();

    // Track which strategy found it
    run.strategyWins[result.strategy] = (run.strategyWins[result.strategy] || 0) + 1;

    // Determine if this is a breakthrough
    const isBreakthrough = prevBest !== null
      && Math.abs(improvement) > Math.abs(prevBest) * this.config.breakthroughThreshold;

    if (isBreakthrough) {
      this.addAlert('breakthrough', 'breakthrough',
        `🔥 Breakthrough: ${run.name}`,
        `Score jumped ${prevBest!.toFixed(6)} → ${result.score.toFixed(6)} (${(improvement / Math.abs(prevBest!) * 100).toFixed(1)}% improvement) via ${result.strategy} at eval #${run.totalEvals}`,
        {
          runId: run.id, previousBest: prevBest, newBest: result.score,
          improvement, strategy: result.strategy, eval: run.totalEvals,
          params: result.params,
        },
      );
    }
  }

  private onDiscovery(run: RunTracker, discovery: Discovery): void {
    run.discoveryCount++;

    const severityMap: Record<string, AlertSeverity> = {
      'anomaly': 'warning',
      'plateau': 'warning',
      'landscape_shift': 'critical',
      'new_best': 'info',
      'convergence': 'info',
      'constraint_boundary': 'info',
    };

    const categoryMap: Record<string, Alert['category']> = {
      'anomaly': 'anomaly',
      'plateau': 'plateau',
      'landscape_shift': 'anomaly',
      'new_best': 'breakthrough',
      'convergence': 'insight',
      'constraint_boundary': 'insight',
    };

    this.addAlert(
      severityMap[discovery.type] || 'info',
      categoryMap[discovery.type] || 'insight',
      `${discovery.type.replace(/_/g, ' ')}: ${run.name}`,
      discovery.description,
      { runId: run.id, confidence: discovery.confidence, score: discovery.result.score },
    );
  }

  private onPhaseChange(run: RunTracker, from: string, to: string): void {
    run.phase = to;
    this.addAlert('info', 'insight',
      `Phase shift: ${run.name}`,
      `${from} → ${to} at eval #${run.totalEvals}. ${this.phaseAdvice(to)}`,
      { runId: run.id, from, to, eval: run.totalEvals },
    );
  }

  private onReport(run: RunTracker, state: AgentState): void {
    run.ufe = state.ufe;
    run.phase = state.phase;

    // Strategy insight: flag if one strategy dominates
    const topStrategy = state.strategies[0];
    if (topStrategy && topStrategy.uses > 50 && topStrategy.avgImprovement > 0) {
      const totalUses = state.strategies.reduce((s, st) => s + st.uses, 0);
      if (topStrategy.uses / totalUses > 0.5) {
        // Only alert once per strategy dominance
        const key = `${run.id}-strategy-${topStrategy.type}`;
        if (!this.alerts.some(a => a.data?.key === key)) {
          this.addAlert('info', 'strategy',
            `Strategy insight: ${topStrategy.type} dominates in ${run.name}`,
            `${topStrategy.type} accounts for ${(topStrategy.uses / totalUses * 100).toFixed(0)}% of evals with avg improvement ${topStrategy.avgImprovement.toFixed(4)}`,
            { runId: run.id, key, strategy: topStrategy.type, share: topStrategy.uses / totalUses },
          );
        }
      }
    }
  }

  private onStopped(run: RunTracker, reason: string, state: AgentState): void {
    run.status = 'completed';
    run.ufe = state.ufe;

    this.addAlert('info', 'milestone',
      `Run complete: ${run.name}`,
      `${reason}. Final score: ${run.bestScore?.toFixed(8)} | ${run.totalEvals} evals | ${run.improvements} improvements | UFE: ${state.ufe ? (state.ufe.ufeRatio * 100).toFixed(1) + '%' : 'N/A'}`,
      { runId: run.id, finalScore: run.bestScore, totalEvals: run.totalEvals, ufe: state.ufe },
    );
  }

  private onConverged(run: RunTracker, result: EvalResult, totalEvals: number): void {
    run.status = 'completed';

    this.addAlert('breakthrough', 'insight',
      `🎯 Converged: ${run.name}`,
      `Optimization converged after ${totalEvals} evals. Final score: ${result.score.toFixed(8)}`,
      { runId: run.id, finalScore: result.score, totalEvals },
    );
  }

  // ─── Alert Management ────────────────────────────────────────────────────

  private addAlert(severity: AlertSeverity, category: Alert['category'], title: string, detail: string, data?: Record<string, any>): Alert {
    const alert: Alert = {
      id: `alert-${++this.alertCounter}`,
      timestamp: Date.now(),
      severity,
      category,
      title,
      detail,
      data,
      acknowledged: false,
    };

    this.alerts.unshift(alert);
    if (this.alerts.length > this.config.maxAlerts) {
      this.alerts = this.alerts.slice(0, this.config.maxAlerts);
    }

    // Console output with color coding
    const icon = severity === 'breakthrough' ? '🔥' : severity === 'critical' ? '🚨' : severity === 'warning' ? '⚠️' : 'ℹ️';
    const ts = new Date().toISOString().slice(11, 19);
    console.log(`${icon} [${ts}] [${category.toUpperCase()}] ${title}`);
    if (severity !== 'info') {
      console.log(`   ${detail}`);
    }

    // Log to file
    if (this.alertLogStream) {
      this.alertLogStream.write(JSON.stringify(alert) + '\n');
    }

    // Webhook for critical/breakthrough
    if ((severity === 'critical' || severity === 'breakthrough') && this.config.webhookUrl) {
      this.sendWebhook(alert);
    }

    // Notify listeners
    for (const listener of this.listeners) {
      try { listener(alert); } catch { /* ignore */ }
    }

    return alert;
  }

  /** Subscribe to alerts */
  onAlert(listener: (alert: Alert) => void): void {
    this.listeners.push(listener);
  }

  /** Acknowledge an alert */
  acknowledgeAlert(alertId: string): boolean {
    const alert = this.alerts.find(a => a.id === alertId);
    if (alert) { alert.acknowledged = true; return true; }
    return false;
  }

  /** Get alerts filtered by category/severity */
  getAlerts(filter?: { category?: Alert['category']; severity?: AlertSeverity; unacknowledgedOnly?: boolean }): Alert[] {
    let result = this.alerts;
    if (filter?.category) result = result.filter(a => a.category === filter.category);
    if (filter?.severity) result = result.filter(a => a.severity === filter.severity);
    if (filter?.unacknowledgedOnly) result = result.filter(a => !a.acknowledged);
    return result;
  }

  /** Get full monitoring snapshot */
  getSnapshot(): MonitorSnapshot {
    return {
      status: this.runs.size > 0 && [...this.runs.values()].some(r => r.status === 'running') ? 'running' : 'idle',
      uptime: (Date.now() - this.startTime) / 1000,
      runs: Object.fromEntries(this.runs),
      alerts: this.alerts,
      summary: {
        totalRuns: this.runs.size,
        totalEvals: [...this.runs.values()].reduce((s, r) => s + r.totalEvals, 0),
        totalBreakthroughs: this.alerts.filter(a => a.category === 'breakthrough').length,
        totalAnomalies: this.alerts.filter(a => a.category === 'anomaly').length,
        activeAlerts: this.alerts.filter(a => !a.acknowledged).length,
      },
    };
  }

  // ─── HTTP Dashboard ──────────────────────────────────────────────────────

  /** Start the live HTTP dashboard */
  startDashboard(): void {
    if (this.config.port <= 0) return;

    this.server = http.createServer((req, res) => {
      const url = req.url || '/';
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST');

      if (url === '/api/snapshot') {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(this.getSnapshot()));
      } else if (url === '/api/alerts') {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(this.alerts.slice(0, 100)));
      } else if (url.startsWith('/api/alerts/')) {
        const category = url.split('/api/alerts/')[1] as Alert['category'];
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(this.getAlerts({ category }).slice(0, 50)));
      } else if (url.startsWith('/api/run/')) {
        const runId = url.split('/api/run/')[1];
        const run = this.runs.get(runId);
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(run || { error: 'not found' }));
      } else if (url === '/api/summary') {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(this.getSnapshot().summary));
      } else if (url === '/') {
        res.setHeader('Content-Type', 'text/html');
        res.end(this.renderDashboardHTML());
      } else {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({
          endpoints: ['/api/snapshot', '/api/alerts', '/api/alerts/:category', '/api/run/:id', '/api/summary'],
        }));
      }
    });

    this.server.listen(this.config.port, () => {
      console.log(`📊 AEGIS Monitor: http://localhost:${this.config.port}`);
    });
  }

  /** Stop the dashboard */
  stopDashboard(): void {
    this.server?.close();
    this.alertLogStream?.end();
  }

  /** Print a formatted status report to console */
  printStatus(): void {
    const snap = this.getSnapshot();
    const lines: string[] = [
      '',
      '╔═══════════════════════════════════════════════════════════════════╗',
      '║                    AEGIS LIVE MONITOR                           ║',
      '╠═══════════════════════════════════════════════════════════════════╣',
      `║  Uptime: ${formatUptime(snap.uptime).padEnd(15)} Active runs: ${String(snap.summary.totalRuns).padEnd(20)}║`,
      `║  Evals: ${snap.summary.totalEvals.toLocaleString().padEnd(16)} Breakthroughs: ${String(snap.summary.totalBreakthroughs).padEnd(18)}║`,
      `║  Alerts: ${String(snap.summary.activeAlerts).padEnd(15)} Anomalies: ${String(snap.summary.totalAnomalies).padEnd(22)}║`,
      '╠═══════════════════════════════════════════════════════════════════╣',
    ];

    // Runs
    for (const [id, run] of this.runs) {
      const status = run.status === 'running' ? '🟢' : run.status === 'completed' ? '✅' : '❌';
      lines.push(
        `║ ${status} ${run.name.padEnd(20)} score=${(run.bestScore?.toFixed(6) ?? 'N/A').padStart(12)} ` +
        `evals=${String(run.totalEvals).padStart(7)} ` +
        `UFE=${run.ufe ? (run.ufe.ufeRatio * 100).toFixed(1).padStart(5) + '%' : '  N/A '} ║`,
      );
    }

    lines.push('╠═══════════════════════════════════════════════════════════════════╣');
    lines.push('║                      RECENT ALERTS                              ║');
    lines.push('╠═══════════════════════════════════════════════════════════════════╣');

    const recentAlerts = this.alerts.slice(0, 8);
    for (const a of recentAlerts) {
      const icon = a.severity === 'breakthrough' ? '🔥' : a.severity === 'critical' ? '🚨' : a.severity === 'warning' ? '⚠️' : 'ℹ️';
      const ts = new Date(a.timestamp).toISOString().slice(11, 19);
      const ack = a.acknowledged ? '✓' : '•';
      lines.push(`║ ${ack} ${icon} [${ts}] ${a.title.substring(0, 50).padEnd(50)} ║`);
    }

    if (recentAlerts.length === 0) {
      lines.push('║  No alerts yet                                                  ║');
    }

    lines.push('╚═══════════════════════════════════════════════════════════════════╝');
    console.log(lines.join('\n'));
  }

  // ─── Internal ────────────────────────────────────────────────────────────

  private getLastImprovedEval(run: RunTracker): number {
    // Approximate from history
    if (run.scoreHistory.length < 2) return run.totalEvals;
    const lastImproveIdx = run.scoreHistory.findIndex((h, i) =>
      i > 0 && h.score < run.scoreHistory[i - 1].score);
    if (lastImproveIdx === -1) return 0;
    return run.scoreHistory[run.scoreHistory.length - 1].eval - (run.totalEvals - run.lastImprovedAt);
  }

  private phaseAdvice(phase: string): string {
    switch (phase) {
      case 'exploring': return 'Broad search active — building initial model of the landscape.';
      case 'exploiting': return 'Narrowing in on promising region — high convergence rate.';
      case 'curious': return 'Exploration rate increased — agent seeks novel regions to escape local optima.';
      case 'converged': return 'Near-optimal solution found — minimal further improvement expected.';
      default: return '';
    }
  }

  private sendWebhook(alert: Alert): void {
    if (!this.config.webhookUrl) return;
    try {
      const body = JSON.stringify({
        text: `[${alert.severity.toUpperCase()}] ${alert.title}\n${alert.detail}`,
        alert, timestamp: new Date().toISOString(),
      });
      const parsed = new URL(this.config.webhookUrl);
      const lib = parsed.protocol === 'https:' ? require('https') : require('http');
      const req = lib.request(this.config.webhookUrl, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
      });
      req.on('error', () => {});
      req.write(body);
      req.end();
    } catch { /* best effort */ }
  }

  private renderDashboardHTML(): string {
    const snap = this.getSnapshot();
    const runs = Object.values(snap.runs);

    // ── Classify runs by domain ──
    const domainLabels: Record<string, string> = {
      'einstein-cartan': 'Einstein-Cartan Torsion',
      'ft-gravity': 'f(T) Teleparallel Gravity',
      'ufe-torsion': 'UFE Torsion Field',
      'torsion-wave': 'Torsion Wave Propagation',
    };
    const domains = Object.keys(domainLabels);

    function classifyDomain(id: string): string | null {
      for (const d of domains) { if (id.includes(d)) return d; }
      return null;
    }

    // Best result per domain (all-time)
    const domainBests: Record<string, RunTracker | null> = {};
    for (const d of domains) domainBests[d] = null;
    for (const r of runs) {
      const d = classifyDomain(r.id);
      if (!d || r.bestScore === null) continue;
      if (!domainBests[d] || r.bestScore! < domainBests[d]!.bestScore!) {
        domainBests[d] = r;
      }
    }

    // Extract scientific contributions: breakthroughs + convergences + anomalies
    const contributions = this.alerts.filter(a =>
      a.category === 'breakthrough' || a.category === 'anomaly' ||
      (a.category === 'insight' && a.severity === 'breakthrough')
    );

    // Major improvements: top N largest score jumps
    const majorImprovements = this.alerts
      .filter(a => a.category === 'breakthrough' && a.data?.improvement !== undefined)
      .sort((a, b) => Math.abs(b.data!.improvement) - Math.abs(a.data!.improvement))
      .slice(0, 15);

    // Strategy leaderboard across all runs
    const stratWins: Record<string, number> = {};
    for (const r of runs) {
      for (const [strat, count] of Object.entries(r.strategyWins)) {
        stratWins[strat] = (stratWins[strat] || 0) + (count as number);
      }
    }
    const stratLeaderboard = Object.entries(stratWins).sort((a, b) => b[1] - a[1]);
    const totalStratWins = stratLeaderboard.reduce((s, e) => s + e[1], 0);

    // UFE efficiency rankings
    const ufeRanked = runs
      .filter(r => r.ufe && r.ufe.ufeRatio > 0)
      .sort((a, b) => b.ufe!.ufeRatio - a.ufe!.ufeRatio)
      .slice(0, 10);

    // Format helpers
    const fmtScore = (n: number | null) => n === null ? 'N/A' : Math.abs(n) < 0.001 && n !== 0 ? n.toExponential(4) : n.toFixed(6);
    const fmtPct = (n: number) => (n * 100).toFixed(1) + '%';
    const fmtParam = (k: string, v: number) => `<span class="param-name">${k}</span>=<span class="param-val">${Math.abs(v) < 0.001 && v !== 0 ? v.toExponential(3) : v.toFixed(6)}</span>`;

    return `<!DOCTYPE html>
<html><head><title>AEGIS Monitor</title>
<meta http-equiv="refresh" content="5">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0a0e14; color: #c9d1d9; font-family: 'SF Mono', 'Consolas', 'Fira Code', monospace; }
  .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 16px; max-width: 1600px; margin: 0 auto; }
  .full-width { grid-column: 1 / -1; }

  .header { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
  .header h1 { color: #58a6ff; font-size: 20px; margin-bottom: 6px; letter-spacing: 2px; }
  .header .subtitle { color: #8b949e; font-size: 11px; }

  .stats-bar { display: flex; flex-wrap: wrap; gap: 8px; }
  .stat-box { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 12px 16px; flex: 1; min-width: 120px; text-align: center; }
  .stat-box .val { font-size: 26px; font-weight: bold; }
  .stat-box .lbl { font-size: 10px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
  .val.blue { color: #58a6ff; } .val.green { color: #3fb950; } .val.orange { color: #f0883e; }
  .val.red { color: #f85149; } .val.purple { color: #bc8cff; } .val.cyan { color: #39d353; }

  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
  .card-title { background: #0d1117; padding: 10px 16px; font-size: 12px; color: #58a6ff; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
  .card-title .count { background: #30363d; color: #c9d1d9; padding: 2px 8px; border-radius: 10px; font-size: 10px; }
  .card-body { padding: 12px 16px; max-height: 420px; overflow-y: auto; }

  /* Domain cards */
  .domain-card { padding: 12px; border-bottom: 1px solid #21262d; }
  .domain-card:last-child { border-bottom: none; }
  .domain-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .domain-name { color: #f0883e; font-weight: bold; font-size: 13px; }
  .domain-score { color: #3fb950; font-size: 18px; font-weight: bold; }
  .domain-score.none { color: #484f58; font-size: 14px; }
  .params-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 4px; margin-top: 6px; }
  .param-name { color: #bc8cff; }
  .param-val { color: #79c0ff; }
  .domain-meta { color: #8b949e; font-size: 11px; margin-top: 4px; }

  /* Contributions */
  .contrib { padding: 10px 12px; border-bottom: 1px solid #21262d; }
  .contrib:last-child { border-bottom: none; }
  .contrib-header { display: flex; justify-content: space-between; margin-bottom: 4px; }
  .contrib-title { font-weight: bold; font-size: 12px; }
  .contrib-time { color: #8b949e; font-size: 10px; }
  .contrib-detail { color: #8b949e; font-size: 11px; line-height: 1.4; }
  .contrib.breakthrough .contrib-title { color: #f0883e; }
  .contrib.anomaly .contrib-title { color: #f85149; }
  .contrib.convergence .contrib-title { color: #3fb950; }

  /* Improvements table */
  table { width: 100%; border-collapse: collapse; font-size: 11px; }
  th { text-align: left; padding: 6px 10px; color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #30363d; }
  td { padding: 6px 10px; border-bottom: 1px solid #21262d; }
  tr:hover { background: #1c2128; }

  /* Strategy bar */
  .strat-row { display: flex; align-items: center; padding: 4px 0; }
  .strat-name { width: 100px; font-size: 11px; color: #bc8cff; }
  .strat-bar-bg { flex: 1; height: 16px; background: #21262d; border-radius: 3px; overflow: hidden; margin: 0 8px; }
  .strat-bar { height: 100%; border-radius: 3px; transition: width 0.5s; }
  .strat-count { width: 50px; text-align: right; font-size: 11px; color: #8b949e; }

  /* Runs table */
  .run-status { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
  .run-status.running { background: #3fb950; box-shadow: 0 0 4px #3fb950; }
  .run-status.completed { background: #58a6ff; }
  .run-status.failed { background: #f85149; }

  /* Scrollbar */
  .card-body::-webkit-scrollbar { width: 4px; }
  .card-body::-webkit-scrollbar-track { background: #0d1117; }
  .card-body::-webkit-scrollbar-thumb { background: #30363d; border-radius: 2px; }

  @media (max-width: 900px) { .dashboard { grid-template-columns: 1fr; } }
</style></head><body>
<div class="dashboard">

  <!-- Header -->
  <div class="header full-width">
    <h1>⚡ AEGIS — LIVE SCIENTIFIC MONITOR</h1>
    <div class="subtitle">Autonomous Evolving General Intelligence System — Torsion Field Theory Exploration &nbsp;|&nbsp; Uptime: ${formatUptime(snap.uptime)} &nbsp;|&nbsp; Last refresh: ${new Date().toISOString().slice(11, 19)} UTC</div>
  </div>

  <!-- Stats Bar -->
  <div class="stats-bar full-width">
    <div class="stat-box"><div class="val blue">${snap.summary.totalEvals.toLocaleString()}</div><div class="lbl">Evaluations</div></div>
    <div class="stat-box"><div class="val green">${snap.summary.totalRuns}</div><div class="lbl">Runs</div></div>
    <div class="stat-box"><div class="val orange">${snap.summary.totalBreakthroughs}</div><div class="lbl">Breakthroughs</div></div>
    <div class="stat-box"><div class="val red">${snap.summary.totalAnomalies}</div><div class="lbl">Anomalies</div></div>
    <div class="stat-box"><div class="val purple">${contributions.length}</div><div class="lbl">Contributions</div></div>
    <div class="stat-box"><div class="val cyan">${runs.filter(r => r.status === 'running').length}</div><div class="lbl">Active Now</div></div>
  </div>

  <!-- Best Results by Torsion Domain -->
  <div class="card full-width">
    <div class="card-title">🔬 Best Results by Physics Domain <span class="count">${domains.length} domains</span></div>
    <div class="card-body">
${domains.map(d => {
  const best = domainBests[d];
  const domainRuns = runs.filter(r => classifyDomain(r.id) === d);
  const completed = domainRuns.filter(r => r.bestScore !== null).length;
  if (!best) {
    return `<div class="domain-card">
      <div class="domain-header"><span class="domain-name">${domainLabels[d]}</span><span class="domain-score none">Awaiting data…</span></div>
      <div class="domain-meta">${domainRuns.length} run(s) tracked, ${completed} with results</div>
    </div>`;
  }
  const paramsHTML = best.bestParams
    ? Object.entries(best.bestParams).map(([k, v]) => fmtParam(k, v as number)).join(' &nbsp;│&nbsp; ')
    : 'N/A';
  const topStrat = Object.entries(best.strategyWins).sort((a, b) => (b[1] as number) - (a[1] as number))[0];
  return `<div class="domain-card">
    <div class="domain-header">
      <span class="domain-name">${domainLabels[d]}</span>
      <span class="domain-score">${fmtScore(best.bestScore)}</span>
    </div>
    <div class="params-grid">${paramsHTML}</div>
    <div class="domain-meta">
      ${completed} runs completed &nbsp;│&nbsp;
      ${best.totalEvals.toLocaleString()} evals on best run &nbsp;│&nbsp;
      ${best.improvements} improvements &nbsp;│&nbsp;
      UFE: ${best.ufe ? fmtPct(best.ufe.ufeRatio) : 'N/A'} &nbsp;│&nbsp;
      Top strategy: ${topStrat ? topStrat[0] : 'N/A'}
    </div>
  </div>`;
}).join('\n')}
    </div>
  </div>

  <!-- Major Improvements (left column) -->
  <div class="card">
    <div class="card-title">🏆 Major Improvements <span class="count">${majorImprovements.length}</span></div>
    <div class="card-body">
${majorImprovements.length === 0 ? '<p style="color:#484f58;text-align:center;padding:20px;">Accumulating data…</p>' :
  `<table>
    <tr><th>Run</th><th>Improvement</th><th>New Score</th><th>Strategy</th><th>Eval #</th></tr>
    ${majorImprovements.map(a => {
      const d = a.data || {};
      const impPct = d.previousBest && d.previousBest !== 0
        ? (Math.abs(d.improvement) / Math.abs(d.previousBest) * 100).toFixed(1) + '%'
        : '—';
      return `<tr>
        <td style="color:#f0883e">${a.title.replace(/🔥\s*Breakthrough:\s*/, '').substring(0, 35)}</td>
        <td style="color:#3fb950">${impPct}</td>
        <td>${fmtScore(d.newBest ?? null)}</td>
        <td style="color:#bc8cff">${d.strategy || '—'}</td>
        <td>#${d.eval || '—'}</td>
      </tr>`;
    }).join('\n')}
  </table>`
}
    </div>
  </div>

  <!-- Strategy Effectiveness (right column) -->
  <div class="card">
    <div class="card-title">🧠 Strategy Effectiveness <span class="count">${stratLeaderboard.length} strategies</span></div>
    <div class="card-body" style="padding:16px;">
${stratLeaderboard.length === 0 ? '<p style="color:#484f58;text-align:center;">No strategy data yet</p>' :
  stratLeaderboard.map(([name, count], i) => {
    const pct = totalStratWins > 0 ? count / totalStratWins * 100 : 0;
    const colors = ['#f0883e', '#58a6ff', '#3fb950', '#bc8cff', '#f85149', '#d29922', '#39d353', '#79c0ff', '#ff7b72', '#d2a8ff'];
    const color = colors[i % colors.length];
    return `<div class="strat-row">
      <span class="strat-name">${name}</span>
      <div class="strat-bar-bg"><div class="strat-bar" style="width:${pct}%;background:${color}"></div></div>
      <span class="strat-count">${count}</span>
    </div>`;
  }).join('\n')
}
    </div>
  </div>

  <!-- Scientific Contributions Feed (left column) -->
  <div class="card">
    <div class="card-title">📡 Scientific Contributions <span class="count">${contributions.length}</span></div>
    <div class="card-body">
${contributions.length === 0 ? '<p style="color:#484f58;text-align:center;padding:20px;">No discoveries yet — engines are exploring…</p>' :
  contributions.slice(0, 25).map(a => {
    const ts = new Date(a.timestamp).toISOString().slice(11, 19);
    const cls = a.category === 'breakthrough' ? 'breakthrough' : a.category === 'anomaly' ? 'anomaly' : 'convergence';
    const icon = a.severity === 'breakthrough' ? '🔥' : a.severity === 'critical' ? '🚨' : '🎯';
    return `<div class="contrib ${cls}">
      <div class="contrib-header"><span class="contrib-title">${icon} ${a.title}</span><span class="contrib-time">${ts}</span></div>
      <div class="contrib-detail">${a.detail}</div>
    </div>`;
  }).join('\n')
}
    </div>
  </div>

  <!-- UFE Efficiency Rankings (right column) -->
  <div class="card">
    <div class="card-title">📊 UFE Efficiency Rankings <span class="count">Top ${ufeRanked.length}</span></div>
    <div class="card-body">
${ufeRanked.length === 0 ? '<p style="color:#484f58;text-align:center;padding:20px;">Waiting for completed runs…</p>' :
  `<table>
    <tr><th>Run</th><th>UFE Ratio</th><th>Conv. Velocity</th><th>AUCC</th><th>Evals</th></tr>
    ${ufeRanked.map(r => `<tr>
      <td>${r.name.substring(0, 35)}</td>
      <td style="color:#3fb950">${fmtPct(r.ufe!.ufeRatio)}</td>
      <td>${r.ufe!.convergenceVelocity.toFixed(4)}</td>
      <td>${r.ufe!.aucc.toFixed(2)}</td>
      <td>${r.totalEvals.toLocaleString()}</td>
    </tr>`).join('\n')}
  </table>`
}
    </div>
  </div>

  <!-- Active Runs -->
  <div class="card full-width">
    <div class="card-title">⚙ Active Runs <span class="count">${runs.length}</span></div>
    <div class="card-body">
      <table>
        <tr><th>Run</th><th>Status</th><th>Evals</th><th>Best Score</th><th>UFE</th><th>Phase</th><th>Improvements</th><th>Top Strategy</th></tr>
        ${runs.slice(-30).reverse().map(r => {
          const topS = Object.entries(r.strategyWins).sort((a, b) => (b[1] as number) - (a[1] as number))[0];
          return `<tr>
            <td><span class="run-status ${r.status}"></span>${r.name}</td>
            <td>${r.status}</td>
            <td>${r.totalEvals.toLocaleString()}</td>
            <td>${fmtScore(r.bestScore)}</td>
            <td>${r.ufe ? fmtPct(r.ufe.ufeRatio) : '—'}</td>
            <td>${r.phase}</td>
            <td>${r.improvements}</td>
            <td style="color:#bc8cff">${topS ? topS[0] : '—'}</td>
          </tr>`;
        }).join('\n')}
      </table>
    </div>
  </div>

  <!-- Alerts Feed -->
  <div class="card full-width">
    <div class="card-title">🔔 All Alerts <span class="count">${this.alerts.length}</span></div>
    <div class="card-body">
${this.alerts.slice(0, 30).map(a => {
  const ts = new Date(a.timestamp).toISOString().slice(11, 19);
  return `<div class="alert ${a.severity}"><strong>[${ts}] ${a.title}</strong><br><small>${a.detail}</small></div>`;
}).join('\n')}
${this.alerts.length === 0 ? '<p style="color:#484f58">No alerts yet</p>' : ''}
    </div>
  </div>

</div>
<script>setTimeout(() => location.reload(), 5000);</script>
</body></html>`;
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatUptime(seconds: number): string {
  if (seconds < 60) return `${Math.floor(seconds)}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
  return `${Math.floor(seconds / 86400)}d ${Math.floor((seconds % 86400) / 3600)}h`;
}

// ─── Quick Factory ───────────────────────────────────────────────────────────

/**
 * Create a live monitor and start the dashboard.
 *
 * @example
 * const monitor = createMonitor({ port: 5555 });
 * const agent = new AegisAgent(task, config);
 * agent.on(monitor.createHandler('run-1'));
 * monitor.startDashboard();
 * await agent.run();
 * monitor.printStatus();
 */
export function createMonitor(config?: MonitorConfig): LiveMonitor {
  const monitor = new LiveMonitor(config);
  return monitor;
}
