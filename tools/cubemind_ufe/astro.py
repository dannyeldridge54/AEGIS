"""UFE-lens tracks for Janus (Danny 21 Nov 2026): astrophysics, compression, the UFE itself, and placing a piece in the field.
Every item is graded mechanically: NUM:<value>:<rel tol> for numbers, exact text otherwise."""
import math
G_ASTRO = {}
def _num(v, tol=0.02): return 'NUM:%.6g:%g' % (v, tol)
def _kepler(rng, n):
    out = []
    for _ in range(n):
        a = round(rng.uniform(0.3, 40), 2); M = round(rng.uniform(0.3, 3), 2)
        out.append((f'A planet orbits a star of {M} solar masses at {a} AU. Orbital period in years? (Kepler: P^2 = a^3/M). Give only the number.', _num(math.sqrt(a ** 3 / M))))
    return out
def _schw(rng, n):
    out = []
    for _ in range(n):
        M = rng.choice([1, 3, 10, 30, 65, 4.3e6, 6.5e9, rng.randint(2, 99)])
        out.append((f'Schwarzschild radius in km of a {M} solar-mass black hole (r = 2GM/c^2, 2.953 km per solar mass)? Give only the number.', _num(2.953 * M)))
    return out
def _escape(rng, n):
    out = []
    for _ in range(n):
        M = round(rng.uniform(0.1, 300), 1); R = round(rng.uniform(0.3, 12), 2)
        out.append((f'Escape velocity in km/s from a body of {M} Earth masses and {R} Earth radii (Earth: 11.19 km/s)? Give only the number.', _num(11.186 * math.sqrt(M / R))))
    return out
def _hubble(rng, n):
    out = []
    for _ in range(n):
        v = rng.randint(700, 30000)
        out.append((f'A galaxy recedes at {v} km/s. With H0 = 70 km/s/Mpc, its distance in Mpc? Give only the number.', _num(v / 70)))
    return out
def _wien(rng, n):
    out = []
    for _ in range(n):
        T = rng.randint(2000, 40000)
        out.append((f'A star has surface temperature {T} K. Wien peak wavelength in nm (b = 2.898e6 nm K)? Give only the number.', _num(2.898e6 / T)))
    return out
def _lum(rng, n):
    out = []
    for _ in range(n):
        R = round(rng.uniform(0.1, 50), 2); T = rng.randint(3000, 30000)
        out.append((f'A star has radius {R} R_sun and temperature {T} K (Sun 5772 K). Luminosity in L_sun (L = R^2 (T/5772)^4)? Give only the number.', _num(R ** 2 * (T / 5772) ** 4, 0.03)))
    return out
def _lawson(rng, n):
    out = []
    for _ in range(n):
        nn = rng.choice([1e19, 3e19, 1e20, 3e20, 1e21]); T = rng.choice([5, 10, 15, 20]); tau = rng.choice([0.1, 0.5, 1, 3, 10])
        ok = nn * T * tau >= 3e21
        out.append((f'Fusion plasma: density {nn:.0e} m^-3, temperature {T} keV, confinement {tau} s. Does n*T*tau reach the D-T ignition triple product 3e21 keV s m^-3? Answer YES or NO.', 'YES' if ok else 'NO'))
    return out
def _bits(rng, n):
    out = []
    for _ in range(n):
        ps = [round(rng.choice([0.5, 0.9, 0.99, 0.75, 0.6, 0.95]), 2) for _ in range(rng.randint(3, 6))]
        out.append((f'A compressor gave the actual next symbols these probabilities: {ps}. Ideal compressed size in bits (sum of -log2 p)? Give only the number.', _num(sum(-math.log2(p) for p in ps), 0.02)))
    return out
def _which(rng, n):
    out = []
    for _ in range(n):
        a = [round(rng.uniform(0.3, 0.99), 2) for _ in range(4)]; b = [round(rng.uniform(0.3, 0.99), 2) for _ in range(4)]
        ca, cb = sum(-math.log2(x) for x in a), sum(-math.log2(x) for x in b)
        if abs(ca - cb) < 0.2: b[0] = round(max(0.3, b[0] - 0.25), 2); cb = sum(-math.log2(x) for x in b)
        out.append((f'Model A gave the true symbols probabilities {a}; model B gave {b}. Which compresses smaller? Answer A or B.', 'A' if ca < cb else 'B'))
    return out
UFE_FACTS = [
    ('In the Weave UFE, what is the visible gauge kinetic function f_vis in terms of T_vis and S?', 'T_vis + 9S'),
    ('In the Weave UFE, the flux 9 in f_vis = T_vis + 9S equals how many families times 3? Give the number of families.', '3'),
    ('Which orientifold does the Weave compactify on? Answer like Z6-II.', 'Z6-II'),
    ('Euler number chi of the Weave fold?', '48'),
    ('KKLT condensate rank N selected in the Weave?', '6'),
    ('The S vacuum sits at the knot rho. g_s there equals 2 divided by the square root of what number?', '3'),
    ('Order of the knot rho = e^(i pi/3) (the still point)?', '3'),
    ('Order of the knot i (the hub)?', '2'),
    ('Weave dark-matter (dark baryon) mass in GeV?', 'NUM:12.8:0.02'),
    ('Weave heavy-neutrino mass M_N in GeV?', 'NUM:1.84e11:0.03'),
    ('Weave tensor-to-scalar ratio r (D = 10)?', 'NUM:5.4e-4:0.03'),
    ('Weave |W0| value?', 'NUM:5.6e-9:0.05'),
    ('Weave proton lifetime in years?', 'NUM:1.6e35:0.05'),
    ('Which interface of the three Weave fields (S-T, T-U or S-U) holds every current failure? Answer like S-T.', 'S-T'),
    ('Weave predicted Delta N_eff?', '0'),
    ('How many Weave fields are in tandem (S, T, U)?', '3'),
]
PLACE = [  # every piece fits somewhere: which field governs it (S time/cosmology, T forces/scales, U matter/flavour)
    ('inflation', 'S'), ('reheating temperature', 'S'), ('the spectral index n_s', 'S'), ('the string coupling g_s', 'S'),
    ('primordial gravitational waves r', 'S'), ('the gravitino mass', 'T'), ('the gauge couplings at unification', 'T'),
    ('the gluino mass', 'T'), ('the proton lifetime', 'T'), ('the volume of the compact space', 'T'), ('quark masses', 'U'),
    ('the CKM mixing matrix', 'U'), ('charged-lepton masses (Koide)', 'U'), ('neutrino masses', 'U'), ('heavy neutrinos M_N', 'U'),
    ('the wino mass', 'T')]
def _ufe(rng, n):
    idx = list(range(len(UFE_FACTS))); rng.shuffle(idx); return [UFE_FACTS[i] for i in idx[:n]]
def _place(rng, n):
    idx = list(range(len(PLACE))); rng.shuffle(idx)
    return [(f'UFE lens: which of the three Weave fields governs {PLACE[i][0]}? S (time/cosmology), T (forces/scales) or U (matter/flavour). Answer S, T or U.', PLACE[i][1]) for i in idx[:n]]
def _astro_mix(rng, n):
    gens = [_kepler, _schw, _escape, _hubble, _wien, _lum, _lawson]; out = []
    for i in range(n): out += gens[i % len(gens)](rng, 1)
    return out
TRACKS = {'astro': _astro_mix, 'compress': lambda r, n: [(_bits if i % 2 else _which)(r, 1)[0] for i in range(n)], 'ufe': _ufe, 'place': _place}
LENS_TRACKS = set(TRACKS)
