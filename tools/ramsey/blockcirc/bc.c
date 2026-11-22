// D2019 block-circulant search. Usage: bc B m K [maxdeg mindeg]. Vertices v = b*m + i. Orbits: within (b, d), cross (b<b', t).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t U; int B, m, n, K, MAXD = 9, MIND = 5, no; int ob[400], ob2[400], od[400], deg[64], on[400]; U adj[64];
long long leaves = 0, checked = 0, nodes = 0; int minalpha = 99, best;
static void arec(int size, U cand) { if (best >= K) return; if (size + __builtin_popcountll(cand) <= best) return; if (!cand) { best = size; return; }
  int v = __builtin_ctzll(cand); arec(size + 1, cand & ~adj[v] & ~(1ULL << v)); arec(size, cand & ~(1ULL << v)); }
static int edge_list(int o, int *eu, int *ev) {   // edges of orbit o
  int k = 0;
  for (int i = 0; i < m; i++) {
    int u = ob[o] * m + i, v;
    if (ob[o] == ob2[o]) { v = ob[o] * m + (i + od[o]) % m; if (2 * od[o] == m && i >= m / 2) continue; }
    else v = ob2[o] * m + (i + od[o]) % m;
    eu[k] = u; ev[k] = v; k++;
  }
  return k;
}
static int dinc(int o, int b) { if (ob[o] == ob2[o]) return (ob[o] == b) ? ((2 * od[o] == m) ? 1 : 2) : 0; return (ob[o] == b || ob2[o] == b) ? 1 : 0; }
static int can_add(int o) {
  for (int b = 0; b < B; b++) if (deg[b] + dinc(o, b) > MAXD) return 0;
  int eu[64], ev[64], k = edge_list(o, eu, ev); U a2[64]; for (int v = 0; v < n; v++) a2[v] = adj[v];
  for (int j = 0; j < k; j++) { if (a2[eu[j]] & a2[ev[j]]) return 0; a2[eu[j]] |= 1ULL << ev[j]; a2[ev[j]] |= 1ULL << eu[j]; }
  for (int j = 0; j < k; j++) if (a2[eu[j]] & a2[ev[j]]) return 0;
  return 1;
}
static void toggle(int o, int on_) { int eu[64], ev[64], k = edge_list(o, eu, ev);
  for (int j = 0; j < k; j++) { if (on_) { adj[eu[j]] |= 1ULL << ev[j]; adj[ev[j]] |= 1ULL << eu[j]; } else { adj[eu[j]] &= ~(1ULL << ev[j]); adj[ev[j]] &= ~(1ULL << eu[j]); } }
  for (int b = 0; b < B; b++) deg[b] += on_ ? dinc(o, b) : -dinc(o, b); on[o] = on_; }
static int norm_ok(void) {   // block b >= 1: its smallest cross offset to block 0 (if any) must be 0 (translation normalisation)
  for (int b = 1; b < B; b++) { int mn = 99; for (int o = 0; o < no; o++) if (on[o] && ob[o] == 0 && ob2[o] == b && od[o] < mn) mn = od[o]; if (mn != 99 && mn != 0) return 0; }
  return 1;
}
static void dfs(int o) {
  nodes++;
  if (o == no) {
    for (int p = 0; p < no; p++) if (!on[p] && can_add(p)) return;            // not maximal
    leaves++; for (int b = 0; b < B; b++) if (deg[b] < MIND) return;
    if (!norm_ok()) return;
    checked++; best = 0; arec(0, n == 64 ? ~0ULL : (1ULL << n) - 1); if (best < minalpha) minalpha = best;
    if (best < K) { printf("WITNESS alpha=%d orbits:", best); for (int p = 0; p < no; p++) if (on[p]) printf(" (%d,%d,%d)", ob[p], ob2[p], od[p]); printf("\n"); fflush(stdout); }
    return;
  }
  if (can_add(o)) { toggle(o, 1); dfs(o + 1); toggle(o, 0); }
  dfs(o + 1);
}
int main(int argc, char **argv) {
  B = atoi(argv[1]); m = atoi(argv[2]); K = atoi(argv[3]); if (argc > 4) MAXD = atoi(argv[4]); if (argc > 5) MIND = atoi(argv[5]); n = B * m; no = 0;
  for (int b = 0; b < B; b++) for (int d = 1; d <= m / 2; d++) { ob[no] = b; ob2[no] = b; od[no] = d; no++; }
  for (int b = 0; b < B; b++) for (int c = b + 1; c < B; c++) for (int t = 0; t < m; t++) { ob[no] = b; ob2[no] = c; od[no] = t; no++; }
  dfs(0);
  printf("B=%d m=%d K=%d orbits=%d nodes=%lld maximal=%lld checked=%lld min_alpha=%d\n", B, m, K, no, nodes, leaves, checked, minalpha); return 0;
}
