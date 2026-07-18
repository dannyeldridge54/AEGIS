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
export class SeededRNG {
  private s: BigInt64Array;
  readonly seed: number;

  constructor(seed?: number) {
    this.seed = seed ?? Math.floor(Math.random() * 2 ** 32);
    this.s = new BigInt64Array(4);
    this.initFromSeed(this.seed);
  }

  private initFromSeed(seed: number): void {
    let s = BigInt(seed) & 0xFFFFFFFFFFFFFFFFn;
    for (let i = 0; i < 4; i++) {
      s = (s + 0x9E3779B97F4A7C15n) & 0xFFFFFFFFFFFFFFFFn;
      let z = s;
      z = ((z ^ (z >> 30n)) * 0xBF58476D1CE4E5B9n) & 0xFFFFFFFFFFFFFFFFn;
      z = ((z ^ (z >> 27n)) * 0x94D049BB133111EBn) & 0xFFFFFFFFFFFFFFFFn;
      z = z ^ (z >> 31n);
      this.s[i] = z;
    }
    if (this.s.every(v => v === 0n)) this.s[0] = 1n;
  }

  private rotl(x: bigint, k: bigint): bigint {
    return ((x << k) | (x >> (64n - k))) & 0xFFFFFFFFFFFFFFFFn;
  }

  private nextU64(): bigint {
    const result = (this.rotl((this.s[1] * 5n) & 0xFFFFFFFFFFFFFFFFn, 7n) * 9n) & 0xFFFFFFFFFFFFFFFFn;
    const t = (this.s[1] << 17n) & 0xFFFFFFFFFFFFFFFFn;
    this.s[2] ^= this.s[0];
    this.s[3] ^= this.s[1];
    this.s[1] ^= this.s[2];
    this.s[0] ^= this.s[3];
    this.s[2] ^= t;
    this.s[3] = this.rotl(this.s[3], 45n);
    return result;
  }

  /** Return uniform random float in [0, 1) */
  random(): number {
    const u = this.nextU64();
    const mantissa = Number((u >> 11n) & 0x1FFFFFFFFFFFFFn);
    return mantissa / (2 ** 53);
  }

  /** Return uniform random float in [min, max) */
  range(min: number, max: number): number {
    return min + this.random() * (max - min);
  }

  /** Return random integer in [min, max] inclusive */
  int(min: number, max: number): number {
    return Math.floor(this.range(min, max + 1));
  }

  /** Return random normal (Box-Muller transform) */
  normal(mean: number = 0, stddev: number = 1): number {
    const u1 = this.random();
    const u2 = this.random();
    const z = Math.sqrt(-2 * Math.log(u1 || 1e-15)) * Math.cos(2 * Math.PI * u2);
    return mean + z * stddev;
  }

  /** Shuffle array in-place (Fisher-Yates) */
  shuffle<T>(arr: T[]): T[] {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = this.int(0, i);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  /** Pick a random element */
  pick<T>(arr: T[]): T {
    return arr[this.int(0, arr.length - 1)];
  }

  /** Fork a child RNG with a derived seed */
  fork(): SeededRNG {
    return new SeededRNG(Number(this.nextU64() & 0x7FFFFFFFn));
  }
}
