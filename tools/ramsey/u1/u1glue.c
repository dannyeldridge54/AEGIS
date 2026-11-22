// U1 (D2020 prototype): for each (3,8,27)-graph D (graph6 on stdin), find all 6-tuples A1<=...<=A6 of independent sets of D (|A| 5..7)
// so that H = D + v + w1..w6 (w_a ~ v, w_a ~ A_a) is a (3,9,34)-graph: triangle-free automatically; alpha(H) <= 8 iff every independent
// j-set of D is missed by at most 8-j of the A's (j = 7,6,5,4,3); and max degree <= 8 (deg_D(u) + #A containing u <= 8).
// Prints per-D solution counts and (optionally) the H graphs' A-sets. Usage: u1glue [maxD] [print]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t U; static U adj[32]; static int n;
#define MAXI 400000
static U I7[MAXI], I6[MAXI], I5[MAXI], I4[MAXI], I3[MAXI]; static int n7, n6, n5, n4, n3;
static U cand[MAXI]; static int nc; static U *mm[6]; static int W[6];   // per candidate: bitset of which j-sets it misses (for 7- and 6-sets)
static int dD[32];
static void enumI(U mask, int size, U cur, int start) {
  if (size >= 3 && size <= 7) { switch (size) { case 7: if (n7 < MAXI) I7[n7++] = cur; break; case 6: if (n6 < MAXI) I6[n6++] = cur; break;
      case 5: if (n5 < MAXI) I5[n5++] = cur; if (nc < MAXI) cand[nc++] = cur; break; case 4: if (n4 < MAXI) I4[n4++] = cur; break; case 3: if (n3 < MAXI) I3[n3++] = cur; break; } }
  if (size == 6 && nc < MAXI) cand[nc++] = cur; if (size == 7 && nc < MAXI) cand[nc++] = cur;
  if (size == 7) return;
  for (int v = start; v < n; v++) if (mask >> v & 1) enumI(mask & ~adj[v] & ~((1u << (v + 1)) - 1), size + 1, cur | (1u << v), v + 1);
}
static long long sols; static int PRINT; static int chosen[6];
static int miss_ok(U *list, int cnt, int maxmiss, int k) {   // every set in list missed by at most maxmiss of chosen[0..k-1]
  if (maxmiss >= k) return 1;
  for (int s = 0; s < cnt; s++) { int miss = 0; for (int a = 0; a < k; a++) if (!(cand[chosen[a]] & list[s])) { if (++miss > maxmiss) return 0; } }
  return 1;
}
static int cap_ok(int k) { int c[32] = {0}; for (int a = 0; a < k; a++) { U x = cand[chosen[a]]; while (x) { int u = __builtin_ctz(x); x &= x - 1; if (dD[u] + (++c[u]) > 8) return 0; } } return 1; }
static void rec(int k, int from) {
  if (k == 6) {
    if (!miss_ok(I5, n5, 3, 6) || !miss_ok(I4, n4, 4, 6) || !miss_ok(I3, n3, 5, 6)) return;
    sols++; if (PRINT) { for (int a = 0; a < 6; a++) printf("%x ", cand[chosen[a]]); printf("\n"); } return;
  }
  for (int c = from; c < nc; c++) { chosen[k] = c;
    if (!cap_ok(k + 1)) continue;
    if (!miss_ok(I7, n7, 1, k + 1)) continue;          // a 7-set may be missed by at most 1 A
    if (k + 1 >= 3 && !miss_ok(I6, n6, 2, k + 1)) continue;
    rec(k + 1, c); }
}
int main(int argc, char **argv) {
  long maxD = argc > 1 ? atol(argv[1]) : 1000000000L; PRINT = argc > 2; char line[512]; long nd = 0, withsol = 0; long long total = 0;
  while (nd < maxD && fgets(line, sizeof line, stdin)) {
    n = line[0] - 63; memset(adj, 0, sizeof adj); int bit = 0, k = 1;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { int c = line[k + bit / 6] - 63; if (c >> (5 - bit % 6) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; } bit++; }
    for (int i = 0; i < n; i++) dD[i] = __builtin_popcount(adj[i]);
    n7 = n6 = n5 = n4 = n3 = nc = 0; enumI((1u << n) - 1, 0, 0, 0);
    sols = 0; rec(0, 0); nd++; total += sols; if (sols) withsol++;
    if (PRINT) printf("# D %ld: cand %d I7 %d I6 %d sols %lld\n", nd, nc, n7, n6, sols);
  }
  fprintf(stderr, "D graphs %ld, with solutions %ld, total 6-tuples %lld\n", nd, withsol, total); return 0;
}
