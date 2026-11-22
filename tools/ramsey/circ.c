// D2000 dimension 1: exhaustive search of maximal triangle-free circulant graphs C_n(S) with independence number < K.
// Usage: circ <n> <K>  -> prints every witness S (distances) and a count; exit 0 if any witness.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static int n, K, H; static u64 adj[64]; static long long maximal = 0, wit = 0, nodes = 0;
static int inS[64];
static void build(void){ for (int v = 0; v < n; v++){ adj[v] = 0; for (int d = 1; d <= H; d++) if (inS[d]) { adj[v] |= 1ULL << ((v + d) % n); adj[v] |= 1ULL << ((v - d + n) % n); } } }
static int has_indep(u64 cand, int k){ if (k == 0) return 1; if (__builtin_popcountll(cand) < k) return 0;
  while (cand){ int v = __builtin_ctzll(cand); cand &= cand - 1; if (__builtin_popcountll(cand) < k - 1) return 0; if (has_indep(cand & ~adj[v], k - 1)) return 1; } return 0; }
static int dist_in(int x){ x = ((x % n) + n) % n; if (x == 0) return 0; int d = x <= n - x ? x : n - x; return inS[d]; }
static int tri_free_with(int d){   // would adding distance d create a triangle? triangle iff a+b=c (mod n) with a,b,c in ±S
  inS[d] = 1; int ok = 1;
  for (int a = 1; a <= H && ok; a++) if (inS[a]) for (int b = 1; b <= H && ok; b++) if (inS[b]) {
    if (dist_in(a + b) || dist_in(a - b) ) { if ((a + b) % n != 0 && dist_in(a + b)) ok = 0; if (a != b && dist_in(a - b)) ok = 0; } }
  inS[d] = 0; return ok; }
static void rec(int d){
  nodes++;
  if (d > H){   // maximal?
    for (int e = 1; e <= H; e++) if (!inS[e] && tri_free_with(e)) return;
    maximal++; build(); u64 nb0 = ((n == 64) ? ~0ULL : ((1ULL << n) - 1)) & ~adj[0] & ~1ULL;
    if (!has_indep(nb0, K - 1)) { wit++; printf("WITNESS n=%d K=%d S={", n, K); for (int e = 1; e <= H; e++) if (inS[e]) printf(" %d", e); printf(" }\n"); fflush(stdout); }
    return; }
  if (tri_free_with(d)) { inS[d] = 1; rec(d + 1); inS[d] = 0; }
  rec(d + 1); }
int main(int argc, char **argv){ n = atoi(argv[1]); K = atoi(argv[2]); H = n / 2; rec(1);
  fprintf(stderr, "n=%d K=%d maximal_tri_free_S=%lld witnesses=%lld nodes=%lld\n", n, K, maximal, wit, nodes); return wit ? 0 : 1; }
