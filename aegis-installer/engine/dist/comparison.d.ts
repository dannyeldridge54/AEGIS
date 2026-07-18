/**
 * AEGIS — UFE Model Comparison Runner
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
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
export declare function compareModels(config: ComparisonConfig): Promise<ComparisonReport>;
//# sourceMappingURL=comparison.d.ts.map