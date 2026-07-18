/**
 * AEGIS — UFE Model Comparison Runner
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Head-to-head model racing with statistical rigor.
 * Runs N trials per model × benchmark, computes ELO, CI, significance.
 */

import { AegisAgent } from './agent';
import { benchmarkFunctions } from './benchmarks';
import {
  ComparisonConfig, ModelConfig, TrialResult, LeaderboardEntry, StatisticalTest,
} from './interfaces';
import { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating } from './statistics';

export interface ComparisonReport {
  leaderboard: LeaderboardEntry[];
  trials: TrialResult[];
  pairwise: Array<{ modelA: string; modelB: string; test: StatisticalTest; metric: string }>;
  summary: string;
}

export async function compareModels(config: ComparisonConfig): Promise<ComparisonReport> {
  const verbosity = config.verbosity || 'normal';
  const baseSeed = config.baseSeed || 42;
  const benchmarkIds = config.benchmarks === 'all'
    ? Object.keys(benchmarkFunctions) as Array<keyof typeof benchmarkFunctions>
    : config.benchmarks;

  const allTrials: TrialResult[] = [];
  const elo = new ELORating(32);
  for (const model of config.models) elo.register(model.id);

  if (verbosity !== 'silent') {
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║              AEGIS Model Comparison                       ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║  Models: ${config.models.map(m => m.name).join(', ').substring(0, 47).padEnd(48)}║`);
    console.log(`║  Benchmarks: ${benchmarkIds.length} functions × ${config.trials} trials              ║`);
    console.log(`║  Budget: ${config.budget} evals per trial                         ║`);
    console.log('╚═══════════════════════════════════════════════════════════╝\n');
  }

  for (const benchId of benchmarkIds) {
    const bench = (benchmarkFunctions as any)[benchId] as (typeof benchmarkFunctions)['rosenbrock'];
    if (!bench) continue;

    if (verbosity !== 'silent') console.log(`\n── ${bench.name} ──`);

    for (let trial = 0; trial < config.trials; trial++) {
      const trialSeed = baseSeed + trial;
      const trialResults: Map<string, TrialResult> = new Map();

      for (const model of config.models) {
        const agent = new AegisAgent(bench, {
          ...model.agentConfig,
          maxEvals: config.budget,
          verbosity: 'silent',
          seed: trialSeed,
        });

        const start = Date.now();
        const state = await agent.run(bench.optimum);
        const wallTime = (Date.now() - start) / 1000;

        const result: TrialResult = {
          modelId: model.id, benchmarkId: benchId, trial,
          finalScore: state.best?.score ?? Infinity,
          ufe: state.ufe, wallTime, seed: trialSeed,
        };
        allTrials.push(result);
        trialResults.set(model.id, result);
      }

      // Pairwise ELO
      for (let i = 0; i < config.models.length; i++) {
        for (let j = i + 1; j < config.models.length; j++) {
          const rA = trialResults.get(config.models[i].id)!;
          const rB = trialResults.get(config.models[j].id)!;
          const metricA = getMetric(rA, config.rankBy);
          const metricB = getMetric(rB, config.rankBy);
          const lowerBetter = config.rankBy !== 'ufe_ratio';
          const scoreA = lowerBetter
            ? (metricA < metricB ? 1 : metricA > metricB ? 0 : 0.5)
            : (metricA > metricB ? 1 : metricA < metricB ? 0 : 0.5);
          elo.recordMatch(config.models[i].id, config.models[j].id, scoreA);
        }
      }
    }
  }

  // Build leaderboard
  const leaderboard: LeaderboardEntry[] = config.models.map(model => {
    const modelTrials = allTrials.filter(t => t.modelId === model.id);
    const scores = modelTrials.map(t => t.finalScore);
    const ufes = modelTrials.map(t => t.ufe.ufeRatio);
    const auccs = modelTrials.map(t => t.ufe.aucc);
    const ci = bootstrapCI(scores);
    return {
      modelId: model.id, modelName: model.name,
      meanScore: ci.mean, meanUFE: ufes.reduce((a, b) => a + b, 0) / ufes.length,
      meanAUCC: auccs.reduce((a, b) => a + b, 0) / auccs.length,
      wins: 0, losses: 0, ties: 0,
      elo: elo.getRating(model.id), ci95: [ci.lower, ci.upper],
    };
  });

  // Pairwise tests
  const pairwise: ComparisonReport['pairwise'] = [];
  for (let i = 0; i < config.models.length; i++) {
    for (let j = i + 1; j < config.models.length; j++) {
      const scoresA = allTrials.filter(t => t.modelId === config.models[i].id).map(t => getMetric(t, config.rankBy));
      const scoresB = allTrials.filter(t => t.modelId === config.models[j].id).map(t => getMetric(t, config.rankBy));
      const mw = mannWhitneyU(scoresA, scoresB);
      const d = cohensD(scoresA, scoresB);

      const pairedA: number[] = [], pairedB: number[] = [];
      for (const benchId of benchmarkIds) {
        for (let t = 0; t < config.trials; t++) {
          const a = allTrials.find(r => r.modelId === config.models[i].id && r.benchmarkId === benchId && r.trial === t);
          const b = allTrials.find(r => r.modelId === config.models[j].id && r.benchmarkId === benchId && r.trial === t);
          if (a && b) { pairedA.push(getMetric(a, config.rankBy)); pairedB.push(getMetric(b, config.rankBy)); }
        }
      }
      const ws = wilcoxonSignedRank(pairedA, pairedB);

      const test: StatisticalTest = {
        test: `${mw.test} + ${ws.test}`,
        pValue: Math.max(mw.pValue, ws.pValue),
        effectSize: Math.abs(d),
        significant: mw.significant && ws.significant,
        direction: mw.significant ? mw.direction : 'no_difference',
      };

      pairwise.push({ modelA: config.models[i].id, modelB: config.models[j].id, test, metric: config.rankBy });

      const entryA = leaderboard.find(e => e.modelId === config.models[i].id)!;
      const entryB = leaderboard.find(e => e.modelId === config.models[j].id)!;
      if (test.significant) {
        if (test.direction === 'a_better') { entryA.wins++; entryB.losses++; }
        else if (test.direction === 'b_better') { entryB.wins++; entryA.losses++; }
        else { entryA.ties++; entryB.ties++; }
      } else { entryA.ties++; entryB.ties++; }
    }
  }

  leaderboard.sort((a, b) => b.elo - a.elo);

  let summary = '';
  if (verbosity !== 'silent') {
    summary = formatReport(leaderboard, pairwise);
    console.log(summary);
  }

  return { leaderboard, trials: allTrials, pairwise, summary };
}

function getMetric(trial: TrialResult, metric: ComparisonConfig['rankBy']): number {
  switch (metric) {
    case 'final_score': return trial.finalScore;
    case 'ufe_ratio': return trial.ufe.ufeRatio;
    case 'aucc': return trial.ufe.aucc;
    case 'time_to_target_50': return trial.ufe.timeToTarget.pct50 ?? Infinity;
  }
}

function formatReport(leaderboard: LeaderboardEntry[], pairwise: ComparisonReport['pairwise']): string {
  const lines: string[] = [
    '', '╔═══════════════════════════════════════════════════════════╗',
    '║                   LEADERBOARD                             ║',
    '╠═══════════════════════════════════════════════════════════╣',
  ];
  for (let i = 0; i < leaderboard.length; i++) {
    const e = leaderboard[i];
    const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : '  ';
    lines.push(
      `║ ${medal} ${e.modelName.padEnd(18)} ELO=${String(e.elo).padStart(4)} | ` +
      `Score=${e.meanScore.toFixed(4).padStart(10)} | ` +
      `UFE=${(e.meanUFE * 100).toFixed(1).padStart(5)}% | ` +
      `W${e.wins}/L${e.losses}/T${e.ties} ║`
    );
  }
  lines.push('╚═══════════════════════════════════════════════════════════╝');
  return lines.join('\n');
}
