"""Twin slip-ladder DATA SHEET (P-Q9/P-Q10). Writes theory/quarks/LADDER_DATASHEET.csv.
Left ladder: (m,0) classes, rungs climb toward the knot ρ (CP-violating minima, 2201.02020).
Right ladder: (0,n) classes, minima at the knot i (CP-conserving, 2201.02020).
Centre: mixed (m,n) classes sit on the arc |τ|=1 between ρ and i (CP-conserving), moving toward ρ or i as m or n grows.
Every number carries a status: lit (paper), formula (paper's fit, verified m<=7), extrap (m>7), computed, or open."""
import csv, math, os
c = math.sqrt(3)*0.0145
OCC = {1: 'down quarks; charged leptons (T1, D1734; TENSION with Koide-at-ρ)', 8: 'up quarks (T2: m_u*=8.26, chance 52%)'}
rows = []
for m in list(range(1, 33)) + [48, 64, 128]:
    e = c/(m + 1/16)
    rows.append(dict(side='left (ρ)', cls=f'({m},0)', rung=m, eps_abs=f'{e:.5f}', eps_arg_deg=50.0, cp='violating',
                     m2_over_m3_scale=f'{e:.5f}', m1_over_m3_scale=f'{e*e:.2e}', occupant=OCC.get(m, 'empty'),
                     status='computed (Q11, ±0.4%)' if m <= 32 else 'extrap (formula)'))
rows.append(dict(side='left (ρ)', cls='(∞,0)', rung='∞', eps_abs='0', eps_arg_deg='', cp='conserving (knot)', m2_over_m3_scale='0',
                 m1_over_m3_scale='0', occupant='Koide circulant leptons? (D1595); inflaton endpoint (D1606)', status='lit/derived'))
ARC = {(1,1): -0.23776+0.97132j, (2,1): -0.28568+0.95832j, (3,1): -0.31151+0.95024j, (1,2): -0.19009+0.98177j, (1,3): -0.16344+0.98655j}
for (a, b), t in ARC.items():
    rows.append(dict(side='centre (arc)', cls=f'({a},{b})', rung=f'm/n={a}/{b}', eps_abs=f'tau={t.real:.4f}{t.imag:+.4f}i', eps_arg_deg='', cp='conserving (arc)',
                     m2_over_m3_scale='open', m1_over_m3_scale='open', occupant='none assigned', status='computed (Q11); position set by m/n only'))
for n in (1, 2, 3, '∞'):
    rows.append(dict(side='right (i)', cls=f'(0,{n})', rung=n, eps_abs='0 (τ = i)', eps_arg_deg='', cp='conserving',
                     m2_over_m3_scale='none (no slip)', m1_over_m3_scale='none', occupant='neutrino modulus (P-F3); dark thread rests at i (D1653)' if n == '∞' else 'empty',
                     status='lit'))
p = os.path.join(os.path.dirname(__file__), 'LADDER_DATASHEET.csv')
with open(p, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(p, len(rows), 'rows')
