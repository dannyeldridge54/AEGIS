// U1 v3 (D2020): 6-tuples as cliques in the pair-compatibility graph. Pair (a,b) compatible iff no independent (M-1)-set of D is missed by
// both (the "missed by at most 1" rule), plus the degree cap on the pair. Triples are then checked for (M-2)-sets, and the full 6-tuple
// for all smaller sets. Repeats (twins, A_a = A_b) are allowed (a == b allowed when the set is self-compatible).  Usage: u1clq M [maxD] [print]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t U; typedef uint64_t W;
static U adj[32]; static int n, M = 8;
#define MAXC 12000
#define MAXS 8192
static U S[10][MAXS]; static int ns[10]; static U C[MAXC]; static int nc, nwc; static W *miss[10]; static int nw[10]; static int dD[32];
static W *cg;   // compatibility bitsets nc x nwc
static long CURD, OFFSET = 0; static long long sols; static int PRINT, ch[6];
static void enumI(U mask, int size, U cur, int start) {
  if (size >= 3 && size <= M - 1 && ns[size] < MAXS) S[size][ns[size]++] = cur;
  if (size >= 5 && size <= M - 1 && nc < MAXC) C[nc++] = cur;
  if (size >= M - 1) return;
  for (int v = start; v < n; v++) if (mask >> v & 1) enumI(mask & ~adj[v] & ~((1u << (v + 1)) - 1), size + 1, cur | (1u << v), v + 1);
}
static int allmiss(int j, int *idx, int r) { int w = nw[j]; for (int q = 0; q < w; q++) { W x = ~0ULL; for (int t = 0; t < r; t++) x &= miss[j][(long)idx[t] * w + q]; if (x) return 1; } return 0; }
static int okset_new(int j, int k) {   // subsets of size r = M-j+1 containing the newest element
  int r = M - j + 1; if (r > k || r < 1) return 1; int sub[8], pos[8];
  for (int t = 0; t < r - 1; t++) pos[t] = t;
  while (1) { for (int t = 0; t < r - 1; t++) sub[t] = ch[pos[t]]; sub[r - 1] = ch[k - 1]; if (allmiss(j, sub, r)) return 0;
    int t = r - 2; while (t >= 0 && pos[t] == (k - 1) - (r - 1) + t) t--; if (t < 0) break; pos[t]++; for (int u = t + 1; u < r - 1; u++) pos[u] = pos[u - 1] + 1; }
  return 1;
}
static int capok(int k) { int c[32] = {0}; for (int a = 0; a < k; a++) { U x = C[ch[a]]; while (x) { int u = __builtin_ctz(x); x &= x - 1; if (dD[u] + (++c[u]) > M) return 0; } } return 1; }
static void rec(int k, W *P) {   // P = candidates compatible with all chosen, with index >= last
  if (k == 6) { if (!okset_new(M - 3, 6)) return; for (int j = M - 4; j >= 3; j--) for (int s = 0; s < ns[j]; s++) { int miss_ = 0; for (int a = 0; a < 6; a++) if (!(C[ch[a]] & S[j][s])) miss_++; if (miss_ > M - j) return; } sols++; { printf("SOL D=%ld", CURD); for (int a = 0; a < 6; a++) printf(" %x", C[ch[a]]); printf("\n"); } return; }
  W Q[MAXC / 64 + 1];
  for (int q = 0; q < nwc; q++) { W x = P[q]; while (x) { int c = q * 64 + __builtin_ctzll(x); x &= x - 1;
      ch[k] = c; if (!capok(k + 1)) continue;
      int ok = okset_new(M - 2, k + 1) && okset_new(M - 3, k + 1);   // j = M-1 via the pair graph; j <= M-4 at the leaf
      if (!ok) continue;
      for (int t = 0; t < nwc; t++) Q[t] = P[t] & cg[(long)c * nwc + t];
      for (int t = 0; t < q; t++) Q[t] = 0; Q[q] &= ~((c % 64 == 0) ? 0ULL : ((1ULL << (c % 64)) - 1));   // keep indices >= c (repeats allowed)
      rec(k + 1, Q); } }
}
int main(int argc, char **argv) {
  setvbuf(stdout, NULL, _IOLBF, 0); M = atoi(argv[1]); if (getenv("OFFSET")) OFFSET = atol(getenv("OFFSET")); long maxD = argc > 2 ? atol(argv[2]) : 1000000000L; PRINT = argc > 3; char line[512]; long nd = 0, withsol = 0; long long total = 0;
  for (int j = 0; j < 10; j++) miss[j] = malloc(sizeof(W) * (long)MAXC * (MAXS / 64)); cg = malloc(sizeof(W) * (long)MAXC * (MAXC / 64 + 1));
  while (nd < maxD && fgets(line, sizeof line, stdin)) {
    n = line[0] - 63; memset(adj, 0, sizeof adj); int bit = 0, k = 1;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { int c = line[k + bit / 6] - 63; if (c >> (5 - bit % 6) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; } bit++; }
    for (int i = 0; i < n; i++) dD[i] = __builtin_popcount(adj[i]);
    for (int j = 0; j < 10; j++) ns[j] = 0; nc = 0; enumI((1u << n) - 1, 0, 0, 0); nwc = (nc + 63) / 64;
    for (int j = M - 3; j <= M - 1; j++) { nw[j] = (ns[j] + 63) / 64; memset(miss[j], 0, sizeof(W) * (long)nc * nw[j]);
      for (int c = 0; c < nc; c++) for (int s = 0; s < ns[j]; s++) if (!(C[c] & S[j][s])) miss[j][(long)c * nw[j] + s / 64] |= 1ULL << (s % 64); }
    memset(cg, 0, sizeof(W) * (long)nc * nwc); long pairs = 0;
    for (int a = 0; a < nc; a++) for (int b = a; b < nc; b++) {
      int idx[2] = {a, b}; if (allmiss(M - 1, idx, 2)) continue;
      U ov = C[a] & C[b]; int bad = 0; while (ov) { int u = __builtin_ctz(ov); ov &= ov - 1; if (dD[u] + 2 > M) { bad = 1; break; } } if (bad) continue;
      cg[(long)a * nwc + b / 64] |= 1ULL << (b % 64); cg[(long)b * nwc + a / 64] |= 1ULL << (a % 64); pairs++; }
    CURD = nd + OFFSET; W P[MAXC / 64 + 1]; for (int q = 0; q < nwc; q++) P[q] = 0; for (int c = 0; c < nc; c++) P[c / 64] |= 1ULL << (c % 64);
    sols = 0; rec(0, P); nd++; total += sols; if (sols) withsol++;
    if (PRINT) printf("# D %ld: cand %d pairs %ld sols %lld\n", nd, nc, pairs, sols);
    if (nd % 1000 == 0) fprintf(stderr, "progress %ld D, %ld with solutions, %lld tuples\n", nd, withsol, total);
  }
  fprintf(stderr, "M=%d D graphs %ld, with solutions %ld, total 6-tuples %lld\n", M, nd, withsol, total); return 0;
}
