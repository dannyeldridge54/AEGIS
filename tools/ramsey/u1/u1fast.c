// U1 fast (D2020): for each (3,8,27)-graph D (graph6 on stdin), count/print 6-tuples A1<=..<=A6 of independent sets (|A| 5..7) such that
// H = D + v + w1..w6 has alpha(H) <= M (M = 8 for (3,9,34)) and max degree <= M. Condition: every independent j-set of D is missed by at
// most M-j of the A's. Pruning: miss-bitsets; pairs must jointly hit every set with M-j = 1 (j = M-1), etc.  Usage: u1fast M [maxD] [print]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t U; typedef uint64_t W;
static U adj[32]; static int n, M = 8;
#define MAXC 20000
#define MAXS 8192
static U S[10][MAXS]; static int ns[10];                     // independent sets of size j (3..M-1)
static U C[MAXC]; static int nc;                             // candidates |A| in 5..M-1
static W *miss[10]; static int nw[10];                       // miss[j][c*nw+w]: bit s set if C[c] misses S[j][s]
static int dD[32]; static long long sols; static int PRINT, ch[6];
static void enumI(U mask, int size, U cur, int start) {
  if (size >= 3 && size <= M - 1 && ns[size] < MAXS) S[size][ns[size]++] = cur;
  if (size >= 5 && size <= M - 1 && nc < MAXC) C[nc++] = cur;
  if (size >= M - 1) return;
  for (int v = start; v < n; v++) if (mask >> v & 1) enumI(mask & ~adj[v] & ~((1u << (v + 1)) - 1), size + 1, cur | (1u << v), v + 1);
}
static int okset(int j, int k) {   // every j-set missed by at most M-j of ch[0..k-1]: equivalently no (M-j+1)-subset of ch all miss a set
  int r = M - j + 1; if (r > k) return 1;
  int w = nw[j]; static int idx[8];
  for (int t = 0; t < r; t++) idx[t] = t;
  while (1) {   // only test subsets that contain the newest element ch[k-1]
    if (idx[r - 1] == k - 1) {
      for (int q = 0; q < w; q++) { W x = ~0ULL; for (int t = 0; t < r; t++) x &= miss[j][(long)ch[idx[t]] * w + q]; if (x) return 0; }
    }
    int t = r - 1; while (t >= 0 && idx[t] == k - r + t) t--; if (t < 0) break; idx[t]++; for (int u = t + 1; u < r; u++) idx[u] = idx[u - 1] + 1;
  }
  return 1;
}
static int capok(int k) { int c[32] = {0}; for (int a = 0; a < k; a++) { U x = C[ch[a]]; while (x) { int u = __builtin_ctz(x); x &= x - 1; if (dD[u] + (++c[u]) > M) return 0; } } return 1; }
static void rec(int k, int from) {
  if (k == 6) { sols++; if (PRINT) { for (int a = 0; a < 6; a++) printf("%x ", C[ch[a]]); printf("\n"); } return; }
  for (int c = from; c < nc; c++) { ch[k] = c; if (!capok(k + 1)) continue;
    int ok = 1; for (int j = M - 1; j >= 3 && ok; j--) ok = okset(j, k + 1);
    if (ok) rec(k + 1, c); }
}
int main(int argc, char **argv) {
  M = atoi(argv[1]); long maxD = argc > 2 ? atol(argv[2]) : 1000000000L; PRINT = argc > 3; char line[512]; long nd = 0, withsol = 0; long long total = 0;
  for (int j = 0; j < 10; j++) miss[j] = malloc(sizeof(W) * (long)MAXC * (MAXS / 64));
  while (nd < maxD && fgets(line, sizeof line, stdin)) {
    n = line[0] - 63; memset(adj, 0, sizeof adj); int bit = 0, k = 1;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { int c = line[k + bit / 6] - 63; if (c >> (5 - bit % 6) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; } bit++; }
    for (int i = 0; i < n; i++) dD[i] = __builtin_popcount(adj[i]);
    for (int j = 0; j < 10; j++) ns[j] = 0; nc = 0; enumI((1u << n) - 1, 0, 0, 0);
    for (int j = 3; j <= M - 1; j++) { nw[j] = (ns[j] + 63) / 64; memset(miss[j], 0, sizeof(W) * (long)nc * nw[j]);
      for (int c = 0; c < nc; c++) for (int s = 0; s < ns[j]; s++) if (!(C[c] & S[j][s])) miss[j][(long)c * nw[j] + s / 64] |= 1ULL << (s % 64); }
    sols = 0; rec(0, 0); nd++; total += sols; if (sols) withsol++;
    if (PRINT) printf("# D %ld: cand %d S7 %d S6 %d sols %lld\n", nd, nc, ns[7], ns[6], sols);
    if (nd % 1000 == 0) { fprintf(stderr, "progress %ld D, %ld with solutions, %lld tuples\n", nd, withsol, total); }
  }
  fprintf(stderr, "M=%d D graphs %ld, with solutions %ld, total 6-tuples %lld\n", M, nd, withsol, total); return 0;
}
