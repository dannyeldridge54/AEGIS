/**
 * Seeker — Statistical Engine
 * Bootstrap confidence intervals, Mann-Whitney U, Wilcoxon signed-rank,
 * Cohen's d effect size. Powers all model comparisons.
 */
export interface CIResult {
    mean: number;
    lower: number;
    upper: number;
    std: number;
    n: number;
}
export interface TestResult {
    test: string;
    pValue: number;
    effectSize: number;
    significant: boolean;
    direction: 'a_better' | 'b_better' | 'no_difference';
}
/**
 * Compute bootstrap 95% CI for the mean.
 * Uses percentile method with 10,000 resamples.
 */
export declare function bootstrapCI(data: number[], nBoot?: number, alpha?: number): CIResult;
/**
 * Two-sample Mann-Whitney U test.
 * Tests whether one sample tends to have larger values than the other.
 * Uses normal approximation for n > 20.
 */
export declare function mannWhitneyU(a: number[], b: number[]): TestResult;
/**
 * Paired Wilcoxon signed-rank test.
 * For comparing two models on the same benchmarks (paired observations).
 */
export declare function wilcoxonSignedRank(a: number[], b: number[]): TestResult;
/**
 * Cohen's d: standardized mean difference.
 * |d| < 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, >0.8 = large
 */
export declare function cohensD(a: number[], b: number[]): number;
export declare class ELORating {
    private ratings;
    private readonly K;
    constructor(k?: number, initialRating?: number);
    private initialRating;
    register(id: string): void;
    /** Record a match result. scoreA: 1 = A wins, 0 = B wins, 0.5 = draw */
    recordMatch(idA: string, idB: string, scoreA: number): void;
    getRating(id: string): number;
    getLeaderboard(): Array<{
        id: string;
        elo: number;
    }>;
}
//# sourceMappingURL=statistics.d.ts.map