/**
 * Seeker — UFE Model Comparison Runner
 * Head-to-head model racing with statistical rigor.
 * Runs N trials per model × benchmark, computes ELO, CI, significance.
 */

import { SeekerAgent } from './agent';
import { benchmarkFunctions } from './benchmarks';
import {
  ComparisonConfig, ModelConfig, TrialResult, LeaderboardEntry,
  StatisticalTest, UFEMetrics,
} from './interfaces';
import { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating } from './statistics';

export interface ComparisonReport {
  leaderboard: LeaderboardEntry[];
  trials: TrialResult[];
  pairwise: Array<{
    modelA: string;
    modelB: string;
    test: StatisticalTest;
    metric: string;
  }>;
  summary: string;
}

/**
 * Run a full model comparison: multiple models × benchmarks × trials.
 * Returns leaderboard with ELO ratings, CI, and pairwise significance tests.
 */
export async function compareModels(config: ComparisonConfig): Promise<ComparisonReport> {
  const verbosity = config.verbosity || 'normal';
  const baseSeed = config.baseSeed || 42;
  const benchmarkIds = config.benchmarks === 'all'
    ? Object.keys(benchmarkFunctions)
    : config.benchmarks;

  const allTrials: TrialResult[] = [];
  const elo = new ELORating(32);

  // Register all models
  for (const model of config.models) elo.register(model.id);

  if (verbosity !== 'silent') {
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║              Seeker Model Comparison                      ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║  Models: ${config.models.map(m => m.name).join(', ').substring(0, 47).padEnd(48)}║`);
    console.log(`║  Benchmarks: ${benchmarkIds.length} functions × ${config.trials} trials              ║`);
    console.log(`║  Budget: ${config.budget} evals per trial                         ║`);
    console.log('╚═══════════════════════════════════════════════════════════╝\n');
  }

  // Run all trials
  for (const benchId of benchmarkIds) {
    const bench = benchmarkFunctions[benchId];
    if (!bench) {
      if (verbosity !== 'silent') console.log(`⚠️ Unknown benchmark: ${benchId}, skipping`);
      continue;
    }

    if (verbosity !== 'silent') {
      console.log(`\n── ${bench.name} ──`);
    }

    for (let trial = 0; trial < config.trials; trial++) {
      const trialSeed = baseSeed + trial;
      const trialResults: Map<string, TrialResult> = new Map();

      for (const model of config.models) {
        const agent = new SeekerAgent(bench, {
          ...model.agentConfig,
          maxEvals: config.budget,
          verbosity: 'silent',
          seed: trialSeed,
        });

        const start = Date.now();
        const state = await agent.run(bench.optimum);
        const wallTime = (Date.now() - start) / 1000;

        const result: TrialResult = {
          modelId: model.id,
          benchmarkId: benchId,
          trial,
          finalScore: state.best?.score ?? Infinity,
          ufe: state.ufe,
          wallTime,
          seed: trialSeed,
          discoveries: state.discoveries,
        };

        allTrials.push(result);
        trialResults.set(model.id, result);
      }

      // Pairwise ELO updates for this trial
      const models = config.models;
      for (let i = 0; i < models.length; i++) {
        for (let j = i + 1; j < models.length; j++) {
          const rA = trialResults.get(models[i].id)!;
          const rB = trialResults.get(models[j].id)!;

          const metricA = getMetric(rA, config.rankBy);
          const metricB = getMetric(rB, config.rankBy);

          // Lower is better for score/aucc, higher for ufe_ratio
          const lowerBetter = config.rankBy !== 'ufe_ratio';
          const scoreA = lowerBetter
            ? (metricA < metricB ? 1 : metricA > metricB ? 0 : 0.5)
            : (metricA > metricB ? 1 : metricA < metricB ? 0 : 0.5);

          elo.recordMatch(models[i].id, models[j].id, scoreA);
        }
      }

      if (verbosity === 'verbose') {
        for (const model of models) {
          const r = trialResults.get(model.id)!;
          console.log(`  Trial ${trial + 1}: ${model.name.padEnd(20)} score=${r.finalScore.toFixed(6)} UFE=${(r.ufe.ufeRatio * 100).toFixed(1)}% discoveries=${r.discoveries.length}`);
        }
      }
    }
  }

  // ── Build Leaderboard ──
  const leaderboard: LeaderboardEntry[] = config.models.map(model => {
    const modelTrials = allTrials.filter(t => t.modelId === model.id);
    const scores = modelTrials.map(t => t.finalScore);
    const ufes = modelTrials.map(t => t.ufe.ufeRatio);
    const auccs = modelTrials.map(t => t.ufe.aucc);

    const ci = bootstrapCI(scores);

    return {
      modelId: model.id,
      modelName: model.name,
      meanScore: ci.mean,
      meanUFE: ufes.reduce((a, b) => a + b, 0) / ufes.length,
      meanAUCC: auccs.reduce((a, b) => a + b, 0) / auccs.length,
      wins: 0, losses: 0, ties: 0,
      elo: elo.getRating(model.id),
      ci95: [ci.lower, ci.upper],
    };
  });

  // ── Pairwise Statistical Tests ──
  const pairwise: ComparisonReport['pairwise'] = [];
  const models = config.models;

  for (let i = 0; i < models.length; i++) {
    for (let j = i + 1; j < models.length; j++) {
      const scoresA = allTrials.filter(t => t.modelId === models[i].id).map(t => getMetric(t, config.rankBy));
      const scoresB = allTrials.filter(t => t.modelId === models[j].id).map(t => getMetric(t, config.rankBy));

      // Unpaired test
      const mw = mannWhitneyU(scoresA, scoresB);

      // Paired test (same benchmark+trial pairs)
      const pairedA: number[] = [], pairedB: number[] = [];
      for (const benchId of benchmarkIds) {
        for (let t = 0; t < config.trials; t++) {
          const a = allTrials.find(r => r.modelId === models[i].id && r.benchmarkId === benchId && r.trial === t);
          const b = allTrials.find(r => r.modelId === models[j].id && r.benchmarkId === benchId && r.trial === t);
          if (a && b) {
            pairedA.push(getMetric(a, config.rankBy));
            pairedB.push(getMetric(b, config.rankBy));
          }
        }
      }
      const ws = wilcoxonSignedRank(pairedA, pairedB);
      const d = cohensD(scoresA, scoresB);

      // Use the more conservative test
      const test: StatisticalTest = {
        test: `${mw.test} + ${ws.test}`,
        pValue: Math.max(mw.pValue, ws.pValue),
        effectSize: Math.abs(d),
        significant: mw.significant && ws.significant,
        direction: mw.significant ? mw.direction : 'no_difference',
      };

      pairwise.push({
        modelA: models[i].id,
        modelB: models[j].id,
        test,
        metric: config.rankBy,
      });

      // Update W/L/T
      const entryA = leaderboard.find(e => e.modelId === models[i].id)!;
      const entryB = leaderboard.find(e => e.modelId === models[j].id)!;
      if (test.significant) {
        if (test.direction === 'a_better') { entryA.wins++; entryB.losses++; }
        else if (test.direction === 'b_better') { entryB.wins++; entryA.losses++; }
        else { entryA.ties++; entryB.ties++; }
      } else {
        entryA.ties++;
        entryB.ties++;
      }
    }
  }

  // Sort leaderboard by ELO
  leaderboard.sort((a, b) => b.elo - a.elo);

  // ── Print Results ──
  let summary = '';
  if (verbosity !== 'silent') {
    summary = formatReport(leaderboard, pairwise, config);
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

function formatReport(
  leaderboard: LeaderboardEntry[],
  pairwise: ComparisonReport['pairwise'],
  config: ComparisonConfig
): string {
  const lines: string[] = [
    '',
    '╔═══════════════════════════════════════════════════════════╗',
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

  lines.push('╠═══════════════════════════════════════════════════════════╣');
  lines.push('║                PAIRWISE COMPARISONS                      ║');
  lines.push('╠═══════════════════════════════════════════════════════════╣');

  for (const pw of pairwise) {
    const sig = pw.test.significant ? '✅ SIG' : '➖ n.s.';
    const dir = pw.test.direction === 'a_better' ? `${pw.modelA} >`
      : pw.test.direction === 'b_better' ? `${pw.modelB} >`
      : 'tied';
    lines.push(
      `║  ${pw.modelA} vs ${pw.modelB}: ${sig} p=${pw.test.pValue.toFixed(4)} d=${pw.test.effectSize.toFixed(2)} ${dir} ║`
    );
  }

  lines.push('╚═══════════════════════════════════════════════════════════╝');
  return lines.join('\n');
}
