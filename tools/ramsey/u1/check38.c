// Verify r38_27: each line graph6 on 27 vertices, triangle-free, alpha <= 7 (no independent 8-set). Prints counts and edge/degree ranges.
#include <stdio.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t U; static U adj[32]; static int n, best, K = 8;
static void rec(int size, U cand) { if (best >= K) return; if (size + __builtin_popcount(cand) <= best) return; if (!cand) { best = size; return; }
  int v = __builtin_ctz(cand); rec(size + 1, cand & ~adj[v] & ~(1u << v)); rec(size, cand & ~(1u << v)); }
int main(void) {
  char line[512]; long cnt = 0, bad = 0; int emin = 999, emax = 0, dmin = 99, dmax = 0, amax = 0;
  while (fgets(line, sizeof line, stdin)) {
    n = line[0] - 63; memset(adj, 0, sizeof adj); int bit = 0, k = 1;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { int c = line[k + bit / 6] - 63; if (c >> (5 - bit % 6) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; } bit++; }
    int tri = 0, e = 0; for (int i = 0; i < n; i++) { int d = __builtin_popcount(adj[i]); e += d; if (d < dmin) dmin = d; if (d > dmax) dmax = d;
      for (int j = i + 1; j < n; j++) if ((adj[i] >> j & 1) && (adj[i] & adj[j])) tri = 1; }
    e /= 2; if (e < emin) emin = e; if (e > emax) emax = e;
    best = 0; rec(0, (1u << n) - 1); if (best > amax) amax = best;
    if (n != 27 || tri || best >= 8) bad++; cnt++;
  }
  printf("graphs %ld bad %ld | edges %d..%d degree %d..%d max_alpha %d\n", cnt, bad, emin, emax, dmin, dmax, amax); return 0;
}
