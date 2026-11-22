// D2002: exhaustive gluing of v + w1..w4 onto H = C35(1,7,11,16) for a (3,K,40)-graph with deg(v)=4.
// Usage: glue4 run <part> <nparts> [K]     -> exhaustive search (A1 contains vertex 0), prints solutions as 4 masks
//        glue4 test <trials> <K> <seed>    -> random disjoint A's: prints "ACC|REJ g6" for checking against verify.py
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; static int n = 35, K = 10; static u64 adj[64];
static u64 *C, *F8, *F7, *F6; static int nC = 0, n8 = 0, n7 = 0, n6 = 0, W8;
static u64 *H8;   // hit8 bitsets
static void rec(u64 cand, u64 cur, int k){
  if (k >= 3 && k <= 8) C[nC++] = cur;
  if (k == 8) F8[n8++] = cur; if (k == 7) F7[n7++] = cur; if (k == 6) F6[n6++] = cur;
  while (cand){ int v = __builtin_ctzll(cand); cand &= cand - 1; rec(cand & ~adj[v], cur | (1ULL << v), k + 1); } }
static int okK(u64 *A){   // hit-count thresholds for alpha(G) <= K-1: j-set missed by <= K-1-j of the 4 sets
  u64 *F[3] = {F8, F7, F6}; int nF[3] = {n8, n7, n6}, j[3] = {8, 7, 6};
  for (int t = 0; t < 3; t++){ int maxmiss = K - 1 - j[t]; if (maxmiss >= 4) continue;
    for (int i = 0; i < nF[t]; i++){ int miss = 0; for (int a = 0; a < 4; a++) miss += (F[t][i] & A[a]) == 0; if (miss > maxmiss) return 0; } }
  // sets of size <= 5 can only matter if K-1-j < 4, i.e. j > K-5: for K=10 never; for K=11 never
  return 1; }
static void g6(u64 *A){   // vertices 0..34 = H, 35 = v, 36..39 = w1..w4
  static u64 G[64]; int N = 40; memset(G, 0, sizeof G);
  for (int i = 0; i < 35; i++) G[i] = adj[i];
  for (int a = 0; a < 4; a++){ int w = 36 + a; G[35] |= 1ULL << w; G[w] |= 1ULL << 35; u64 t = A[a]; while (t){ int h = __builtin_ctzll(t); t &= t - 1; G[w] |= 1ULL << h; G[h] |= 1ULL << w; } }
  int bits[2000], nb = 0; for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) bits[nb++] = (G[i] >> j) & 1;
  putchar(N + 63); for (int i = 0; i < nb; i += 6){ int x = 0; for (int b = 0; b < 6; b++) x = (x << 1) | (i + b < nb ? bits[i + b] : 0); putchar(x + 63); } putchar('\n'); }
static u64 rs; static u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv){
  int S[4] = {1, 7, 11, 16}; for (int v = 0; v < n; v++) for (int i = 0; i < 4; i++){ adj[v] |= 1ULL << ((v + S[i]) % n); adj[v] |= 1ULL << ((v - S[i] + n) % n); }
  C = malloc(sizeof(u64) * 80000); F8 = malloc(sizeof(u64) * 4000); F7 = malloc(sizeof(u64) * 15000); F6 = malloc(sizeof(u64) * 25000);
  rec((1ULL << n) - 1, 0, 0); if (argc > 4 && !strcmp(argv[1], "run")) K = atoi(argv[4]);
  fprintf(stderr, "candidates %d, F8 %d, F7 %d, F6 %d\n", nC, n8, n7, n6);
  if (!strcmp(argv[1], "test")){ int T = atoi(argv[2]); K = atoi(argv[3]); rs = strtoull(argv[4], 0, 10) * 2654435761ULL + 7;
    for (int t = 0; t < T; t++){ u64 A[4]; u64 used = 0; int a = 0, guard = 0;
      while (a < 4 && guard++ < 100000){ u64 c = C[rnd() % nC]; if (c & used) continue; A[a++] = c; used |= c; }
      if (a < 4) { t--; continue; } int mk = 0; for (int kk = 9; kk <= 14 && !mk; kk++){ K = kk; if (okK(A)) mk = kk; } K = atoi(argv[3]); printf("MINK %d ", mk); g6(A); } return 0; }
  int part = atoi(argv[2]), np = atoi(argv[3]); W8 = (n8 + 63) / 64; H8 = calloc((size_t)nC * W8, sizeof(u64));
  for (int c = 0; c < nC; c++) for (int i = 0; i < n8; i++) if (F8[i] & C[c]) H8[(size_t)c * W8 + i / 64] |= 1ULL << (i % 64);
  u64 FULL[64]; for (int w = 0; w < W8; w++) FULL[w] = ~0ULL; if (n8 % 64) FULL[W8 - 1] = (1ULL << (n8 % 64)) - 1;
  int *P = malloc(sizeof(int) * nC); long long sols = 0, a1s = 0, pairs = 0;
  int pair8 = (K - 1 - 8) < 2;   // pairs must jointly hit all 8-sets iff an 8-set may be missed by at most 1
  for (int i1 = 0; i1 < nC; i1++){ if (!(C[i1] & 1ULL)) continue; if ((a1s++ % np) != part) continue;
    int np_ = 0; u64 *h1 = H8 + (size_t)i1 * W8;
    for (int c = 0; c < nC; c++){ if (c == i1 || (C[c] & C[i1]) || (C[c] & 1ULL)) continue;
      if (pair8){ u64 *h = H8 + (size_t)c * W8; int ok = 1; for (int w = 0; w < W8 && ok; w++) if ((h1[w] | h[w]) != FULL[w]) ok = 0; if (!ok) continue; }
      P[np_++] = c; }
    pairs += np_;
    for (int x = 0; x < np_; x++) for (int y = x + 1; y < np_; y++){ int c2 = P[x], c3 = P[y]; if (C[c2] & C[c3]) continue;
      if (pair8){ u64 *ha = H8 + (size_t)c2 * W8, *hb = H8 + (size_t)c3 * W8; int ok = 1; for (int w = 0; w < W8 && ok; w++) if ((ha[w] | hb[w]) != FULL[w]) ok = 0; if (!ok) continue; }
      for (int z = y + 1; z < np_; z++){ int c4 = P[z]; if ((C[c4] & C[c2]) || (C[c4] & C[c3])) continue;
        if (pair8){ u64 *hc = H8 + (size_t)c4 * W8, *ha = H8 + (size_t)c2 * W8, *hb = H8 + (size_t)c3 * W8; int ok = 1;
          for (int w = 0; w < W8 && ok; w++) if ((hc[w] | ha[w]) != FULL[w] || (hc[w] | hb[w]) != FULL[w]) ok = 0; if (!ok) continue; }
        u64 A[4] = {C[i1], C[c2], C[c3], C[c4]};
        if (okK(A)){ sols++; printf("SOL %llx %llx %llx %llx ", (unsigned long long)A[0], (unsigned long long)A[1], (unsigned long long)A[2], (unsigned long long)A[3]); g6(A); fflush(stdout); } } }
    if (a1s % 200 == 0) fprintf(stderr, "part %d: A1 #%lld, partners last %d, sols %lld\n", part, a1s, np_, sols); }
  fprintf(stderr, "part %d DONE: A1 sets %lld, partner pairs %lld, solutions %lld\n", part, a1s, pairs, sols); return 0; }
