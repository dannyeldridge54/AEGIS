/**
 * Seeker — UFE Model Comparison Runner
 * Head-to-head model racing with statistical rigor.
 * Runs N trials per model × benchmark, computes ELO, CI, significance.
 */
import { ComparisonConfig, TrialResult, LeaderboardEntry, StatisticalTest } from './interfaces';
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
export declare function compareModels(config: ComparisonConfig): Promise<ComparisonReport>;
//# sourceMappingURL=comparison.d.ts.map