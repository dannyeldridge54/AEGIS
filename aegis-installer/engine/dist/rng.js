"use strict";
/**
 * AEGIS — Seeded PRNG (Xoshiro256**)
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Deterministic random number generation for reproducible runs.
 * Every strategy, every mutation, every sample — all from a single seed.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.SeededRNG = void 0;
/**
 * Xoshiro256** — fast, high-quality 64-bit PRNG.
 * Seeded with SplitMix64 for initialization.
 */
class SeededRNG {
    constructor(seed) {
        this.seed = seed ?? Math.floor(Math.random() * 2 ** 32);
        this.s = new BigInt64Array(4);
        this.initFromSeed(this.seed);
    }
    initFromSeed(seed) {
        let s = BigInt(seed) & 0xffffffffffffffffn;
        for (let i = 0; i < 4; i++) {
            s = (s + 0x9e3779b97f4a7c15n) & 0xffffffffffffffffn;
            let z = s;
            z = ((z ^ (z >> 30n)) * 0xbf58476d1ce4e5b9n) & 0xffffffffffffffffn;
            z = ((z ^ (z >> 27n)) * 0x94d049bb133111ebn) & 0xffffffffffffffffn;
            z = z ^ (z >> 31n);
            this.s[i] = z;
        }
        if (this.s.every(v => v === 0n))
            this.s[0] = 1n;
    }
    rotl(x, k) {
        return ((x << k) | (x >> (64n - k))) & 0xffffffffffffffffn;
    }
    nextU64() {
        const result = (this.rotl((this.s[1] * 5n) & 0xffffffffffffffffn, 7n) * 9n) & 0xffffffffffffffffn;
        const t = (this.s[1] << 17n) & 0xffffffffffffffffn;
        this.s[2] ^= this.s[0];
        this.s[3] ^= this.s[1];
        this.s[1] ^= this.s[2];
        this.s[0] ^= this.s[3];
        this.s[2] ^= t;
        this.s[3] = this.rotl(this.s[3], 45n);
        return result;
    }
    /** Return uniform random float in [0, 1) */
    random() {
        const u = this.nextU64();
        const mantissa = Number((u >> 11n) & 0x1fffffffffffffn);
        return mantissa / (2 ** 53);
    }
    /** Return uniform random float in [min, max) */
    range(min, max) {
        return min + this.random() * (max - min);
    }
    /** Return random integer in [min, max] inclusive */
    int(min, max) {
        return Math.floor(this.range(min, max + 1));
    }
    /** Return random normal (Box-Muller transform) */
    normal(mean = 0, stddev = 1) {
        const u1 = this.random();
        const u2 = this.random();
        const z = Math.sqrt(-2 * Math.log(u1 || 1e-15)) * Math.cos(2 * Math.PI * u2);
        return mean + z * stddev;
    }
    /** Shuffle array in-place (Fisher-Yates) */
    shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = this.int(0, i);
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }
    /** Pick a random element */
    pick(arr) {
        return arr[this.int(0, arr.length - 1)];
    }
    /** Fork a child RNG with a derived seed */
    fork() {
        return new SeededRNG(Number(this.nextU64() & 0x7fffffffn));
    }
}
exports.SeededRNG = SeededRNG;
//# sourceMappingURL=rng.js.map