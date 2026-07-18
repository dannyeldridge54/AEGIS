/**
 * AEGIS — Statistical Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Bootstrap confidence intervals, Mann-Whitney U, Wilcoxon signed-rank,
 * Cohen's d effect size, ELO rating. Powers all model comparisons.
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
export declare function bootstrapCI(data: number[], nBoot?: number, alpha?: number): CIResult;
export declare function mannWhitneyU(a: number[], b: number[]): TestResult;
export declare function wilcoxonSignedRank(a: number[], b: number[]): TestResult;
export declare function cohensD(a: number[], b: number[]): number;
export declare class ELORating {
    private ratings;
    private readonly K;
    private initialRating;
    constructor(k?: number, initialRating?: number);
    register(id: string): void;
    recordMatch(idA: string, idB: string, scoreA: number): void;
    getRating(id: string): number;
    getLeaderboard(): Array<{
        id: string;
        elo: number;
    }>;
}
//# sourceMappingURL=statistics.d.ts.map