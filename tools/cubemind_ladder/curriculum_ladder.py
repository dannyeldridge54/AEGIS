"""CubeMind learning ladder (23 Nov 2026): nuclear -> reactors -> fields -> circuits -> digital logic -> CPU design.
Every item is mechanically gradable with an exact answer (integers, short words or fixed decimals), in the same
(question, answer) format as curriculum.py. Lessons and exams are drawn from the same generators but never share a
question (curriculum.build enforces this). See CUBEMIND_LESSON_PLAN.md for the stages and promotion rules."""
import math

STAGE_OF = {}   # track -> stage number (1..6), for the lesson plan and the console


def _t(stage):
    def deco(f):
        STAGE_OF[f.__name__.lstrip('_')] = stage
        return f
    return deco


# ---------------- Stage 1: nuclear basics ----------------
NUCS = [('helium-4', 2, 4), ('lithium-6', 3, 6), ('lithium-7', 3, 7), ('carbon-12', 6, 12), ('oxygen-16', 8, 16),
        ('iron-56', 26, 56), ('nickel-62', 28, 62), ('tungsten-184', 74, 184), ('lead-208', 82, 208), ('uranium-235', 92, 235),
        ('uranium-238', 92, 238), ('tritium (hydrogen-3)', 1, 3), ('beryllium-9', 4, 9), ('argon-40', 18, 40), ('cobalt-60', 27, 60)]


@_t(1)
def _nuc_count(rng, n):
    out = []
    for i in range(n):
        name, Z, A = rng.choice(NUCS)
        if rng.random() < 0.5:
            out.append((f'{name} has {Z} protons. How many neutrons does it have? Give only the number.', str(A - Z)))
        else:
            out.append((f'{name} has mass number {A} and {A - Z} neutrons. What is its atomic number Z? Give only the number.', str(Z)))
    return out


@_t(1)
def _nuc_binding(rng, n):
    out = []
    for i in range(n):
        Z, N = rng.randint(2, 40), rng.randint(2, 50)
        me = rng.randint(-90000, 20000)
        B = Z * 7289 + N * 8071 - me
        out.append((f'A nucleus has Z={Z}, N={N} and mass excess {me} keV. Using hydrogen-atom excess 7289 keV and neutron excess '
                    f'8071 keV, total binding energy B = Z*7289 + N*8071 - (mass excess). Give B in keV as an integer.', str(B)))
    return out


@_t(1)
def _nuc_decay(rng, n):
    out = []
    for i in range(n):
        T = rng.choice([2, 3, 5, 8, 10, 12, 24, 30]); k = rng.randint(1, 7); N0 = 2 ** rng.randint(k, k + 6) * rng.choice([1, 3, 5])
        if rng.random() < 0.5:
            out.append((f'A sample has a half-life of {T} hours. Starting with {N0} atoms, how many remain after {k*T} hours? Give only the number.', str(N0 // 2 ** k)))
        else:
            out.append((f'An isotope has a half-life of {T} days. After {k*T} days, what fraction remains? Answer as 1/N.', f'1/{2**k}'))
    return out


@_t(1)
def _nuc_qvalue(rng, n):
    reacts = [('D + T -> He-4 + n', [13136, 14950], [2425, 8071], 17590),
              ('D + D -> He-3 + n', [13136, 13136], [14931, 8071], 3270),
              ('D + He-3 -> He-4 + p', [13136, 14931], [2425, 7289], 18353),
              ('n + Li-6 -> T + He-4', [8071, 14087], [14950, 2425], 4783)]
    out = []
    for i in range(n):
        nm, r, p, _ = rng.choice(reacts)
        s = rng.randint(-40, 40)        # perturb so the question is new; answer recomputed
        r2 = [r[0] + s, r[1]]
        Q = sum(r2) - sum(p)
        out.append((f'Reaction {nm}. Reactant mass excesses {r2[0]} and {r2[1]} keV; product mass excesses {p[0]} and {p[1]} keV. '
                    f'Q = (sum of reactant excesses) - (sum of product excesses). Give Q in keV as an integer.', str(Q)))
    return out


# ---------------- Stage 2: reactor physics and design ----------------
@_t(2)
def _rx_power(rng, n):
    out = []
    for i in range(n):
        kind = rng.randint(0, 3)
        if kind == 0:
            P = rng.randint(2, 60) * 50
            out.append((f'A D-T plasma makes {P} MW of fusion power. Alpha particles carry 20% of it. How many MW heat the plasma? Integer only.', str(P // 5)))
        elif kind == 1:
            P, a = rng.randint(4, 60) * 25, rng.choice([10, 20, 25, 40, 50, 100])
            out.append((f'Fusion power {P} MW with {a} MW of external heating. What is the plasma gain Q = P_fus/P_aux? Give an integer if exact, else to 1 decimal.', f'{P/a:.1f}'.rstrip('0').rstrip('.')))
        elif kind == 2:
            th, eff, rec = rng.randint(10, 40) * 100, rng.choice([30, 33, 35, 40, 45]), rng.randint(5, 30) * 10
            out.append((f'A plant produces {th} MW of heat. Turbines convert {eff}% to electricity and the plant uses {rec} MW to run itself. Net electric power in MW (integer)?', str(th * eff // 100 - rec)))
        else:
            nT, t = rng.choice([[1, 10], [2, 12], [3, 15], [1.5, 20], [2.5, 8]]), rng.choice([1, 2, 3, 4])
            n20, T = nT
            prod = n20 * 1e20 * T * t
            out.append((f'Density {n20}e20 per m^3, temperature {T} keV, confinement time {t} s. Is the triple product at least 3e21 keV s/m^3 (ignition rule of thumb)? YES or NO.', 'YES' if prod >= 3e21 else 'NO'))
    return out


@_t(2)
def _rx_limits(rng, n):
    out = []
    for i in range(n):
        kind = rng.randint(0, 2)
        if kind == 0:
            Ip, a = rng.choice([8, 10, 12, 15, 17, 20]), rng.choice([1.0, 1.5, 2.0, 2.5, 3.0])
            nG = Ip / (math.pi * a * a)
            out.append((f'Greenwald density limit n_G = Ip/(pi a^2) in units of 1e20 m^-3, with Ip = {Ip} MA and minor radius a = {a} m. Give n_G to 2 decimals.', f'{nG:.2f}'))
        elif kind == 1:
            Ps, R = rng.randint(40, 250), rng.choice([6, 7, 8, 9])
            out.append((f'Power crossing the plasma edge P_sep = {Ps} MW in a machine with major radius R = {R} m. Does it pass the divertor limit P_sep/R <= 17 MW/m? YES or NO.', 'YES' if Ps / R <= 17 else 'NO'))
        else:
            Ps, PLH = rng.randint(20, 200), rng.randint(40, 160)
            out.append((f'Edge power P_sep = {Ps} MW and H-mode threshold P_LH = {PLH} MW. Does it meet the EU-DEMO rule P_sep >= 1.2 x P_LH? YES or NO.', 'YES' if Ps >= 1.2 * PLH else 'NO'))
    return out


@_t(2)
def _rx_breeding(rng, n):
    out = []
    for i in range(n):
        N = rng.choice([1000, 2000, 4000, 5000, 10000]); T = int(N * rng.uniform(0.85, 1.2))
        tbr = T / N
        q = rng.randint(0, 1)
        if q == 0:
            out.append((f'A blanket simulation follows {N} neutrons and makes {T} tritium atoms. What is the tritium breeding ratio, to 3 decimals?', f'{tbr:.3f}'))
        else:
            out.append((f'Tritium breeding ratio {tbr:.3f}. Does it meet the design target of at least 1.05? YES or NO.', 'YES' if round(tbr, 3) >= 1.05 else 'NO'))
    return out


# ---------------- Stage 3: fields ----------------
@_t(3)
def _fields(rng, n):
    out = []
    for i in range(n):
        kind = rng.randint(0, 3)
        if kind == 0:
            q, v, B = rng.choice([1, 2, 3]), rng.randint(1, 9) * 10 ** 6, rng.randint(1, 12)
            F = q * 1.6e-19 * v * B
            out.append((f'A particle with charge {q} x 1.6e-19 C moves at {v} m/s perpendicular to a {B} T field. Lorentz force F = qvB, in units of 1e-13 N, to 2 decimals?', f'{F/1e-13:.2f}'))
        elif kind == 1:
            nturn, I = rng.choice([1000, 2000, 5000, 10000]), rng.choice([1, 2, 5, 10, 20, 50, 100])
            B = 4e-7 * math.pi * nturn * I
            out.append((f'Long solenoid: {nturn} turns per metre carrying {I} A. B = mu0 n I with mu0 = 4*pi*1e-7. Give B in millitesla to 1 decimal.', f'{B*1000:.1f}'))
        elif kind == 2:
            B = rng.randint(1, 20)
            p = B * B / (2 * 4e-7 * math.pi) / 1e6
            out.append((f'Magnetic pressure p = B^2/(2 mu0) for B = {B} T (mu0 = 4*pi*1e-7). Give p in MPa to 1 decimal.', f'{p:.1f}'))
        else:
            q1, q2, r = rng.randint(1, 9), rng.randint(1, 9), rng.choice([1, 2, 3])
            F = 9e9 * q1 * 1e-6 * q2 * 1e-6 / r ** 2
            out.append((f'Two charges of {q1} uC and {q2} uC are {r} m apart. Coulomb force F = 9e9 q1 q2 / r^2 in newtons, to 3 decimals?', f'{F:.3f}'))
    return out


# ---------------- Stage 4: circuits ----------------
@_t(4)
def _circuits(rng, n):
    out = []
    for i in range(n):
        kind = rng.randint(0, 4)
        if kind == 0:
            I, R = rng.randint(1, 20), rng.randint(2, 99)
            out.append((f'A current of {I} A flows through {R} ohms. Voltage across it in volts (integer)?', str(I * R)))
        elif kind == 1:
            a, b = rng.choice([(6, 3), (12, 6), (10, 10), (20, 5), (30, 60), (4, 12), (9, 18), (40, 10)])
            out.append((f'Resistors of {a} and {b} ohms in parallel. Equivalent resistance in ohms (integer)?', str(a * b // (a + b))))
        elif kind == 2:
            V, R1, R2 = rng.choice([12, 24, 5, 10, 48]), rng.randint(1, 9) * 1000, rng.randint(1, 9) * 1000
            out.append((f'Voltage divider: {V} V across R1 = {R1} ohm in series with R2 = {R2} ohm. Voltage across R2 to 2 decimals?', f'{V*R2/(R1+R2):.2f}'))
        elif kind == 3:
            R, C = rng.randint(1, 99) * 1000, rng.choice([1, 2, 5, 10, 22, 47, 100])
            out.append((f'RC circuit with R = {R} ohm and C = {C} microfarad. Time constant tau = RC in milliseconds (integer)?', str(R * C // 1000)))
        else:
            V, R = rng.choice([5, 10, 12, 20, 24]), rng.choice([2, 4, 5, 8, 10, 20])
            out.append((f'{V} V across a {R} ohm resistor. Power dissipated P = V^2/R in watts, to 1 decimal?', f'{V*V/R:.1f}'))
    return out


# ---------------- Stage 5: digital logic ----------------
@_t(5)
def _logic_gates(rng, n):
    out = []
    ops = {'AND': lambda a, b: a & b, 'OR': lambda a, b: a | b, 'XOR': lambda a, b: a ^ b, 'NAND': lambda a, b: 1 - (a & b), 'NOR': lambda a, b: 1 - (a | b)}
    for i in range(n):
        kind = rng.randint(0, 4)
        if kind == 0:
            v = rng.randint(1, 255); out.append((f'Write {v} in binary (no prefix, no leading zeros).', bin(v)[2:]))
        elif kind == 1:
            v = rng.randint(16, 4095); out.append((f'Write {v} in hexadecimal, uppercase, no prefix.', f'{v:X}'))
        elif kind == 2:
            a, b, c = rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 1); o1, o2 = rng.sample(list(ops), 2)
            out.append((f'Inputs A={a}, B={b}, C={c}. Output = ({o1} of A and B) {o2} C. Give 0 or 1.', str(ops[o2](ops[o1](a, b), c))))
        elif kind == 3:
            a, b, cin = rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 1); s = a + b + cin
            out.append((f'Full adder with A={a}, B={b}, carry-in={cin}. Give SUM and CARRY as two digits, e.g. 10.', f'{s & 1}{s >> 1}'))
        else:
            v = rng.randint(1, 127); bits = rng.choice([8])
            out.append((f'Write -{v} as an {bits}-bit two\'s-complement binary number.', format((1 << bits) - v, f'0{bits}b')))
    return out


@_t(5)
def _logic_code(rng, n):
    out = []
    for i in range(n):
        k, kind = rng.randint(2, 8), rng.randint(0, 2)
        vals = list(range(0, 260, 7))
        if kind == 0:
            exp = [(v, sum((v >> j) & 1 for j in range(k))) for v in vals]
            q = f'Write a Python function f(x) that returns how many of the lowest {k} bits of a non-negative integer x are 1, without using bin(). Give only the code.'
        elif kind == 1:
            exp = [(v, v & ((1 << k) - 1)) for v in vals]
            q = f'Write a Python function f(x) that returns the lowest {k} bits of a non-negative integer x as an integer (a bit mask). Give only the code.'
        else:
            exp = [(v, (v << k) & 0xFFFF) for v in vals]
            q = f'Write a Python function f(x) that shifts x left by {k} bits and keeps only the lowest 16 bits. Give only the code.'
        out.append((q, 'TEST:all(f(v)==c for v,c in ' + repr(exp) + ')'))
    return out


# ---------------- Stage 6: CPU design ----------------
@_t(6)
def _cpu_trace(rng, n):
    out = []
    for i in range(n):
        r = [0, 0, 0, 0]; lines = []
        for k in range(rng.randint(4, 6)):
            op = rng.choice(['LI', 'ADD', 'SUB', 'MUL', 'LI']) if k > 1 else 'LI'
            d = rng.randint(0, 3)
            if op == 'LI':
                v = rng.randint(1, 20); r[d] = v; lines.append(f'LI r{d}, {v}')
            else:
                s1, s2 = rng.randint(0, 3), rng.randint(0, 3)
                val = {'ADD': r[s1] + r[s2], 'SUB': r[s1] - r[s2], 'MUL': r[s1] * r[s2]}[op]; r[d] = val
                lines.append(f'{op} r{d}, r{s1}, r{s2}')
        t = rng.randint(0, 3)
        out.append((f'All registers start at 0. LI loads a constant; ADD/SUB/MUL rd, rs, rt compute rd = rs op rt. Program: {"; ".join(lines)}. Final value of r{t}?', str(r[t])))
    return out


@_t(6)
def _cpu_perf(rng, n):
    out = []
    for i in range(n):
        kind = rng.randint(0, 3)
        if kind == 0:
            s, N = rng.randint(3, 8), rng.randint(5, 200)
            out.append((f'An ideal {s}-stage pipeline with no stalls runs {N} instructions. Total clock cycles?', str(s + N - 1)))
        elif kind == 1:
            N, cpi, f = rng.randint(1, 50) * 1000, rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 4, 5])
            out.append((f'{N} instructions at CPI {cpi} on a {f} GHz clock. Run time in nanoseconds (integer)?', str(N * cpi // f)))
        elif kind == 2:
            h, m, p = rng.choice([1, 2, 3, 4]), rng.choice([2, 5, 10, 20]), rng.choice([50, 100, 200])
            out.append((f'Cache hit time {h} cycles, miss rate {m}%, miss penalty {p} cycles. Average memory access time in cycles (to 1 decimal)?', f'{h + m/100*p:.1f}'))
        else:
            blk, lines_ = rng.choice([16, 32, 64, 128]), rng.choice([64, 128, 256, 512, 1024])
            out.append((f'Direct-mapped cache with {lines_} lines of {blk} bytes and 32-bit addresses. How many tag bits?', str(32 - int(math.log2(blk)) - int(math.log2(lines_)))))
    return out


TRACKS = {name.lstrip('_'): f for name, f in [
    ('nuc_count', _nuc_count), ('nuc_binding', _nuc_binding), ('nuc_decay', _nuc_decay), ('nuc_qvalue', _nuc_qvalue),
    ('rx_power', _rx_power), ('rx_limits', _rx_limits), ('rx_breeding', _rx_breeding),
    ('fields', _fields), ('circuits', _circuits),
    ('logic_gates', _logic_gates), ('logic_code', _logic_code),
    ('cpu_trace', _cpu_trace), ('cpu_perf', _cpu_perf)]}
