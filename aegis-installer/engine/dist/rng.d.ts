/**
 * AEGIS — Seeded PRNG (Xoshiro256**)
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Deterministic random number generation for reproducible runs.
 * Every strategy, every mutation, every sample — all from a single seed.
 */
/**
 * Xoshiro256** — fast, high-quality 64-bit PRNG.
 * Seeded with SplitMix64 for initialization.
 */
export declare class SeededRNG {
    private s;
    readonly seed: number;
    constructor(seed?: number);
    private initFromSeed;
    private rotl;
    private nextU64;
    /** Return uniform random float in [0, 1) */
    random(): number;
    /** Return uniform random float in [min, max) */
    range(min: number, max: number): number;
    /** Return random integer in [min, max] inclusive */
    int(min: number, max: number): number;
    /** Return random normal (Box-Muller transform) */
    normal(mean?: number, stddev?: number): number;
    /** Shuffle array in-place (Fisher-Yates) */
    shuffle<T>(arr: T[]): T[];
    /** Pick a random element */
    pick<T>(arr: T[]): T;
    /** Fork a child RNG with a derived seed */
    fork(): SeededRNG;
}
//# sourceMappingURL=rng.d.ts.map