// loomz: Loom compressor (PREREG_D2006). Pulse out = bit prediction, wave back = the real bit; every node records both ways.
// Layers: L1 two-way nodes (orders 0,1,2,3,4,6 + word + match), L2 context-gated mixers + a second-layer mixer, L3 two SSE lenses.
// Reports the ideal code length after each layer (bits/byte), so each layer's gain is measured.
// Usage: loomz c in out | loomz d in out        (single core; memory set by TB below)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint32_t U32; typedef uint16_t U16; typedef uint8_t U8;

static int sq_t[4096]; static short st_t[4096];
static int squash(int d) { if (d > 2047) d = 2047; if (d < -2047) d = -2047; return sq_t[d + 2048]; }   // -> 0..4095
static int stretch(int p) { return st_t[p]; }
static void init_tables(void) {
  for (int i = 0; i < 4096; i++) { double x = (i - 2048) / 256.0; int v = (int)(4096.0 / (1.0 + exp(-x))); if (v > 4095) v = 4095; if (v < 1) v = 1; sq_t[i] = v; }
  int pi = 0; for (int x = -2047; x <= 2047; x++) { int v = squash(x); for (int j = pi; j <= v; j++) st_t[j] = x; pi = v + 1; }
  for (int j = pi; j < 4096; j++) st_t[j] = 2047;
}

// ---- two-way node: counts of 0s and 1s, nonstationary (the "flip") ----
#define TB 22                     // log2 slots per node table
#define NN 15                     // nodes: o0..o8, word, wordbigram, sparse, column, line-type, markup-state, match
#define NR 3                      // spin rates per node: fast 1/4, mid 1/16, slow 1/128 (a geometric = fractal ladder in time)
typedef struct { U8 n0, n1; U16 p; U16 r[NR]; } Cnt;   // two-way counts + the node's own direct probability
static Cnt *T[NN - 1];
static void cnt_update(Cnt *c, int y) {
  if (y) { if (c->n1 < 60) c->n1++; if (c->n0 > 2) c->n0 = c->n0 / 2 + 1; }
  else   { if (c->n0 < 60) c->n0++; if (c->n1 > 2) c->n1 = c->n1 / 2 + 1; }
}
// StateMap: learned probability for each (n0,n1) state, per node (the node's own lens)
static U16 SM[NN][61 * 61];
static int sm_idx[NN];
static void sm_init(void) { for (int k = 0; k < NN; k++) for (int a = 0; a <= 60; a++) for (int b = 0; b <= 60; b++) SM[k][a * 61 + b] = (U16)(65536.0 * (b + 0.4) / (a + b + 0.8)); }
static U8 SMn[NN][61 * 61];
static void sm_update(int k, int y) { U16 *p = &SM[k][sm_idx[k]]; U8 *n = &SMn[k][sm_idx[k]]; int target = y ? 65535 : 0; *p += (target - *p) / (*n + 2); if (*n < 254) (*n)++; }   // adaptive rate 1/n (lpaq StateMap)

// ---- mixers ----
#define NI (NN * (2 + NR) + 2)
typedef struct { int n, ctxs; int *w; int x[NI]; int pr; int ctx; } Mixer;
static void mx_init(Mixer *m, int n, int ctxs) { m->n = n; m->ctxs = ctxs; m->w = calloc(n * ctxs, sizeof(int)); for (int i = 0; i < n * ctxs; i++) m->w[i] = (1 << 14); }
static int mx_p(Mixer *m, int ctx) { m->ctx = ctx; int *w = m->w + ctx * m->n; long long s = 0; for (int i = 0; i < m->n; i++) s += (long long)m->x[i] * w[i]; m->pr = squash((int)(s >> 16)); return m->pr; }
static void mx_update(Mixer *m, int y, int lr) { int err = ((y << 12) - m->pr) * lr; int *w = m->w + m->ctx * m->n; for (int i = 0; i < m->n; i++) w[i] += (m->x[i] * err) >> 13; }

// ---- SSE lens (APM): refines a probability given a small context ----
typedef struct { U16 *t; int idx; } APM;
static void apm_init(APM *a, int n) { a->t = malloc(n * 33 * sizeof(U16)); for (int i = 0; i < n; i++) for (int j = 0; j < 33; j++) a->t[i * 33 + j] = squash((j - 16) * 128) * 16; }
static int apm_p(APM *a, int pr, int cx) { int s = stretch(pr) + 2048; int lo = s >> 7, w = s & 127; a->idx = lo + cx * 33 + (w >> 6); return (a->t[cx * 33 + lo] * (128 - w) + a->t[cx * 33 + lo + 1] * w) >> 11; }
static void apm_update(APM *a, int y) { int g = (y << 16) + (y << 5) - y - y; a->t[a->idx] += (g - a->t[a->idx]) >> 6; }

// ---- model state ----
static U32 c0 = 1, c4 = 0, word = 0, word1 = 0, c8 = 0, col = 0, linefirst = 0, mstate = 0, abovepos = 0, linestart = 0; static U32 hsh[NN]; static Cnt *cur[NN - 1];
static U8 *buf; static U32 pos = 0, BUFN = 1 << 24; static U32 *MT; static U32 mptr = 0, mlen = 0; static int mbit = 0;
static int LR1 = 2, LR2 = 2; static U32 NODEMASK = 0xffffffff, SPIN = 1, APMW = 2; static Mixer M1, M2, MF; static APM A1, A2; static U8 c1 = 0, c2 = 0;
static double CL[6];   // code length after: best single node(o2), L2 mixer, L3 lens1, L3 lens2 (final)
static int p_o2, p_mix, p_a1, p_fin;

static inline U32 H(U32 a, U32 b) { U32 h = a * 0x9E3779B1u ^ (b + 0x7F4A7C15u) * 0x85EBCA77u; return h ^ (h >> 15); }
static void byte_update(int c) {
  buf[pos & (BUFN - 1)] = c; pos++; c2 = c1; c1 = c; c4 = (c4 << 8) | c;
  c8 = (c8 << 8) | (c4 >> 24);
  if (c == '\n') { abovepos = linestart; linestart = pos; col = 0; linefirst = 0; } else { col++; if (col == 1) linefirst = c; }
  // markup axis: inside [[link]], {{template}}, <tag>, table line, &entity
  if (c == '[' && c1 == '[') mstate |= 1; if (c == ']' && c1 == ']') mstate &= ~1u; if (c == '{' && c1 == '{') mstate |= 2; if (c == '}' && c1 == '}') mstate &= ~2u;
  if (c == '<') mstate |= 4; if (c == '>') mstate &= ~4u; if (c == '&') mstate |= 8; if (c == ';' || c == ' ') mstate &= ~8u;
  if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) word = H(word, c | 32); else if (word) { word1 = word; word = 0; }
  U32 h6 = H(c4, buf[(pos - 5) & (BUFN - 1)] << 8 | buf[(pos - 6) & (BUFN - 1)]);
  hsh[0] = 0; hsh[1] = H(1, c4 & 0xff); hsh[2] = H(2, c4 & 0xffff); hsh[3] = H(3, c4 & 0xffffff); hsh[4] = H(4, c4); hsh[5] = H(5, H(c4, c8 & 0xff)); hsh[6] = H(6, h6); hsh[7] = H(7, H(c4, c8)); hsh[8] = H(8, word); hsh[9] = H(9, H(word, word1)); hsh[10] = H(10, (c4 >> 8) & 0xffff);
  { U32 ab = (col < (linestart - abovepos)) ? buf[(abovepos + col) & (BUFN - 1)] : 0; hsh[11] = H(11, H(col > 63 ? 63 : col, ab << 8 | (c4 & 0xff))); }
  hsh[12] = H(12, H(linefirst, c4 & 0xffff)); hsh[13] = H(13, H(mstate, c4 & 0xffffff));
  // match model: find the last occurrence of the previous 6 bytes
  U32 mh = h6 & ((1 << 22) - 1);
  if (mlen && buf[mptr & (BUFN - 1)] == c && mlen < 65535) { mlen++; mptr++; } else { mlen = 0; }
  if (!mlen && pos >= 6) { mptr = MT[mh]; if (mptr) { U32 L = 0; while (L < 32 && L < mptr && buf[(mptr - 1 - L) & (BUFN - 1)] == buf[(pos - 1 - L) & (BUFN - 1)]) L++; mlen = L >= 6 ? L : 0; } }
  MT[mh] = pos;
}
static int predict(void) {
  int k = 0;
  for (int i = 0; i < NN - 1; i++) {
    if (!(NODEMASK >> i & 1)) { for (int z = 0; z < 2 + NR; z++) { M1.x[k] = M2.x[k] = 0; k++; } cur[i] = 0; continue; }   // ring switched off: no work
    U32 idx = H(hsh[i], c0) & ((1u << TB) - 1); cur[i] = &T[i][idx];
    sm_idx[i] = cur[i]->n0 * 61 + cur[i]->n1; int p = SM[i][sm_idx[i]] >> 4; if (p < 1) p = 1; if (p > 4095) p = 4095;
    int s = stretch(p); M1.x[k] = s; M2.x[k] = s; k++;
    int pd = cur[i]->p ? (cur[i]->p >> 4) : 2048; if (pd < 1) pd = 1; if (pd > 4095) pd = 4095;
    int sd = (cur[i]->n0 + cur[i]->n1) ? stretch(pd) : 0; M1.x[k] = sd; M2.x[k] = sd; k++;
    if (!(NODEMASK >> i & 1)) { M1.x[k-1] = M2.x[k-1] = M1.x[k-2] = M2.x[k-2] = 0; }
    for (int r = 0; r < NR; r++) { int pr = cur[i]->r[r] ? cur[i]->r[r] >> 4 : 2048; if (pr < 1) pr = 1; if (pr > 4095) pr = 4095; M1.x[k] = M2.x[k] = (SPIN && (NODEMASK >> i & 1) && (cur[i]->n0 + cur[i]->n1)) ? stretch(pr) : 0; k++; }
    if (i == 2) p_o2 = p;
  }
  // match node: expected bit and length
  int ml = mlen > 15 ? 15 : mlen; mbit = 0;
  if (mlen) { int bitpos = 0; U32 t = c0; while (t > 1) { t >>= 1; bitpos++; } U8 pb = buf[mptr & (BUFN - 1)];
    if (((pb + 256) >> (8 - bitpos)) == (int)c0) mbit = (pb >> (7 - bitpos)) & 1; else ml = 0; }
  sm_idx[NN - 1] = ml * 2 + mbit; int pm = SM[NN - 1][sm_idx[NN - 1]] >> 4; if (pm < 1) pm = 1; if (pm > 4095) pm = 4095;
  M1.x[k] = (ml && (NODEMASK >> (NN-1) & 1)) ? stretch(pm) : 0; M2.x[k] = M1.x[k]; k++; M1.x[k] = M2.x[k] = 256; k++;   // bias
  M1.x[k] = M2.x[k] = 0; k++;
  int pa = mx_p(&M1, c0); int pb2 = mx_p(&M2, ((ml ? 1 + (ml > 8) : 0) * 16 + mstate) * 256 + c1);
  MF.x[0] = stretch(pa); MF.x[1] = stretch(pb2); MF.x[2] = 256; p_mix = mx_p(&MF, 0);
  p_a1 = apm_p(&A1, p_mix, c0); if (p_a1 < 1) p_a1 = 1; if (p_a1 > 4095) p_a1 = 4095; int pa2 = apm_p(&A2, p_mix, (c0 | (c1 << 8)) & 0xffff);
  int p = APMW == 0 ? p_mix : APMW == 1 ? (p_mix + p_a1) >> 1 : (p_mix + p_a1 + 2 * pa2) >> 2; if (p < 1) p = 1; if (p > 4095) p = 4095; p_fin = p; return p;
}
static void update(int y) {
  CL[0] += -log2((y ? p_o2 : 4096 - p_o2) / 4096.0); CL[1] += -log2((y ? p_mix : 4096 - p_mix) / 4096.0);
  CL[2] += -log2((y ? p_a1 : 4096 - p_a1) / 4096.0); CL[3] += -log2((y ? p_fin : 4096 - p_fin) / 4096.0);
  for (int i = 0; i < NN - 1; i++) { if (!cur[i]) continue; sm_update(i, y); Cnt *q = cur[i]; if (!q->p) q->p = 32768; int nn = q->n0 + q->n1;
    q->p += ((y ? 65535 : 0) - (int)q->p) / (nn < 30 ? nn + 2 : 32);
    static const int SH[NR] = {2, 4, 7}; for (int r = 0; r < NR; r++) { if (!q->r[r]) q->r[r] = 32768; q->r[r] += ((y ? 65535 : 0) - (int)q->r[r]) >> SH[r]; }
    cnt_update(q, y); }
  if (mlen) sm_update(NN - 1, y);
  mx_update(&M1, y, LR1); mx_update(&M2, y, LR1); mx_update(&MF, y, LR2); apm_update(&A1, y); apm_update(&A2, y);
  c0 = (c0 << 1) | y; if (c0 >= 256) { byte_update(c0 & 255); c0 = 1; }
}

// ---- arithmetic coder (carryless, 32-bit) ----
static U32 x1 = 0, x2 = 0xffffffff, xv = 0; static FILE *fo, *fi;
static void enc(int y, int p) { U32 xm = x1 + (U32)(((uint64_t)(x2 - x1) * p) >> 12); y ? (x2 = xm) : (x1 = xm + 1); while (((x1 ^ x2) & 0xff000000) == 0) { putc(x2 >> 24, fo); x1 <<= 8; x2 = (x2 << 8) | 255; } }
static int dec(int p) { U32 xm = x1 + (U32)(((uint64_t)(x2 - x1) * p) >> 12); int y = xv <= xm; y ? (x2 = xm) : (x1 = xm + 1);
  while (((x1 ^ x2) & 0xff000000) == 0) { x1 <<= 8; x2 = (x2 << 8) | 255; int c = getc(fi); xv = (xv << 8) | (c == EOF ? 0 : c); } return y; }

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: loomz c|d in out\n"); return 1; }
  if (getenv("LR1")) LR1 = atoi(getenv("LR1")); if (getenv("LR2")) LR2 = atoi(getenv("LR2")); if (getenv("MASK")) NODEMASK = strtoul(getenv("MASK"), 0, 0); if (getenv("SPIN")) SPIN = atoi(getenv("SPIN")); if (getenv("APMW")) APMW = atoi(getenv("APMW")); init_tables(); sm_init(); for (int i = 0; i < NN - 1; i++) T[i] = calloc(1u << TB, sizeof(Cnt));
  buf = calloc(BUFN, 1); MT = calloc(1 << 22, 4);
  mx_init(&M1, NI, 256); mx_init(&M2, NI, 3 * 16 * 256); mx_init(&MF, 3, 1); apm_init(&A1, 256); apm_init(&A2, 65536);
  for (int i = 0; i < 3; i++) MF.w[i] = 1 << 15;
  fi = fopen(argv[2], "rb"); fo = fopen(argv[3], "wb"); if (!fi || !fo) { perror("open"); return 1; }
  if (argv[1][0] == 'c') {
    fseek(fi, 0, SEEK_END); U32 n = ftell(fi); fseek(fi, 0, SEEK_SET); fwrite(&n, 4, 1, fo);
    for (U32 i = 0; i < n; i++) { int c = getc(fi); for (int j = 7; j >= 0; j--) { int y = (c >> j) & 1; enc(y, predict()); update(y); } }
    putc(x1 >> 24, fo); putc(255, fo); putc(255, fo); putc(255, fo);
    long out = ftell(fo);
    fprintf(stderr, "in %u out %ld  bpc %.4f | per-layer ideal bpc: node o2 %.4f, L2 mixers %.4f, L3 lens1 %.4f, final %.4f\n", n, out, 8.0 * out / n,
            CL[0] / n, CL[1] / n, CL[2] / n, CL[3] / n);
  } else {
    U32 n; if (fread(&n, 4, 1, fi) != 1) return 1; for (int i = 0; i < 4; i++) { int c = getc(fi); xv = (xv << 8) | (c == EOF ? 0 : c); }
    for (U32 i = 0; i < n; i++) { int c = 0; for (int j = 0; j < 8; j++) { int y = dec(predict()); update(y); c = (c << 1) | y; } putc(c, fo); }
  }
  fclose(fo);
  return 0;
}
