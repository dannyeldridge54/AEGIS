# GIMPS software, how it is built, and how our engine maps onto it (21 Nov 2026)
**Sources read (downloaded; nothing built or run):**
- PRPLL (gpuowl) at commit 4d0e759 (14 Dec 2025): the GPU PRP/LL tester. 24.5k lines, OpenCL.
- mfaktc (primesearch): the CUDA trial-factoring program.
- mersenne.org (Prime95/mprime) is blocked from this cloud, so it was not read.

## The real pipeline: 5 layers plus a referee

| Layer | Program | What it does | Key structure |
|---|---|---|---|
| L0 assign | PrimeNet | hands out exponents so no work is duplicated | central ledger |
| L1 TF | mfaktc (CUDA) / mfakto (OpenCL) | tries factors q = 2kp+1 | **wheel of 420 or 4620 classes** (4·3·5·7·11). Only 96 of 420 classes can hold factors (q ≡ ±1 mod 8, not divisible by 3, 5 or 7), so 77% of the k space is skipped outright. Each class is sieved on the GPU by 25,000 to 200,000 small primes, then 2^p mod q uses 95-bit integer kernels. Bit level by bit level (our "layers"), with a checkpoint per class. A self-test of 2,924 known factors runs before any work is trusted. |
| L2 P−1 | PRPLL / Prime95 | stage 1 (B1) and stage 2 (B2) | bounds chosen to maximise expected tests saved |
| L3 PRP | PRPLL (GPU) | x ← x² mod M_p, p times, from 3 | **IBDWT FFT** (Crandall–Fagin): mod 2^p−1 comes free through irrational-base weights. About 18–19 bits per FFT word, so p ≈ 1.4e8 needs an FFT of about 7.5M words. The FFT shape (e.g. 1K:15:256) is chosen per exponent from a measured bits-per-word table. **Per-GPU tuning** (`-tune`, tune.txt) is the hardware-adaptive layer. |
| Inline referee | PRPLL | **Gerbicz check**: blocks of 200 to 1000 squarings, verified every 40k to 1M iterations | a failed check rolls back to the last good state and halves the check step. Hardware errors cannot pass silently. |
| Centre referee | PrimeNet "cert" | **Pietrzak proof** (power 8–10) written alongside the PRP result | another machine verifies the whole test at about 1/2^power of its cost. This replaced full double-checks. |
| Final referee | LL on different hardware and software | only for a found prime | independent proof |

## The economics: why it is so hard
All arithmetic was done in code.
- Prior chance that M_p is prime at p ≈ 1.4e8: 3.6–3.8e-7 (Wagstaff/LPW). After TF to 2^77 that rises to about 1.0e-6 per PRP test.
- PRPLL's own tune.txt gives 936 µs per iteration at p ≈ 1.41e8. That is **about 36 h per test** on the author's tuning GPU (model not stated).
- So the expectation is about 1e6 tests per new prime: **about 4,000 GPU-years on one such GPU.** The 2024 find used thousands of cloud GPUs (Durant).

## What this means for our engine (the plan; nothing run)
1. **Use the one real structure.** It is the factor law q = 2kp+1, q ≡ ±1 (mod 8), and the wheel of classes is that law done properly. Our D2005 N2 tested every k with only the mod-8 rule. Next: adopt the 420/4620-class wheel and a small-prime sieve. That is the same layer law, filtered better; expect roughly 4–10× on N2.
2. **The layer depth is economic, not fixed.** Stop TF at bit b once P(factor in [2^b, 2^(b+1))) ≈ 1/b × (PRP cost saved) falls below that layer's cost, which doubles per bit. This replaces the locked b_max rule in a future lock (via DEVIATIONS, before any rerun).
3. **Referee in the centre** = Gerbicz-style block checks on every long squaring chain, plus an independent LL on any hit. This is the same design as our Loom detector persistence (D1996).
4. **Hardware adaptation** = PRPLL's per-GPU tune and bits-per-word table, plus our core/RAM detection (cm_ramsey.py). On Danny's PC, the GPU vendor decides the programs: NVIDIA → mfaktc + PRPLL; AMD → mfakto + PRPLL.
5. **What we can't beat:** PRPLL's FFT core is the state of the art. Our edge is orchestration, which means:
   - choosing work (layer economics);
   - triangulated refereeing;
   - logging into the target table.

   It does not mean a faster squaring.
6. **Honest scope:** one PC cannot expect a find; the expectation is 1e-6 per test. Joining PrimeNet makes each test count toward GIMPS and qualifies for the $3,000 award. That needs Danny's account; we never type passwords.

## Danny's PC (RTX 4070): every part wired in (21 Nov 2026, plan only, nothing installed)
**Key fact.** The 4070 (Ada, sm_89) is a consumer card. Its FP64 rate is 1/64 of FP32, so a classic FP64 FFT PRP test is slow on it. Two findings from the source:
- mfaktc's current Makefile builds for sm_89 (Ada). TF is pure integer work, which is the 4070's strength.
- **PRPLL (Dec 2025) adds transforms that avoid FP64:**
  - integer NTTs mod M31 = 2³¹−1 and M61 = 2⁶¹−1;
  - FP32 + NTT hybrids (FFT32, FFT3161, FFT3261, FFT323161; see Task.cpp and FFTConfig.cpp).

  These put the 4070's FP32 and INT32 units to work on the PRP itself. Which transform is fastest on this card is unmeasured; PRPLL `-tune` decides.

| Part | Job | Why |
|---|---|---|
| GPU INT32 cores | mfaktc trial factoring (L1) | integer work, no FP64 needed |
| GPU FP32 + INT units | PRPLL PRP with FP32/M31/M61 transforms (L3) | the transforms built for weak-FP64 cards |
| GPU 12 GB VRAM | PRPLL FFT buffers (~7.5M words at p ≈ 1.4e8) plus the mfaktc sieve | fits with room |
| CPU cores (AVX2) | Prime95/mprime: P−1 (L2) and an optional CPU PRP worker | CPU FP64 is full-rate, so it is a real second tester |
| System RAM | **P−1 stage 2**: Prime95 uses as much RAM as allowed (more RAM gives a bigger B2 and more factors found) | the one GIMPS step that scales directly with RAM |
| SSD | PRP checkpoints plus the Pietrzak proof temp files (several GB at power 9–10) | a proof makes the result certifiable |
| Network | PrimeNet: assignments, results, certs | prevents duplicate work; counts for the award |
| Tensor cores | **cannot do exact big-integer squaring** (low precision). Could run CubeMind's local LLM (Ollama) as orchestrator and log reader | would compete with mfaktc for the GPU, so it should run only between work units |
| Loom / CubeMind | referee and scheduler: picks TF depth by layer economics, watches Gerbicz/residue logs, logs to the target table | our part of the stack |

**Wiring rule.** No two heavy jobs on the same unit:
- GPU: mfaktc **or** PRPLL, scheduled;
- CPU: Prime95 P−1, plus one core left for the Loom;
- the LLM runs only when the GPU is idle.
