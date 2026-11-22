// D2000 dimension 2 (grow mode): start from a verified graph (graph6 file), lock it, add one vertex at a time (centre-outward), repair by annealing pulses.
// Usage: r310g <seed> <seconds> <start.g6> <targetN> <K>
// Based on D1998: simulated-annealing pulse search for a triangle-free graph on N vertices with independence number < K (default N=40, K=10).
// Usage: r310 <seed> <seconds> [N] [K]   -> prints progress; on success writes FOUND graph6 to stdout and found_<seed>.g6
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
typedef uint64_t u64;
static int N = 40, K = 10; static u64 adj[64], ALL;
static u64 rs;
static inline u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void){ return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static long long cnt(u64 cand, int k){           // number of independent k-sets inside cand
  if (k == 0) return 1;
  if (__builtin_popcountll(cand) < k) return 0;
  if (k == 1) return __builtin_popcountll(cand);
  long long r = 0;
  while (cand) { int v = __builtin_ctzll(cand); cand &= cand - 1;
    if (__builtin_popcountll(cand) < k - 1) break;
    r += cnt(cand & ~adj[v], k - 1); }
  return r; }
static int find_set(u64 cand, int k, int *out, int depth){   // random independent k-set (randomized DFS); returns 1 if found
  if (k == 0) return 1;
  if (__builtin_popcountll(cand) < k) return 0;
  int c[64], m = 0; u64 t = cand; while (t) { c[m++] = __builtin_ctzll(t); t &= t - 1; }
  for (int i = m - 1; i > 0; i--) { int j = rnd() % (i + 1); int s = c[i]; c[i] = c[j]; c[j] = s; }
  for (int i = 0; i < m; i++) { int v = c[i]; out[depth] = v; if (find_set(cand & ~adj[v] & ~(1ULL << v), k - 1, out, depth + 1)) return 1; }
  return 0; }
static inline void addE(int u, int v){ adj[u] |= 1ULL << v; adj[v] |= 1ULL << u; }
static inline void delE(int u, int v){ adj[u] &= ~(1ULL << v); adj[v] &= ~(1ULL << u); }
static inline long long pairI(int u, int v){ return cnt(ALL & ~adj[u] & ~adj[v] & ~(1ULL << u) & ~(1ULL << v), K - 2); } // indep K-sets containing u,v (if uv non-edge)
static void g6(FILE *f){ int bits[64*64], nb = 0; for (int j = 1; j < N; j++) for (int i = 0; i < j; i++) bits[nb++] = (adj[i] >> j) & 1;
  fputc(N + 63, f); for (int i = 0; i < nb; i += 6) { int x = 0; for (int b = 0; b < 6; b++) x = (x << 1) | (i + b < nb ? bits[i + b] : 0); fputc(x + 63, f); } fputc('\n', f); }
static void load_g6(const char *fn){ FILE *f = fopen(fn, "r"); char buf[4096]; fgets(buf, sizeof buf, f); fclose(f);
  int n = buf[0] - 63; N = n; memset(adj, 0, sizeof adj); int k = 0;
  for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { int byte = buf[1 + k / 6] - 63; if ((byte >> (5 - k % 6)) & 1) addE(i, j); k++; } }
static void add_vertex(void){   // new vertex v = N; neighbourhood = an independent set (keeps triangle-free) minimising new independent K-sets through v
  int v = N; u64 old = ALL; N++; ALL = (N == 64) ? ~0ULL : ((1ULL << N) - 1); long long bestc = -1; u64 bestI = 0;
  for (int trial = 0; trial < 400; trial++) {
    u64 I = 0, cand = old; int sz = 0, target = K - 1 - (int)(rnd() % 3);
    while (cand && sz < target) { int c[64], m = 0; u64 t = cand; while (t) { c[m++] = __builtin_ctzll(t); t &= t - 1; } int x = c[rnd() % m]; I |= 1ULL << x; cand &= ~adj[x] & ~(1ULL << x); sz++; }
    long long cc = cnt(old & ~I, K - 1);
    if (bestc < 0 || cc < bestc) { bestc = cc; bestI = I; } }
  u64 t = bestI; while (t) { int x = __builtin_ctzll(t); t &= t - 1; addE(v, x); } }
int main_grow(int argc, char **argv){
  u64 seed = strtoull(argv[1], 0, 10); double secs = atof(argv[2]); int target = atoi(argv[4]); K = atoi(argv[5]);
  rs = seed * 0x9E3779B97F4A7C15ULL + 1; load_g6(argv[3]); ALL = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
  time_t t0 = time(0), last = t0; int S_[64]; long long S = cnt(ALL, K);
  fprintf(stderr, "grow seed %llu start N=%d score %lld\n", (unsigned long long)seed, N, S);
  while (difftime(time(0), t0) < secs) {
    if (S == 0) { char fn[64]; sprintf(fn, "grow_%d_%d_%llu.g6", N, K, (unsigned long long)seed); FILE *f = fopen(fn, "w"); g6(f); fclose(f);
      fprintf(stderr, "LOCKED N=%d at t=%.0fs\n", N, difftime(time(0), t0)); if (N >= target) { printf("FOUND N=%d: ", N); g6(stdout); return 0; }
      add_vertex(); S = cnt(ALL, K); fprintf(stderr, "grew to N=%d score %lld\n", N, S); continue; }
    double T = 1.0; long long steps = 0, best = S;
    while (S > 0 && difftime(time(0), t0) < secs) {
      steps++; if (steps % 20000 == 0) { T *= 0.97; if (T < 0.05) T = 1.0; }
      if (!find_set(ALL, K, S_, 0)) { S = 0; break; }
      int a = S_[rnd() % K], b; do b = S_[rnd() % K]; while (b == a);
      u64 W = adj[a] & adj[b]; int rem[64][2], nr = 0; long long d = 0;
      while (W) { int w = __builtin_ctzll(W); W &= W - 1; int x = (rnd() & 1) ? a : b; delE(x, w); d += pairI(x, w); rem[nr][0] = x; rem[nr][1] = w; nr++; }
      long long lost = pairI(a, b); addE(a, b); d -= lost;
      if (d <= 0 || urand() < exp(-(double)d / T)) { S += d; if (S < best) best = S; }
      else { delE(a, b); for (int i = nr - 1; i >= 0; i--) addE(rem[i][0], rem[i][1]); }
      if (difftime(time(0), last) >= 30) { last = time(0); fprintf(stderr, "N=%d t=%.0fs score %lld best %lld T %.3f\n", N, difftime(last, t0), S, best, T); } } }
  fprintf(stderr, "grow done N=%d score %lld\n", N, S); return 1; }
int main(int argc, char **argv){
  if (argc > 5) return main_grow(argc, argv);
  u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1; double secs = argc > 2 ? atof(argv[2]) : 60;
  if (argc > 3) N = atoi(argv[3]); if (argc > 4) K = atoi(argv[4]);
  rs = seed * 0x9E3779B97F4A7C15ULL + 1; ALL = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
  memset(adj, 0, sizeof adj);
  // start: random maximal triangle-free graph (triangle-free process)
  for (int it = 0; it < 200000; it++) { int u = rnd() % N, v = rnd() % N; if (u == v || ((adj[u] >> v) & 1)) continue; if (adj[u] & adj[v]) continue; addE(u, v); }
  long long S = cnt(ALL, K), best = S; time_t t0 = time(0), last = t0; long long steps = 0, pulses = 0;
  double T0 = 2.0, T = T0; int S_[64];
  fprintf(stderr, "seed %llu start score %lld\n", (unsigned long long)seed, S);
  while (difftime(time(0), t0) < secs) {
    if (S == 0) break;
    steps++;
    if (steps % 20000 == 0) { T *= 0.97; if (T < 0.05) { T = T0; pulses++; } }  // pulse = one annealing epoch, then reheat
    if (!find_set(ALL, K, S_, 0)) { S = 0; break; }
    int a = S_[rnd() % K], b; do b = S_[rnd() % K]; while (b == a);
    // add edge ab; to keep triangle-free, cut one edge to each common neighbour
    u64 W = adj[a] & adj[b]; int rem[64][2], nr = 0; long long d = 0;
    while (W) { int w = __builtin_ctzll(W); W &= W - 1; int x = (rnd() & 1) ? a : b; delE(x, w); d += pairI(x, w); rem[nr][0] = x; rem[nr][1] = w; nr++; }
    long long lost = pairI(a, b); addE(a, b); d -= lost;
    if (d <= 0 || urand() < exp(-(double)d / T)) { S += d; if (S < best) { best = S; } }
    else { delE(a, b); for (int i = nr - 1; i >= 0; i--) addE(rem[i][0], rem[i][1]); }
    if (difftime(time(0), last) >= 30) { last = time(0); fprintf(stderr, "seed %llu t=%.0fs steps %lld pulses %lld score %lld best %lld T %.3f\n", (unsigned long long)seed, difftime(last, t0), steps, pulses, S, best, T); }
  }
  if (S == 0) { char fn[64]; sprintf(fn, "found_%llu.g6", (unsigned long long)seed); FILE *f = fopen(fn, "w"); g6(f); fclose(f); printf("FOUND seed %llu: ", (unsigned long long)seed); g6(stdout); }
  fprintf(stderr, "seed %llu done steps %lld pulses %lld final %lld best %lld\n", (unsigned long long)seed, steps, pulses, S, best);
  return S == 0 ? 0 : 1; }
