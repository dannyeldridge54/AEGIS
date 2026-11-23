"""N7/N8: our own continuous-energy neutron Monte Carlo (ENDF/B-VIII.0 OpenMC HDF5, 294 K), concentric spheres, analog.
Physics: non-redundant reactions sampled by partial cross section; secondaries from the evaluated distributions (uncorrelated angle +
level / continuous / evaporation energy; Kalbach-Mann; correlated angle-energy); CM->lab per reaction; target at rest (no free-gas thermal
motion); photons not transported. Collision estimator for tritium production (MT205)."""
import math, os, h5py, numpy as np
H5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ndata', 'h5')

# ---------------- small samplers ----------------
def _tab1d(ds):
    x, y = ds[()]; return x, y
def _eval_tab(xy, E):
    return float(np.interp(E, xy[0], xy[1]))
def _pick(Egrid, E, rng):
    """incident-energy bracket + stochastic interpolation index"""
    n = len(Egrid)
    if E <= Egrid[0]: return 0, 0, 0.0
    if E >= Egrid[-1]: return n - 2, n - 1, 1.0
    i = int(np.searchsorted(Egrid, E) - 1); f = (E - Egrid[i]) / (Egrid[i + 1] - Egrid[i])
    return i, (i + 1 if rng.random() < f else i), f
def _sample_table(x, p, c, interp, ndisc, rng):
    xi = rng.random(); k = int(np.searchsorted(c, xi, side='right') - 1); k = max(0, min(k, len(x) - 1))
    if k < ndisc: return x[k], k
    if k >= len(x) - 1: return x[-1], len(x) - 1
    if interp == 1 or p[k + 1] == p[k] or x[k + 1] == x[k]:
        return (x[k] + (xi - c[k]) / p[k]) if p[k] > 0 else x[k], k
    m = (p[k + 1] - p[k]) / (x[k + 1] - x[k]); disc = p[k] ** 2 + 2 * m * (xi - c[k])
    return x[k] + (math.sqrt(max(disc, 0.0)) - p[k]) / m, k

class Angle:
    def __init__(self, g):
        self.E = g['energy'][()]; d = g['mu']; self.t = d[()]; self.off = d.attrs['offsets']; self.itp = d.attrs['interpolation']
    def sample(self, E, rng):
        _, l, _ = _pick(self.E, E, rng); a = self.off[l]; b = self.off[l + 1] if l + 1 < len(self.off) else self.t.shape[1]
        mu, _ = _sample_table(self.t[0, a:b], self.t[1, a:b], self.t[2, a:b], self.itp[l], 0, rng)
        return max(-1.0, min(1.0, mu))

class Tabular:   # continuous tabular E_out (optionally Kalbach-Mann r, a rows)
    def __init__(self, g, km=False, key='distribution'):
        self.E = g['energy'][()]; d = g[key]; self.t = d[()]; self.off = d.attrs['offsets']; self.itp = d.attrs['interpolation']
        self.nd = d.attrs['n_discrete_lines']; self.km = km
    def _rng(self, l):
        a = self.off[l]; b = self.off[l + 1] if l + 1 < len(self.off) else self.t.shape[1]; return a, b
    def sample(self, E, rng):
        i, l, f = _pick(self.E, E, rng); a, b = self._rng(l)
        x = self.t[0, a:b]; e, k = _sample_table(x, self.t[1, a:b], self.t[2, a:b], self.itp[l], self.nd[l], rng)
        # scaled interpolation of the continuous part (OpenMC / MCNP)
        if k >= self.nd[l] and len(self.E) > 1:
            ai, bi = self._rng(i); aj, bj = self._rng(min(i + 1, len(self.E) - 1))
            n_i, n_j = self.nd[i], self.nd[min(i + 1, len(self.E) - 1)]
            E1 = self.t[0, ai + n_i] + f * (self.t[0, aj + n_j] - self.t[0, ai + n_i]); EK = self.t[0, bi - 1] + f * (self.t[0, bj - 1] - self.t[0, bi - 1])
            El1, ElK = x[self.nd[l]], x[-1]
            if ElK > El1: e = E1 + (e - El1) * (EK - E1) / (ElK - El1)
        mu = None
        if self.km:
            r = self.t[3, a + k]; aa = self.t[4, a + k]
            if aa < 1e-8: mu = 2 * rng.random() - 1
            elif rng.random() > r:   # N6-N8 DEV-1: cosh (symmetric) branch with probability 1 - r
                T = (2 * rng.random() - 1) * math.sinh(aa); mu = math.log(T + math.sqrt(T * T + 1)) / aa
            else:                    # precompound e^{a mu} branch with probability r
                xi = rng.random(); mu = math.log(xi * math.exp(aa) + (1 - xi) * math.exp(-aa)) / aa
        return max(e, 0.0), mu, (a + k)

class Correlated:
    def __init__(self, g):
        self.E = g['energy'][()]; d = g['energy_out']; self.t = d[()]; self.off = d.attrs['offsets']; self.itp = d.attrs['interpolation']
        self.nd = d.attrs['n_discrete_lines']; self.mu = g['mu'][()]
    def sample(self, E, rng):
        _, l, _ = _pick(self.E, E, rng); a = self.off[l]; b = self.off[l + 1] if l + 1 < len(self.off) else self.t.shape[1]
        e, k = _sample_table(self.t[0, a:b], self.t[1, a:b], self.t[2, a:b], self.itp[l], self.nd[l], rng)
        j = a + k; mi = int(self.t[3, j]); mo = int(self.t[4, j]); me = int(self.t[4, j + 1]) if j + 1 < self.t.shape[1] else self.mu.shape[1]
        if me <= mo + 1: mu = 2 * rng.random() - 1
        else:
            mu, _ = _sample_table(self.mu[0, mo:me], self.mu[1, mo:me], self.mu[2, mo:me], mi, 0, rng)
        return max(e, 0.0), max(-1.0, min(1.0, mu))
    def _mu_end(self, j, b):
        # last outgoing-energy entry of this incident table: next table's first offset, or end of the mu array
        nxt = b
        return int(self.t[4, nxt]) if nxt < self.t.shape[1] else self.mu.shape[1]

class Dist:
    def __init__(self, g):
        self.type = g.attrs['type'].decode(); self.app = _tab1d(g['applicability']) if 'applicability' in g else None
        self.angle = self.energy = None
        if self.type == 'uncorrelated':
            if 'angle' in g and 'energy' in g['angle']: self.angle = Angle(g['angle'])
            if 'energy' in g:
                e = g['energy']; t = e.attrs['type'].decode(); self.etype = t
                if t == 'level': self.thr, self.mr = e.attrs['threshold'], e.attrs['mass_ratio']
                elif t == 'continuous': self.energy = Tabular(e)
                elif t in ('evaporation', 'maxwell'): self.theta = _tab1d(e['theta']); self.u = e.attrs['u']
                else: raise NotImplementedError(t)
            else: self.etype = None
        elif self.type == 'kalbach-mann': self.km = Tabular(g, km=True)
        elif self.type == 'correlated': self.cor = Correlated(g)
        else: raise NotImplementedError(self.type)
    def sample(self, E, rng):
        """returns (E_out, mu) in the frame the data are given in"""
        if self.type == 'kalbach-mann':
            e, mu, _ = self.km.sample(E, rng); return e, mu
        if self.type == 'correlated': return self.cor.sample(E, rng)
        mu = self.angle.sample(E, rng) if self.angle else 2 * rng.random() - 1
        if self.etype is None: return None, mu
        if self.etype == 'level': return self.mr * (E - self.thr), mu
        if self.etype == 'continuous': e, _, _ = self.energy.sample(E, rng); return e, mu
        th = _eval_tab(self.theta, E); lim = E - self.u
        for _ in range(1000):
            if self.etype == 'evaporation': e = -th * math.log(rng.random() * rng.random())
            else: e = -th * (math.log(rng.random()) + math.log(rng.random()) * math.cos(math.pi / 2 * rng.random()) ** 2)
            if e <= lim: return e, mu
        return max(lim, 0.0), mu

class Reaction:
    def __init__(self, r, E, i0, xs):
        a = r.attrs; self.mt = int(a['mt']); self.Q = float(a['Q_value']); self.com = bool(a['center_of_mass'])
        self.i0 = i0; self.xs = xs; self.prods = []
        for pk in sorted(k for k in r.keys() if k.startswith('product')):
            p = r[pk]
            if p.attrs['particle'] != b'neutron': continue
            y = p['yield']; yt = y.attrs['type'].decode()
            yf = ('poly', y[()]) if yt == 'Polynomial' else ('tab', _tab1d(y))
            ds = [Dist(p[dk]) for dk in sorted(k for k in p.keys() if k.startswith('distribution'))]
            self.prods.append((yf, ds))

class Nuclide:
    def __init__(self, name, T='294K'):
        h = h5py.File(os.path.join(H5, f'{name}.h5'))[name]; self.name = name; self.awr = float(h.attrs['atomic_weight_ratio'])
        self.E = h['energy'][T][()]; self.rx = []; tot = np.zeros_like(self.E)
        for k, r in h['reactions'].items():
            if r.attrs['redundant'] or T not in r: continue
            d = r[T]['xs']; i0 = int(d.attrs.get('threshold_idx', 0)); xs = d[()]
            full = np.zeros_like(self.E); full[i0:i0 + len(xs)] = xs; tot += full
            self.rx.append(Reaction(r, self.E, i0, full))
        self.tot = tot
        t205 = h['reactions'].get('reaction_205'); self.trit = None
        if t205 is not None and T in t205:
            d = t205[T]['xs']; i0 = int(d.attrs.get('threshold_idx', 0)); full = np.zeros_like(self.E); full[i0:i0 + len(d)] = d[()]; self.trit = full
        self.extra = {}   # N9/N10 scores (redundant summary MTs): heating, damage energy, gas production
        for mt in (301, 444, 901, 203, 207):
            rr = h['reactions'].get(f'reaction_{mt:03d}')
            if rr is not None and T in rr:
                d = rr[T]['xs']; i0 = int(d.attrs.get('threshold_idx', 0)); full = np.zeros_like(self.E); full[i0:i0 + len(d)] = d[()]; self.extra[mt] = full
    def at(self, arr, E): return float(np.interp(E, self.E, arr))
    def loc(self, E):
        n = len(self.E)
        if E <= self.E[0]: return 0, 0.0
        if E >= self.E[-1]: return n - 2, 1.0
        i = int(np.searchsorted(self.E, E)) - 1; return i, (E - self.E[i]) / (self.E[i + 1] - self.E[i])
    @staticmethod
    def val(arr, i, f): return float(arr[i] + f * (arr[i + 1] - arr[i]))

def _yield(yf, E):
    if yf[0] == 'poly': return float(np.polyval(yf[1][::-1], E))
    return float(np.interp(E, yf[1][0], yf[1][1]))

def _rotate(u, mu, rng):
    phi = 2 * math.pi * rng.random(); s = math.sqrt(max(0.0, 1 - mu * mu)); ux, uy, uz = u
    if abs(uz) > 0.9999: return (s * math.cos(phi), s * math.sin(phi), mu * (1 if uz > 0 else -1))
    a = math.sqrt(1 - uz * uz)
    return (mu * ux + s * (ux * uz * math.cos(phi) - uy * math.sin(phi)) / a,
            mu * uy + s * (uy * uz * math.cos(phi) + ux * math.sin(phi)) / a,
            mu * uz - s * a * math.cos(phi))

def to_lab(E, Ecm, mu, A):
    El = Ecm + (E + 2 * mu * (A + 1) * math.sqrt(E * Ecm)) / (A + 1) ** 2
    mul = mu * math.sqrt(Ecm / El) + math.sqrt(E / El) / (A + 1) if El > 0 else mu
    return El, max(-1.0, min(1.0, mul))

class Material:
    def __init__(self, comp, cache):
        self.items = [(cache.setdefault(n, Nuclide(n)), d) for n, d in comp.items()]
        grid = np.unique(np.concatenate([nu.E for nu, _ in self.items])); self.grid = grid
        self.sig = sum(d * np.interp(grid, nu.E, nu.tot) for nu, d in self.items)
    def Sigma(self, E):
        g = self.grid
        if E <= g[0]: return float(self.sig[0])
        if E >= g[-1]: return float(self.sig[-1])
        i = int(np.searchsorted(g, E)) - 1; return float(self.sig[i] + (E - g[i]) / (g[i + 1] - g[i]) * (self.sig[i + 1] - self.sig[i]))

def run(regions, radii, n_hist=20000, seed=7, E0=14.0e6, kill_mt=(), tally_regions=(), max_coll=100000, scores=(), yield_override=None):
    """scores: iterable of (region, mt) collision-estimator tallies (sum over nuclides of N sigma_mt / Sigma_t per collision)."""
    """regions: list of Material or None (void) per shell; radii: outer radius per shell (cm). Returns dict of tallies per source neutron."""
    rng = np.random.default_rng(seed); leak = 0.0; trit = {}; ncoll = 0; sc = {k: 0.0 for k in scores}; leakE = 0.0
    for h in range(n_hist):
        mu = 2 * rng.random() - 1; ph = 2 * math.pi * rng.random(); s = math.sqrt(1 - mu * mu)
        bank = [((0.0, 0.0, 0.0), (s * math.cos(ph), s * math.sin(ph), mu), E0)]
        while bank:
            r, u, E = bank.pop()
            alive = True
            while alive:
                rr = math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)
                reg = next((i for i, R in enumerate(radii) if rr < R - 1e-9 or (abs(rr - R) <= 1e-9 and (r[0] * u[0] + r[1] * u[1] + r[2] * u[2]) < 0)), len(radii))
                if reg >= len(radii): leak += 1; leakE += E; break
                # distance to the outer and inner boundaries of this shell
                b = r[0] * u[0] + r[1] * u[1] + r[2] * u[2]; c2 = rr * rr
                Ro = radii[reg]; d_out = -b + math.sqrt(max(b * b - (c2 - Ro * Ro), 0.0))
                d_in = math.inf
                if reg > 0:
                    Ri = radii[reg - 1]; disc = b * b - (c2 - Ri * Ri)
                    if disc > 0 and b < 0:
                        t = -b - math.sqrt(disc)
                        if t > 1e-9: d_in = t
                d_b = min(d_out, d_in); mat = regions[reg]
                if mat is None:
                    r = tuple(r[i] + (d_b + 1e-7) * u[i] for i in range(3)); continue
                St = mat.Sigma(E); d_c = -math.log(rng.random()) / St if St > 0 else math.inf
                if d_c >= d_b:
                    r = tuple(r[i] + (d_b + 1e-7) * u[i] for i in range(3)); continue
                r = tuple(r[i] + d_c * u[i] for i in range(3)); ncoll += 1
                if ncoll > max_coll * n_hist: raise RuntimeError('collision cap')
                # tally (collision estimator): tritium production rate / total rate
                locs = [nu.loc(E) for nu, _ in mat.items]; tots = [Nuclide.val(nu.tot, *lc) * dens for (nu, dens), lc in zip(mat.items, locs)]
                St = sum(tots)
                if reg in tally_regions:
                    for (nu, dens), lc in zip(mat.items, locs):
                        if nu.trit is not None: trit[nu.name] = trit.get(nu.name, 0.0) + dens * Nuclide.val(nu.trit, *lc) / St
                for key in sc:
                    sreg, smt = key[0], key[1]; pre = key[2] if len(key) > 2 else ''
                    if sreg == reg:
                        sc[key] += sum(dens * Nuclide.val(nu.extra[smt], *lc) for (nu, dens), lc in zip(mat.items, locs) if smt in nu.extra and nu.name.startswith(pre)) / St
                # nuclide
                xi = rng.random() * St; acc = 0.0
                for j, ((nu, dens), t) in enumerate(zip(mat.items, tots)):
                    acc += t
                    if acc >= xi: break
                i, f = locs[j]
                # reaction
                xi = rng.random() * Nuclide.val(nu.tot, i, f); acc = 0.0
                for rx in nu.rx:
                    if i + 1 < rx.i0: continue
                    acc += Nuclide.val(rx.xs, i, f)
                    if acc >= xi: break
                if rx.mt in kill_mt or not rx.prods: alive = False; break
                new = []
                for yf, ds in rx.prods:
                    y = yield_override[rx.mt] if (yield_override and rx.mt in yield_override) else _yield(yf, E); n = int(y + rng.random())
                    for _ in range(n):
                        dist = ds[0]
                        if len(ds) > 1:
                            ps = np.array([_eval_tab(d.app, E) for d in ds]); k = int(np.searchsorted(np.cumsum(ps) / ps.sum(), rng.random())); dist = ds[min(k, len(ds) - 1)]
                        Eo, m = dist.sample(E, rng)
                        if rx.mt == 2: Eo = E * (nu.awr / (nu.awr + 1)) ** 2          # elastic: CM neutron energy
                        if m is None: m = 2 * rng.random() - 1
                        if rx.com: Eo, m = to_lab(E, Eo, m, nu.awr)
                        if Eo > 1e-5: new.append((r, _rotate(u, m, rng), Eo))
                if not new: alive = False; break
                (r, u, E) = new[0]; bank.extend(new[1:])
    out = dict(leakage=leak / n_hist, leak_energy_eV=leakE / n_hist, collisions_per_hist=ncoll / n_hist, n_hist=n_hist, scores={'_'.join(str(x) for x in k): v / n_hist for k, v in sc.items()})
    for k, v in trit.items(): out[f'T_{k}'] = v / n_hist
    out['TBR'] = sum(v for k, v in out.items() if k.startswith('T_Li'))
    return out
