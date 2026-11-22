#include <stdio.h>
#include <stdint.h>
typedef uint64_t u64; static int n = 35; static u64 adj[64]; static long long c[16];
static void rec(u64 cand, int k){ c[k]++; while (cand){ int v = __builtin_ctzll(cand); cand &= cand - 1; rec(cand & ~adj[v], k + 1); } }
int main(){ int S[4] = {1, 7, 11, 16}; for (int v = 0; v < n; v++) for (int i = 0; i < 4; i++){ int a = (v + S[i]) % n, b = (v - S[i] + n) % n; adj[v] |= 1ULL << a; adj[v] |= 1ULL << b; }
  rec((1ULL << n) - 1, 0); for (int k = 0; k <= 9; k++) printf("size %d: %lld\n", k, c[k]); }
