// D2018: exhaustive Cayley search. Usage: cay <table> <K> [maxdeg] [mindeg]. Finds inverse-closed triangle-free S, mindeg<=|S|<=maxdeg,
// maximal under the size cap; reports min alpha; prints any S with alpha < K (a (3,K)-graph witness).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t U; int n, K, MAXD = 9, MIND = 5, T[64][64], inv[64], ncls, cls[64][2], csz[64];
int inS[64]; long long leaves = 0, checked = 0; int bestalpha = 99;
static int best;
static void arec(U *adj, int size, U cand) {
  if (best >= K) return;
  if (size + __builtin_popcountll(cand) <= best) return;
  if (!cand) { best = size; return; }
  int v = __builtin_ctzll(cand);
  arec(adj, size + 1, cand & ~adj[v] & ~(1ULL << v)); arec(adj, size, cand & ~(1ULL << v));
}
static int alpha(void) { U adj[64]; for (int a = 0; a < n; a++) { adj[a] = 0; for (int s = 0; s < n; s++) if (inS[s]) adj[a] |= 1ULL << T[a][s]; }
  best = 0; arec(adj, 0, n == 64 ? ~0ULL : ((1ULL << n) - 1)); return best; }
static int ok_add(int c) {   // adding class c keeps triangle-free: no a,b in S' with a*b in S'
  int add[2], na = csz[c]; add[0] = cls[c][0]; add[1] = cls[c][1];
  for (int i = 0; i < na; i++) inS[add[i]] = 1;
  int ok = 1, el[64], m = 0; for (int b = 0; b < n; b++) if (inS[b]) el[m++] = b;   // check every pair of S' (|S'| <= 9)
  for (int i = 0; i < m && ok; i++) for (int j = 0; j < m && ok; j++) if (inS[T[el[i]][el[j]]]) ok = 0;
  for (int i = 0; i < na; i++) inS[add[i]] = 0;
  return ok;
}
static void setc(int c, int v) { for (int i = 0; i < csz[c]; i++) inS[cls[c][i]] = v; }
static void dfs(int c, int size) {
  if (c == ncls) {
    // maximality under the cap: no class could be added (triangle or size)
    for (int d = 0; d < ncls; d++) if (!inS[cls[d][0]] && size + csz[d] <= MAXD && ok_add(d)) return;
    leaves++; if (size < MIND) return;
    checked++; int al = alpha(); if (al < bestalpha) bestalpha = al;
    if (al < K) { printf("WITNESS |S|=%d alpha=%d S=", size, al); for (int s = 0; s < n; s++) if (inS[s]) printf("%d ", s); printf("\n"); fflush(stdout); }
    return;
  }
  if (size + csz[c] <= MAXD && ok_add(c)) { setc(c, 1); dfs(c + 1, size + csz[c]); setc(c, 0); }
  dfs(c + 1, size);
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); K = atoi(argv[2]); if (argc > 3) MAXD = atoi(argv[3]); if (argc > 4) MIND = atoi(argv[4]);
  if (fscanf(f, "%d", &n) != 1) return 1; for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (fscanf(f, "%d", &T[a][b]) != 1) return 1;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (T[a][b] == 0) inv[a] = b;
  int seen[64] = {0}; ncls = 0;
  for (int a = 1; a < n; a++) if (!seen[a]) { seen[a] = seen[inv[a]] = 1; cls[ncls][0] = a; cls[ncls][1] = inv[a]; csz[ncls] = (inv[a] == a) ? 1 : 2; if (T[a][a] == 0) csz[ncls] = 1; ncls++; }
  for (int c = 0; c < ncls; c++) if (T[cls[c][0]][cls[c][0]] == cls[c][0]) {}   // (a*a=a only for identity)
  dfs(0, 0);
  printf("%s K=%d classes=%d maximal_leaves=%lld checked=%lld min_alpha=%d\n", argv[1], K, ncls, leaves, checked, bestalpha);
  return 0;
}
