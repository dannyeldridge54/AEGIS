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
#define NN 21                     // nodes: o0..o8, word, wordbigram, sparse, column, line-type, markup-state, match
#define NR 3                      // spin rates per node: fast 1/4, mid 1/16, slow 1/128 (a geometric = fractal ladder in time)
typedef struct { U8 n0, n1; U16 p; U16 r[NR]; U8 chk; } Cnt;   // + hash confirmation byte (ignition hygiene)   // two-way counts + the node's own direct probability
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
static U32 nbits_g = 0; static double BOOST = 0;
static void mx_update(Mixer *m, int y, int lr) { int err = (int)(((y << 12) - m->pr) * lr * (1.0 + BOOST * 8388608.0 / (8388608.0 + nbits_g))); int *w = m->w + m->ctx * m->n; for (int i = 0; i < m->n; i++) w[i] += (m->x[i] * err) >> 13; }

// ---- SSE lens (APM): refines a probability given a small context ----
typedef struct { U16 *t; int idx; } APM;
static void apm_init(APM *a, int n) { a->t = malloc(n * 33 * sizeof(U16)); for (int i = 0; i < n; i++) for (int j = 0; j < 33; j++) a->t[i * 33 + j] = squash((j - 16) * 128) * 16; }
static int apm_p(APM *a, int pr, int cx) { int s = stretch(pr) + 2048; int lo = s >> 7, w = s & 127; a->idx = lo + cx * 33 + (w >> 6); return (a->t[cx * 33 + lo] * (128 - w) + a->t[cx * 33 + lo + 1] * w) >> 11; }
static int apm_p16(APM *a, int pr, int cx) { int s = stretch(pr) + 2048; int lo = s >> 7, w = s & 127; a->idx = lo + cx * 33 + (w >> 6); return (a->t[cx * 33 + lo] * (128 - w) + a->t[cx * 33 + lo + 1] * w) >> 7; }   // 16-bit lens output
static void apm_update(APM *a, int y) { int g = (y << 16) + (y << 5) - y - y; a->t[a->idx] += (g - a->t[a->idx]) >> 6; }

// ---- model state ----
static U32 rep[4]; static U32 evst = 0; static U16 RSM[4][16]; static U8 RSMn[4][16]; static int ridx[4];   // xz/LZMA: 4 rep distances, event state
static int NOREP = 0, NOML = 0;
static int FIXPREV = 0, IGN = 0;
// v13 nodes: XML header fields, indirect, numbers, UTF-8
static U32 fld = 0, fpos = 0, tagh = 0; static int intag = 0, closing = 0; static U8 fval[16][64], fcur[64]; static U8 ind2[65536], ind3[65536]; static int numlen = 0, prevnum = 0, u8st = 0;
static U8 stk[32]; static U32 stkpos[32]; static int sd = 0; static U32 NSMASK = 3;   // negative space: pending closers
static U8 CMAP[256]; static int use_cmap = 0; static U32 chist = 0;
static U32 c0 = 1, c4 = 0, word = 0, word1 = 0, c8 = 0, col = 0, linefirst = 0, mstate = 0, abovepos = 0, linestart = 0; static U32 hsh[NN]; static Cnt *cur[NN - 1];
static U8 *buf; static U32 pos = 0, BUFN = 1 << 24; static U32 *MT; static U32 mptr = 0, mlen = 0; static int mbit = 0;
static int LR1 = 2, LR2 = 2; static U32 NODEMASK = 0xffffffff, SPIN = 1, APMW = 2; static Mixer M1, M2, MF;
#define NV 8
static Mixer MV[NV]; static int act = 0, bact = 2, pv[NV], pbl[4]; static double cv[NV], cb[4]; static int EVON;   // live balancer: shadow knob settings
static const int VLR[NV] = {1, 2, 4, 1, 1, 1, 1, 1}; static const U8 VMASK[NV] = {0x7f, 0x7f, 0x7f, 0x7d, 0x77, 0x7b, 0x47, 0x79};   // inputs: M1 M1fast M2 R0 R1 R2 bias
static const char *VNAME[NV] = {"all lr1", "all lr2", "all lr4", "-fastmix", "-ring0", "-ctxmix", "globals only", "rings+M1"}; static APM A1, A2; static U8 c1 = 0, c2 = 0;
static double CL[6];   // code length after: best single node(o2), L2 mixer, L3 lens1, L3 lens2 (final)
static int p_o2, p_mix, p_a1, p_fin; static int PMIN = 16, CONFIRM = 2;

static inline U32 H(U32 a, U32 b) { U32 h = a * 0x9E3779B1u ^ (b + 0x7F4A7C15u) * 0x85EBCA77u; return h ^ (h >> 15); }
static void byte_update(int c) {
  buf[pos & (BUFN - 1)] = c; pos++; c2 = c1; c1 = c; c4 = (c4 << 8) | c;
  c8 = (c8 << 8) | (c4 >> 24);
  if (c == '\n') { abovepos = linestart; linestart = pos; col = 0; linefirst = 0; } else { col++; if (col == 1) linefirst = c; }
  // XML field axis: which header field we are in, and the same field's value on the previous page
  if (c == '<') { intag = 1; tagh = 0; closing = 0; }
  else if (intag && c == '/' && tagh == 0) closing = 1;
  else if (intag && (c == '>' || c == ' ')) { intag = 0;
    if (closing) { if (fld) { memcpy(fval[fld & 15], fcur, 64); } fld = 0; } else { fld = tagh | 1; fpos = 0; memset(fcur, 0, 64); } }
  else if (intag) tagh = tagh * 31 + c;
  else if (fld) { if (fpos < 64) fcur[fpos] = c; fpos++; if (fpos > 200) fld = 0; }
  // indirect: what followed these two (three) bytes last time
  ind2[(c4 >> 8) & 0xffff] = c; ind3[((c4 >> 8) * 0x9E37u >> 8) & 0xffff] = c;
  // numbers
  if (c >= '0' && c <= '9') numlen++; else { if (numlen) prevnum = numlen; numlen = 0; }
  // UTF-8 continuation state
  if (c >= 0xC0) u8st = (c >= 0xF0) ? 3 : (c >= 0xE0) ? 2 : 1; else if (c >= 0x80 && u8st) u8st--; else u8st = 0;
  // negative space: push expected closers, pop when paid
  { U8 want = 0; if (c == '[' && (FIXPREV ? c2 : c1) == '[') want = ']'; else if (c == '{' && (FIXPREV ? c2 : c1) == '{') want = '}'; else if (c == '(') want = ')'; else if (c == '<') want = '>';
    if (want) { if (sd < 32) { stk[sd] = want; stkpos[sd] = pos; sd++; } }
    else if (sd && c == stk[sd - 1] && (c == ')' || c == '>' || (FIXPREV ? c2 : c1) == c)) sd--;
    if (c == '\n' && sd && stk[sd - 1] != '}') sd = 0; }
  // markup axis: inside [[link]], {{template}}, <tag>, table line, &entity
  if (c == '[' && c1 == '[') mstate |= 1; if (c == ']' && c1 == ']') mstate &= ~1u; if (c == '{' && c1 == '{') mstate |= 2; if (c == '}' && c1 == '}') mstate &= ~2u;
  if (c == '<') mstate |= 4; if (c == '>') mstate &= ~4u; if (c == '&') mstate |= 8; if (c == ';' || c == ' ') mstate &= ~8u;
  if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) word = H(word, c | 32); else if (word) { word1 = word; word = 0; }
  U32 h6 = H(c4, buf[(pos - 5) & (BUFN - 1)] << 8 | buf[(pos - 6) & (BUFN - 1)]);
  hsh[0] = 0; hsh[1] = H(1, c4 & 0xff); hsh[2] = H(2, c4 & 0xffff); hsh[3] = H(3, c4 & 0xffffff); hsh[4] = H(4, c4); hsh[5] = H(5, H(c4, c8 & 0xff)); hsh[6] = H(6, h6); hsh[7] = 0; /* set below: matched literal (xz) */ hsh[8] = H(8, word); hsh[9] = H(9, H(word, word1)); chist = (chist << 5 | CMAP[c]) & 0xfffff; hsh[10] = use_cmap ? H(10, chist) : H(10, (c4 >> 8) & 0xffff);   // D2007 class node (4 symbols of class history)
  { U32 ab = (col < (linestart - abovepos)) ? buf[(abovepos + col) & (BUFN - 1)] : 0; hsh[11] = H(11, H(col > 63 ? 63 : col, ab << 8 | (c4 & 0xff))); }
  hsh[12] = H(12, H(linefirst, c4 & 0xffff)); hsh[13] = H(13, H(mstate, c4 & 0xffffff));
  { U8 top = sd ? stk[sd - 1] : 0; int dep = sd > 7 ? 7 : sd; U32 gap = sd ? pos - stkpos[sd - 1] : 0; int gb = 0; while (gap > 1 && gb < 15) { gap >>= 1; gb++; }
    { U8 pf = (fld && fpos < 64) ? fval[fld & 15][fpos] : 0; hsh[16] = fld ? H(16, H(fld, pf << 16 | (fpos < 63 ? fpos : 63) << 8 | (c4 & 0xff))) : 16; }
    hsh[17] = H(17, H(ind2[c4 & 0xffff] << 8 | ind3[(c4 * 0x9E37u >> 8) & 0xffff], c4 & 0xff));
    hsh[18] = (numlen || (c4 & 0xff) == '|' || (c4 & 0xff) == ' ') ? H(18, H(numlen << 8 | prevnum, c4 & 0xffff)) : 18;
    hsh[19] = u8st || (c4 & 0x80) ? H(19, H(u8st, c4 & 0xffff)) : 19;
    hsh[14] = H(14, H(top << 8 | dep, c4 & 0xff)); hsh[15] = H(15, H(top << 8 | gb, c4 & 0xff));
    if (!(NSMASK & 1)) hsh[14] = 0; if (!(NSMASK & 2)) hsh[15] = 0; }
  // match model: find the last occurrence of the previous 6 bytes
  U32 mh = h6 & ((1 << 22) - 1);
  if (mlen && buf[mptr & (BUFN - 1)] == c && mlen < 65535) { mlen++; mptr++; } else { mlen = 0; }
  int was = mlen > 0;
  if (!mlen && pos >= 6) { mptr = MT[mh]; if (mptr) { U32 L = 0; while (L < 32 && L < mptr && buf[(mptr - 1 - L) & (BUFN - 1)] == buf[(pos - 1 - L) & (BUFN - 1)]) L++; mlen = L >= 6 ? L : 0;
      if (mlen) { U32 d = pos - mptr; int j = 0; while (j < 4 && rep[j] != d) j++; if (j == 4) j = 3; for (; j > 0; j--) rep[j] = rep[j - 1]; rep[0] = d; } } }
  evst = ((evst << 1) | was) & 15;
  MT[mh] = pos;
  { U32 mb = mlen ? buf[mptr & (BUFN - 1)] : (rep[0] ? buf[(pos - rep[0]) & (BUFN - 1)] : 0); hsh[7] = NOML ? H(7, H(c4, c8)) : H(7, H(mb | 256, c4 & 0xff)); }
}
static float GAIN[NN];   // per-node gain knob (tuned by poking)
static Mixer LM[NN], RM[8], M1b; static int ringof[NN] = {0,0,0,0,1,1,1,1,2,2,1,2,2,2,1,1,2,1,2,2,1}; static int NG = 3, NOBAL = 0;   // D2024: ring partition is a knob (RINGS env)
static int CP[8]; static double CC[8];   // compass: code length of every scale, per chunk
static int predict(void) {
  int k = 0, rk[8] = {0};
  for (int i = 0; i < NN - 1; i++) {
    int ins[3] = {0, 0, 0};
    if (NODEMASK >> i & 1) {
      U32 hh = H(hsh[i], c0); U32 idx = hh & ((1u << TB) - 1); cur[i] = &T[i][idx]; Cnt *q = cur[i];
      if (CONFIRM) { U8 ck = (hh >> 24) | 1; if (q->chk != ck) { if (q->n0 + q->n1 > 2 && CONFIRM == 2) { idx ^= 1; cur[i] = &T[i][idx]; q = cur[i]; } if (q->chk != ck) { memset(q, 0, sizeof *q); q->chk = ck; } } }
      sm_idx[i] = q->n0 * 61 + q->n1; int p = SM[i][sm_idx[i]] >> 4; if (p < 1) p = 1; if (p > 4095) p = 4095; if (i == 2) p_o2 = p;
      int seen = q->n0 + q->n1; int pd = q->p ? (q->p >> 4) : 2048; if (pd < 1) pd = 1; if (pd > 4095) pd = 4095;
      // local ring: the node mixes its own spins (fast / mid / slow) with its two-way counts
      Mixer *L = &LM[i]; L->x[0] = stretch(p); L->x[1] = seen ? stretch(pd) : 0;
      for (int r = 0; r < NR; r++) { int pr = q->r[r] ? q->r[r] >> 4 : 2048; if (pr < 1) pr = 1; if (pr > 4095) pr = 4095; L->x[2 + r] = (SPIN && seen) ? stretch(pr) : 0; }
      int pl = mx_p(L, seen > 15 ? 15 : seen);
      ins[0] = L->x[0]; ins[1] = L->x[1]; ins[2] = seen ? stretch(pl) : 0;
      if (IGN && seen < IGN) for (int z = 0; z < 3; z++) ins[z] = ins[z] * (seen + 1) / (IGN + 1);
      if (GAIN[i] != 1.0f) for (int z = 0; z < 3; z++) { int v = (int)(ins[z] * GAIN[i]); ins[z] = v > 2047 ? 2047 : v < -2047 ? -2047 : v; }
    } else cur[i] = 0;
    int g = ringof[i];
    for (int z = 0; z < 3; z++) { M1.x[k] = M1b.x[k] = M2.x[k] = ins[z]; k++; RM[g].x[rk[g]++] = ins[z]; }
  }
  int ml = mlen > 15 ? 15 : mlen; mbit = 0;
  if (mlen) { int bitpos = 0; U32 t = c0; while (t > 1) { t >>= 1; bitpos++; } U8 pb = buf[mptr & (BUFN - 1)];
    if (((pb + 256) >> (8 - bitpos)) == (int)c0) mbit = (pb >> (7 - bitpos)) & 1; else ml = 0; }
  sm_idx[NN - 1] = ml * 2 + mbit; int pm = SM[NN - 1][sm_idx[NN - 1]] >> 4; if (pm < 1) pm = 1; if (pm > 4095) pm = 4095;
  int xm = (ml && (NODEMASK >> (NN - 1) & 1)) ? stretch(pm) : 0; if (GAIN[NN - 1] != 1.0f) { int v = (int)(xm * GAIN[NN - 1]); xm = v > 2047 ? 2047 : v < -2047 ? -2047 : v; }
  M1.x[k] = M1b.x[k] = M2.x[k] = xm; k++; M1.x[k] = M1b.x[k] = M2.x[k] = 256; k++;
  { int bitpos = 0; U32 t = c0; while (t > 1) { t >>= 1; bitpos++; }
    for (int r = 0; r < 4; r++) { int xin = 0; ridx[r] = -1;
      if (!NOREP && rep[r] && (r > 0 || !mlen) && rep[r] < pos) { U8 eb = buf[(pos - rep[r]) & (BUFN - 1)];
        if (((eb + 256) >> (8 - bitpos)) == (int)c0) { int eb1 = (eb >> (7 - bitpos)) & 1; ridx[r] = bitpos * 2 + eb1; if (!RSM[r][ridx[r]]) RSM[r][ridx[r]] = eb1 ? 49152 : 16384;
          int pr = RSM[r][ridx[r]] >> 4; if (pr < 1) pr = 1; if (pr > 4095) pr = 4095; xin = stretch(pr); } }
      M1.x[k] = M1b.x[k] = M2.x[k] = xin; k++; RM[1].x[rk[1]++] = xin; } }
  M1.n = M1b.n = M2.n = k;
  RM[ringof[NN - 1]].x[rk[ringof[NN - 1]]++] = xm; for (int g = 0; g < NG; g++) { RM[g].x[rk[g]++] = 256; RM[g].n = rk[g]; }
  M1.n = M1b.n = M2.n = k;
  int pa = mx_p(&M1, c0), pab = mx_p(&M1b, c0), pb2 = mx_p(&M2, ((ml ? 1 + (ml > 8) : 0) * 16 + mstate) * 256 + c1);
  int prs[8]; for (int g = 0; g < NG; g++) prs[g] = mx_p(&RM[g], c0); CP[0] = pa; CP[1] = pab; CP[2] = pb2; CP[3] = prs[0]; CP[4] = NG > 1 ? prs[1] : 2048; CP[5] = NG > 2 ? prs[2] : 2048;
  MF.x[0] = stretch(pa); MF.x[1] = stretch(pab); MF.x[2] = stretch(pb2); for (int g = 0; g < NG; g++) MF.x[3 + g] = stretch(prs[g]); MF.x[3 + NG] = 256;
  { int ctx = (EVON ? evst : 0) * 24 + (ml ? 1 + (ml > 8) : 0) * 8 + ((c0 >= 16) + (c0 >= 4));
    for (int v = 0; v < NV; v++) { for (int j = 0; j < 4 + NG; j++) MV[v].x[j] = (NG != 3 || (VMASK[v] >> j & 1)) ? MF.x[j] : 0; pv[v] = mx_p(&MV[v], ctx); if (pv[v] < 1) pv[v] = 1; if (pv[v] > 4095) pv[v] = 4095; }
    p_mix = pv[act]; }
  int a1 = apm_p16(&A1, p_mix, c0); p_a1 = a1 >> 4; if (p_a1 < 1) p_a1 = 1; if (p_a1 > 4095) p_a1 = 4095; int pa2 = apm_p16(&A2, p_mix, (c0 | (c1 << 8)) & 0xffff); int pm16 = (p_mix << 4) + 8;
  pbl[0] = pm16; pbl[1] = (pm16 + a1) >> 1; pbl[2] = (pm16 + a1 + 2 * pa2) >> 2; pbl[3] = (a1 + pa2) >> 1;
  for (int b = 0; b < 4; b++) { if (pbl[b] < PMIN) pbl[b] = PMIN; if (pbl[b] > 65536 - PMIN) pbl[b] = 65536 - PMIN; }
  int p = pbl[bact]; p_fin = p; return p;
}
static U32 nbits = 0; static double chunkCL = 0;
static void update(int y) {
  nbits_g++;
  double cl = -log2((y ? p_fin : 65536 - p_fin) / 65536.0);
  CL[0] += -log2((y ? p_o2 : 4096 - p_o2) / 4096.0); CL[1] += -log2((y ? p_mix : 4096 - p_mix) / 4096.0);
  CL[2] += -log2((y ? p_a1 : 4096 - p_a1) / 4096.0); CL[3] += cl; chunkCL += cl;
  for (int j = 0; j < 6; j++) { int p = CP[j]; if (p < 1) p = 1; if (p > 4095) p = 4095; CC[j] += -log2((y ? p : 4096 - p) / 4096.0); }
  CC[6] += -log2((y ? p_mix : 4096 - p_mix) / 4096.0); CC[7] += -log2((y ? p_o2 : 4096 - p_o2) / 4096.0);
  if (++nbits % (8u << 20) == 0 && getenv("LIVE")) { double n = 1 << 20;
    fprintf(stderr, "COMPASS %u MB | final %.4f | M1 %.4f M1fast %.4f M2ctx %.4f | ring0(o0-3) %.4f ring1(o4-8,match,rep,class) %.4f ring2(words,axes) %.4f | MF %.4f | o2 alone %.4f\n",
      nbits >> 23, chunkCL / n, CC[0] / n, CC[1] / n, CC[2] / n, CC[3] / n, CC[4] / n, CC[5] / n, CC[6] / n, CC[7] / n);
    chunkCL = 0; for (int j = 0; j < 8; j++) CC[j] = 0; }
  for (int i = 0; i < NN - 1; i++) { if (!cur[i]) continue; mx_update(&LM[i], y, LR1); sm_update(i, y); Cnt *q = cur[i]; if (!q->p) q->p = 32768; int nn = q->n0 + q->n1;
    q->p += ((y ? 65535 : 0) - (int)q->p) / (nn < 30 ? nn + 2 : 32);
    static const int SH[NR] = {2, 4, 7}; for (int r = 0; r < NR; r++) { if (!q->r[r]) q->r[r] = 32768; q->r[r] += ((y ? 65535 : 0) - (int)q->r[r]) >> SH[r]; }
    cnt_update(q, y); }
  if (mlen) sm_update(NN - 1, y);
  for (int r = 0; r < 4; r++) if (ridx[r] >= 0) { U16 *p = &RSM[r][ridx[r]]; U8 *n = &RSMn[r][ridx[r]]; *p += ((y ? 65535 : 0) - *p) / (*n + 2); if (*n < 254) (*n)++; }
  mx_update(&M1, y, LR1); mx_update(&M1b, y, 4 * LR1); mx_update(&M2, y, LR1); for (int g = 0; g < NG; g++) mx_update(&RM[g], y, LR1);
  for (int v = 0; v < NV; v++) { cv[v] += -log2((y ? pv[v] : 4096 - pv[v]) / 4096.0); mx_update(&MV[v], y, VLR[v]); }
  for (int b = 0; b < 4; b++) cb[b] += -log2((y ? pbl[b] : 65536 - pbl[b]) / 65536.0);
  if (nbits % (8u << 18) == 0) { int bv = 0, bb = 0; for (int v = 1; v < NV; v++) if (cv[v] < cv[bv]) bv = v; for (int b = 1; b < 4; b++) if (cb[b] < cb[bb]) bb = b;
    if (getenv("LIVE") && (bv != act || bb != bact)) fprintf(stderr, "  KNOB @%.2f MB: mixer %s -> %s (%.0f vs %.0f bits), lens blend %d -> %d\n", nbits / 8388608.0, VNAME[act], VNAME[bv], cv[act], cv[bv], bact, bb);
    act = bv; bact = bb; for (int v = 0; v < NV; v++) cv[v] *= 0.5; for (int b = 0; b < 4; b++) cb[b] *= 0.5; } apm_update(&A1, y); apm_update(&A2, y);
  c0 = (c0 << 1) | y; if (c0 >= 256) { byte_update(c0 & 255); c0 = 1; }
}

// ---- arithmetic coder (carryless, 32-bit) ----
static U32 x1 = 0, x2 = 0xffffffff, xv = 0; static FILE *fo, *fi;
static void enc(int y, int p) { U32 xm = x1 + (U32)(((uint64_t)(x2 - x1) * p) >> 16); y ? (x2 = xm) : (x1 = xm + 1); while (((x1 ^ x2) & 0xff000000) == 0) { putc(x2 >> 24, fo); x1 <<= 8; x2 = (x2 << 8) | 255; } }
static int dec(int p) { U32 xm = x1 + (U32)(((uint64_t)(x2 - x1) * p) >> 16); int y = xv <= xm; y ? (x2 = xm) : (x1 = xm + 1);
  while (((x1 ^ x2) & 0xff000000) == 0) { x1 <<= 8; x2 = (x2 << 8) | 255; int c = getc(fi); xv = (xv << 8) | (c == EOF ? 0 : c); } return y; }

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: loomz c|d in out\n"); return 1; }
  if (getenv("LR1")) LR1 = atoi(getenv("LR1")); if (getenv("LR2")) LR2 = atoi(getenv("LR2")); if (getenv("MASK")) NODEMASK = strtoul(getenv("MASK"), 0, 0); if (getenv("SPIN")) SPIN = atoi(getenv("SPIN")); if (getenv("APMW")) APMW = atoi(getenv("APMW")); if (getenv("CLASSMAP")) { FILE *cf = fopen(getenv("CLASSMAP"), "rb"); if (!cf || fread(CMAP, 1, 256, cf) != 256) { fprintf(stderr, "bad CLASSMAP\n"); return 1; } fclose(cf); use_cmap = 1; }
  NOREP = getenv("NOREP") != 0; NOML = getenv("NOML") != 0;
  init_tables(); sm_init(); for (int i = 0; i < NN - 1; i++) T[i] = calloc(1u << TB, sizeof(Cnt));
  buf = calloc(BUFN, 1); MT = calloc(1 << 22, 4);
  mx_init(&M1, NI, 256); mx_init(&M1b, NI, 256); for (int i = 0; i < NN; i++) mx_init(&LM[i], 5, 16); for (int g = 0; g < 8; g++) mx_init(&RM[g], 40, 256); mx_init(&M2, NI, 3 * 16 * 256); mx_init(&MF, 7, 24 * 16); apm_init(&A1, 256); apm_init(&A2, 65536);
  if (getenv("RINGS")) { char *q = getenv("RINGS"); NG = 0; for (int i = 0; i < NN && *q; i++) { ringof[i] = strtol(q, &q, 10); if (ringof[i] + 1 > NG) NG = ringof[i] + 1; if (*q == ',') q++; } }
  NOBAL = getenv("NOBAL") != 0;
  for (int v = 0; v < NV; v++) { mx_init(&MV[v], 4 + NG, 24 * 16); for (int i = 0; i < (4 + NG) * 24 * 16; i++) MV[v].w[i] = (1 << 16) * 7 / (4 + NG) / 4; }
  EVON = getenv("EV") != 0; if (getenv("PMIN")) PMIN = atoi(getenv("PMIN")); if (getenv("CONFIRM")) CONFIRM = atoi(getenv("CONFIRM")); FIXPREV = getenv("FIXPREV") != 0; if (getenv("IGN")) IGN = atoi(getenv("IGN")); if (getenv("BOOST")) BOOST = atof(getenv("BOOST")); if (getenv("NS")) NSMASK = atoi(getenv("NS"));
  for (int i = 0; i < NN; i++) GAIN[i] = 1.0f; if (getenv("GAINS")) { char *q = getenv("GAINS"); for (int i = 0; i < NN && *q; i++) { GAIN[i] = strtof(q, &q); if (*q == ',') q++; } }
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
